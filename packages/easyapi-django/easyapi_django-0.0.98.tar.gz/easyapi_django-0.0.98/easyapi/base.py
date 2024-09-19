from datetime import datetime
import json
import os
import re
from functools import reduce
from importlib import import_module
from urllib import parse

from asgiref.sync import sync_to_async
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connections
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import View
from django.db.utils import IntegrityError
import operator
from redis import asyncio as aioredis

from .filters import Filter as OrmFilter
from .exception import HTTPException
from .tenant.tenant import aset_tenant
from settings.env import REDIS_PREFIX
from settings.settings import COOKIE_ID

re_id = re.compile(r'(.*)\/(?:(?P<uuid>\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)|(?P<int_id>\d+))(?:\/)?$')
search_regex = re.compile(r'__isnull|__gte|__lte|__lt|__gt|__startswith')

REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_DB = os.environ['REDIS_DB']

try:
    Segment = getattr(
        import_module('modules.segment.models'),
        'Segment'
    )
except ImportError:
    Segment = None


async def method_not_allowed(self, **kwargs):
    raise HTTPException(405, 'Method not allowed')


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(obj)


def get_edit_related(args, field):
    result = args['result']
    model = args['model']
    obj = args['obj']

    model = model.split('__')

    if len(model) > 1:
        obj = getattr(obj, model[0])
        model = '__'. join(model[1:])
        reduce(get_edit_related, [field], {'model': model, 'obj': obj, 'result': result})
    else:
        model = model[0]
        keys = field.split('__')
        if len(keys) == 1:
            obj = getattr(obj, model)
            result[field] = getattr(obj, field, None)
            if 'id' not in result:
                result['id'] = getattr(obj, 'id')
        else:
            result[keys[0]] = {}
            reduce(get_edit_related, keys[1:], {'model': keys[0], 'obj': getattr(obj, model), 'result': result[keys[0]]})
    return args


def get_related_objects(args, model):
    obj = args[0]
    result = args[1]
    count = args[2]
    parent = args[3]
    related_models = args[4]
    related_fields = args[5]
    model_obj = getattr(obj, model, None)

    if count == 0:
        # Adicionado para não ser excluído no return_result
        if model not in related_models:
            related_models[model] = []

        if model_obj:
            result[model] = {}
            for field in related_fields[parent]:
                result[model][field] = getattr(model_obj, field, None)
                related_models[model].append(field)
        else:
            result[model] = None

    else:
        return model_obj, result, count - 1, parent, related_models, related_fields


class BaseResource(View):
    authenticated = True
    allowed_methods = ['delete', 'get', 'patch', 'post']
    routes = []

    account_db = 'default'
    cache = False
    cache_ttl = 60
    session_cache = False

    limit = 25
    page = 1
    order_by = 'id'
    count_results = False

    id = None
    model = None
    queryset = None

    app_label = None
    model_name = None
    contextId = None

    fields = []
    all_fields = []
    fk_fields = []
    m2m_fields = []

    related_models = {}
    list_related_fields = {}
    many_to_many_models = {}
    edit_prefetch_related = None
    list_prefetch_related = None

    filter_fields = []
    queryset_filter = []
    search_fields = []
    order_fields = []
    list_fields = []
    list_exclude_fields = []
    edit_fields = []
    edit_related_fields = {}
    edit_set = {}
    edit_exclude_fields = ['_state']
    update_fields = []
    create_fields = []

    default_filter = None
    search_operator = 'icontains'

    obj = None
    obj_id = None
    data = None

    normalize_list = False
    normalize_obj = False
    normalized = False

    diff = {}

    user = None
    account = None
    body = None

    def __init__(self):

        self.diff = {}

        if self.model:
            fields = []
            for field in self.model._meta.get_fields():
                if not field.is_relation:
                    fields.append(field.name)
                    continue

                if field.concrete and field.many_to_many:
                    self.m2m_fields.append(field.name)
                    continue

                if field.concrete and field.many_to_one:
                    self.fk_fields.append(field.name)
                    fields.append(f'{field.name}_id')
                    continue

                # if not field.concrete and field.one_to_many:
                #     self.related_fields.append(field.name)
                #     continue

            all_fields = [
                field.name for field in self.model._meta.local_fields
            ]
            self.all_fields = all_fields + self.m2m_fields

            self.fields = fields
            self.list_fields = self.list_fields or fields

            if not self.edit_fields:
                self.edit_fields = [field.column for field in self.model._meta.local_fields]  # + m2m_fields

            self.queryset = self.model.objects

    def get_method(self, request, args, kwargs):
        self.request = request
        for route in self.routes:
            match = re.search(route['path'], request.path)
            if match:
                allowed_methods = route.get('allowed_methods')
                return getattr(self, route['func']), match.groupdict(), allowed_methods

        return None, None, None

    async def dispatch(self, request, *args, **kwargs) -> None:
        session = None
        if request.headers.get('X-Api-Key') and hasattr(request, 'api_session'):
            # session = request.api_session
            pass
        else:
            session_key = request.COOKIES.get(COOKIE_ID)
            if session_key:
                redis = await aioredis.Redis(
                    host=REDIS_SERVER, db=REDIS_DB, decode_responses=True
                ).client()
                prefix = f'{REDIS_PREFIX}:' if REDIS_PREFIX else ''
                session_key = f'{prefix}sessions:{session_key}'
                session = await redis.get(session_key)
                await redis.close()
                await redis.connection_pool.disconnect()
                if session:
                    session = json.loads(session)
                    self.user = session['user']
                    self.account = session.get('account')

        if self.authenticated and not session:
            raise HTTPException(401, 'Not authorized')

        if session and session.get('account'):
            self.account_db = await aset_tenant(session['account']['id'])
            self.account_id = session['account']['id']

        self.method = 'get' if request.method == 'HEAD' else request.method.lower()

        # func é o método que será executado, caso exista rota personalizada
        func, match, allowed_methods = self.get_method(request, args, kwargs)

        if func:
            self.allowed_methods = allowed_methods or self.allowed_methods

        if self.method not in self.allowed_methods:
            raise HTTPException(405, f'{self.method.upper()} not allowed')

        if not func:
            handler = getattr(self, self.method, method_not_allowed)

        self.cache = self.cache and self.method == 'get'
        if self.cache:
            self.cache_key = f'{REDIS_PREFIX}:cache' if REDIS_PREFIX else 'easyapi:cache'
            if self.session_cache:
                self.cache_key += f':{session_key}'
            self.cache_key += f':{request.path}'

            redis = await aioredis.Redis(
                host=REDIS_SERVER, db=REDIS_DB, decode_responses=True
            ).client()
            response = await redis.get(self.cache_key)
            await redis.close()
            await redis.connection_pool.disconnect()

            if response:
                return JsonResponse(json.loads(response), encoder=CustomJSONEncoder, safe=False)

        await self.pre_process(request)

        if self.method in ['get', 'patch']:
            id_match = re_id.match(request.path_info)
            if id_match:
                uuid = id_match.group('uuid')
                id = id_match.group('int_id')
                self.id = id or uuid

        if self.method in ['post', 'patch']:
            if request.content_type != 'multipart/form-data':
                try:
                    self.body = json.loads(request.body.decode('utf-8'))
                except Exception:
                    raise HTTPException(
                        400, 'Invalid body'
                    )
                await self.hydrate(self.body)
        else:
            self.body = None

        if self.method == 'get' and not self.id:
            self.build_filters(request)
            self.paginate(request)
            self.ordenate(request)

        if self.queryset_filter:
            self.queryset = self.queryset.filter(**self.queryset_filter)

        if func:
            if self.method in ['post', 'patch']:
                response = await func(request, match=match, body=self.body)
            else:
                response = await func(request, match=match)
        else:
            response = await handler(request)

        if type(response) in [dict, list]:
            response = await self.serialize(response)

        return response

    def build_filters(self, request):
        if not self.queryset:
            return

        if hasattr(self, 'model_filter'):
            self.queryset = self.queryset.filter(**self.model_filter)

        if request.GET.get('search'):
            self.search_fields += ['id']
            filters = reduce(
                operator.or_, [
                    Q((f'{field}__{self.search_operator}',
                      request.GET.get('search')))
                    for field in self.search_fields
                ]
            )
            self.queryset = self.queryset.filter(filters)

        params = dict(request.GET)
        if self.filter_fields:
            filter = {}
            for key in params:
                if key == 'normalize':
                    self.normalize_list = True
                    continue

                if search_regex.search(key):
                    keys = key.split('__')
                    if len(keys) == 3:
                        field = f'{keys[0]}__{keys[1]}'
                    else:
                        field = keys[0]

                else:
                    field = key

                if field in self.filter_fields:
                    param = params[key][0]
                    if param.lower() == 'false':
                        param = False
                    elif param.lower() == 'true':
                        param = True

                    filter[key] = param

            self.queryset = self.queryset.filter(**filter)

        if (
            self.model and f'{self.model._meta.app_label}_{self.model._meta.model_name}' == 'core_tag'
        ):
            context = request.GET.get('context')
            if context:
                self.queryset = self.queryset.filter(context=context)

        tags = request.GET.get('tags')
        if tags and hasattr(self.model, 'tags'):
            tags_operator = request.GET.get('tags_operator', 'OR')
            tags_ids = tags.split(',')
            if tags_operator == 'OR':
                self.queryset = self.queryset.filter(tags__id__in=tags_ids)

            # try:
            #     tags = self.Meta.related_tag_model['model'].objects.filter(
            #         tag_id__in=tag_values
            #     ).values(self.Meta.related_tag_model['field']).annotate(count=Count('tag_id'))
            # except Exception:
            #     orm_filters['pk__in'] = []
            #     return orm_filters

            # if filters.get('tags_operator', 'AND').upper() == ConditionOperator.AND:
            #     total_tags = len(tag_values)
            #     tags = tags.filter(count=total_tags)

            # orm_filters['pk__in'] = [obj[self.Meta.related_tag_model['field']] for obj in tags]

    def ordenate(self, request):
        order_by = request.GET.get('order_by')
        if order_by and order_by.split('-')[-1] in self.order_fields:
            self.order_by = order_by

    def paginate(self, request):
        page = request.GET.get('page')
        if page:
            try:
                self.page = int(page)
            except Exception:
                pass

        limit = request.GET.get('limit')
        if limit:
            try:
                self.limit = int(limit)
            except Exception:
                pass

    #########################################################
    # Funçoes dentro do Resource
    #########################################################
    async def serialize(self, result, **kwargs):

        if type(result) is JsonResponse:
            return result

        response = kwargs.get('response')
        if response:
            return response

        if not self.count_results:

            if isinstance(result, list):
                for row in result:
                    await self.dehydrate(row)

            elif type(result) is dict and 'objects' in result:
                for row in result['objects']:
                    await self.dehydrate(row)

            else:
                await self.dehydrate(result)

        result = await self.post_process(result)
        await self.save_cache(result)

        return JsonResponse(result, encoder=CustomJSONEncoder, safe=False)

    async def save_cache(self, content):
        if not self.cache:
            return

        redis = await aioredis.Redis(
            host=REDIS_SERVER, db=REDIS_DB, decode_responses=True
        ).client()
        await redis.set(self.cache_key, json.dumps(content))
        await redis.expire(self.cache_key, self.cache_ttl)
        await redis.close()
        await redis.connection_pool.disconnect()

    async def add_m2m(self, result):
        return await result

    async def alter_detail(self, result):
        return result

    async def alter_list(self, results):
        return results

    async def hydrate(self, body):
        return body

    async def pre_process(self, request):
        return request

    async def dehydrate(self, response):
        return response

    async def post_process(self, response):
        return response

    #########################################################
    # GET
    #########################################################

    # count só se aplica a listagens
    @sync_to_async
    def count(self):
        count = 0
        self.count_results = 10
        if not hasattr(self.queryset, 'query'):
            self.queryset = self.queryset.all()

        query, params = self.queryset.query.sql_with_params()
        table = self.model._meta.db_table
        query = re.sub(
            r'^SELECT .*? FROM',
            f'SELECT count(DISTINCT {table}.id) FROM',
            query,
        )

        connection = connections[self.account_db]
        cursor = connection.cursor()
        cursor.execute(query, params)
        count = cursor.fetchone()[0]

        self.count_results = {'count': count}

    # filtro por segmento/filter só se aplica a listagens
    async def get_filters(self, request):
        filter_ = request.GET.get('filter')

        segment_id = request.GET.get('segment_id')

        if segment_id is None and filter_ is None:
            return

        if Segment and segment_id:
            segment = await Segment.objects.filter(id=segment_id).afirst()
            conditions = segment.conditions

        elif filter_:
            conditions = json.loads(filter_)

        if not conditions:
            return

        queryset = OrmFilter(
            self.model,
            self.user.get('timezone', 'UTC') if self.user else 'UTC'
        )
        queryset = queryset.filter_by(conditions)

        if request.GET.get('search'):
            self.search_fields += ['id']
            filters = reduce(
                operator.or_, [
                    Q((f'{field}__{self.search_operator}',
                      request.GET.get('search')))
                    for field in self.search_fields
                ]
            )
            queryset = queryset.filter(filters)

        self.queryset = queryset.distinct()

    async def return_results(self, results):

        if type(results) is JsonResponse:
            return results

        if self.count_results:
            return self.count_results

        results = await self.alter_list(results)

        if self.normalized:
            return results

        if self.normalize_list and isinstance(results, list):
            normalized = {}
            for result in results:
                normalized[result['id']] = result
            return normalized

        result = {}
        if self.limit:
            params = {**self.request.GET} if self.request.GET else {}
            params['page'] = self.page + 1
            next_page = self.request.path + '?' + parse.urlencode(params)

            result['meta'] = {
                'page': self.page,
                'limit': self.limit,
                'next': next_page,
            }

            if self.page > 1:
                params['page'] = self.page - 1
                previous_page = self.request.path + \
                    '?' + parse.urlencode(params)
                result['meta']['previous'] = previous_page

        result['objects'] = results
        return result

    async def get_objs(self, request):
        await self.get_filters(request)

        if request.GET.get('count'):
            return await self.count()

        if self.page > 0:
            start = (self.page - 1) * self.limit
        else:
            start = 0

        if self.list_related_fields:
            self.queryset = self.queryset.select_related(*self.list_related_fields.keys())

        prefetch_fields = self.list_prefetch_related.keys() if self.list_prefetch_related else []
        if prefetch_fields:
            self.queryset = self.queryset.prefetch_related(*prefetch_fields)

        self.queryset = self.queryset.order_by(
            self.order_by
        )

        if self.limit:
            self.queryset = self.queryset[start:start + self.limit]

        results = []

        fields = request.GET.get('fields')
        if fields:
            list_fields = fields.split(',')
            related = False
        else:
            list_fields = self.list_fields
            related = True

        async for row in self.queryset:
            result = {}
            if related:
                for key, fields in self.list_related_fields.items():
                    model = key.split('__')
                    count = len(model) - 1
                    reduce(
                        get_related_objects, model, (row, result, count, key, self.related_models, self.list_related_fields)
                    )

            for field in list_fields:
                if field in self.list_exclude_fields:
                    continue

                result[field] = getattr(row, field, None)

            for field in prefetch_fields:
                result[field] = []
                query = getattr(row, field)
                async for prefetch in query.values(*self.list_prefetch_related[field]):
                    result[field].append(prefetch)

            results.append(result)

        return results

    async def return_result(self, result):
        for key in list(result):
            if (
                self.edit_fields and
                key not in self.edit_fields and
                key not in self.edit_related_fields and
                key != '_result' and
                key not in self.related_models and
                key not in self.m2m_fields
            ):
                if result.get(key):
                    del result[key]

            if self.edit_exclude_fields and key in self.edit_exclude_fields:
                if result.get(key):
                    del result[key]

        result = await self.alter_detail(result)

        if self.normalize_obj:
            normalized = {}
            normalized[result['id']] = result
            return await self.serialize(normalized)

        return result

    async def get_obj(self, id):
        related_fields = None

        if self.edit_related_fields:
            related_fields = list(self.edit_related_fields.keys())
            for key in self.edit_related_fields.keys():
                for rf in self.edit_related_fields[key]:
                    rf = rf.split('__')
                    if len(rf) > 1:
                        new_rf = key + '__' + '__'.join(rf[:-1])
                        related_fields.append(new_rf)

            self.queryset = self.queryset.select_related(*related_fields)

        prefetch_fields = self.edit_prefetch_related.keys() if self.edit_prefetch_related else []
        if prefetch_fields:
            self.queryset = self.queryset.prefetch_related(*prefetch_fields)

        self.obj = await self.queryset.filter(pk=id).afirst()
        if not self.obj:
            raise HTTPException(404, 'Object does not exist')

        result = {}

        for model, fields in self.edit_related_fields.items():
            final = {}
            obj = self.obj

            if hasattr(obj, model) and not getattr(obj, model):
                result[model] = {}
                continue

            reduce(get_edit_related, fields, {'model': model, 'obj': obj, 'result': final})
            result[model] = final

        for field in self.edit_fields:
            result[field] = getattr(self.obj, field, None)

        for field in prefetch_fields:
            result[field] = []
            query = getattr(self.obj, field)
            async for prefetch in query.values(*self.edit_prefetch_related[field]):
                result[field].append(prefetch)

        for key, value in self.edit_set.items():
            query = getattr(self.obj, key)
            result[key] = []
            async for item in query.values(*value):
                result[key].append(item)

        return result

    async def _get_objs(self, request):
        data = await self.get_objs(request)
        return await self.return_results(data)

    async def get(self, request):
        if self.id:
            data = await self.get_obj(self.id)
            data = await self.alter_detail(data)
            if self.normalize_obj:
                normalized = {}
                normalized[data['id']] = data
                return await self.serialize(normalized)

            return await self.serialize(data)
        else:
            data = await self._get_objs(request)
            return await self.serialize(data)

    #########################################################
    # DELETE
    #########################################################
    async def delete_obj(self, id):
        try:
            await self.queryset.filter(pk=id).adelete()
        except Exception as err:
            raise HTTPException(400, err.__class__.__name__ + ': ' + err.__str__())

        return {'success': True, 'id': id, 'message': 'Deleted'}

    async def delete(self, request):
        id_match = re_id.match(request.path_info)
        if id_match:
            uuid = id_match.group('uuid')
            id = id_match.group('int_id')
            self.id = id or uuid
            results = await self.delete_obj(self.id)
            return await self.serialize(results)
        else:
            raise HTTPException(404, 'Item not found')

    #########################################################
    # PATCH
    #########################################################

    def save_related_tags(self, tags):
        core_tag_model = self.model.tags.field.related_model
        tag_model = self.obj.tags.through
        tag_field = self.model.tags.field._m2m_name_cache + '_id'

        tags_ids = []
        # Crio as tags no contexto
        for tag in tags:
            tag, created = core_tag_model.objects.get_or_create(
                context=self.contextId,
                name=tag
            )
            tags_ids.append(tag.id)

        # Pegando os tags existentes e comparando com os tags enviados, para poder apagar somente
        # os tags que não foram enviados
        existing_tags = [
            tag for tag in
            tag_model.objects.filter(
                **{tag_field: self.obj.id}
            ).values_list('tag_id', flat=True)
        ]

        # Removendo tags
        tag_model.objects.filter(
            **{tag_field: self.obj.id, 'tag_id__in': set(existing_tags) - set(tags_ids)}
        ).delete()

        # Inserindo tags
        insert_tags = set(tags_ids) - set(existing_tags)
        if insert_tags:
            tag_list = [
                tag_model(
                    **{'tag_id': tag_id, tag_field: self.obj.id}
                ) for tag_id in insert_tags
            ]
            tag_model.objects.bulk_create(tag_list)

    async def update_obj(self, id, body):
        keys = list(body.keys())
        allowed = False
        diff = None
        if self.update_fields:
            diff = list(set(keys) - set(self.update_fields))
            allowed = not diff
            diff = (', ').join(list(diff))

        if not allowed:
            raise HTTPException(403, f'Changes on field(s): {diff} is not allowed')

        try:
            self.obj = await self.queryset.aget(pk=id)
        except Exception:
            raise HTTPException(404, 'Item not found')

        to_update = {}
        for key, value in body.items():

            if key in self.m2m_fields:
                query = getattr(self.obj, key)
                await query.aset(value)
                continue

            if key == 'tags':
                self.save_related_tags(value)

            elif key == 'custom_attributes':
                for key, value in body['custom_attributes'].items():
                    self.obj.custom_attributes[key] = value

            else:
                field = getattr(self.model, key)
                if field.field.primary_key:
                    key += '_id'
                    value = int(value)
                to_update[key] = value

                old_value = getattr(self.obj, key)
                self.diff[key] = {'old': old_value, 'new': value}

                setattr(self.obj, key, value)

        if to_update:
            await self.model.objects.filter(pk=id).aupdate(**to_update)

        return await self.get_obj(id)

    async def patch(self, request):
        result = await self.update_obj(self.id, self.body)
        result = await self.return_result(result)
        return await self.serialize(result)

    #########################################################
    # POST
    #########################################################
    async def create_obj(self, request, body):
        keys = list(body.keys())
        allowed = False
        diff = None
        if self.create_fields:
            diff = list(set(keys) - set(self.create_fields))
            allowed = not diff
            diff = (', ').join(diff)

        if not allowed:
            if self.create_fields:
                raise HTTPException(403, f'Creation on field(s): {diff} is not allowed')
            raise HTTPException(500, 'Create fields not defined')

        to_save = {}
        user = self.user

        if user:
            if 'created_by' in self.all_fields:
                body['created_by_id'] = user['id']
            if 'updated_by' in self.all_fields:
                body['updated_by_id'] = user['id']
            if 'owner' in self.all_fields:
                body['owner_id'] = user['id']

        blank_errors = []
        null_errors = []

        for field in self.model._meta.local_fields:
            if field.primary_key:
                continue

            allow_blank = field.blank
            allow_null = field.null
            default = field.has_default() or hasattr(field, 'auto_now') or hasattr(field, 'auto_now_add')

            field_key = f'{field.name}_id' if field.is_relation else field.name

            field_value = body.get(field_key)

            if not default and not allow_blank and field_value == '':
                blank_errors.append(field.verbose_name)

            if not default and not allow_null and not field_value:
                null_errors.append(field.verbose_name)

            if body.get(field_key) is not None:
                to_save[field_key] = body[field_key]

        if blank_errors or null_errors:
            errors = ''
            if blank_errors:
                errors += 'Field(s): ' + ', '.join(blank_errors) + ' can\'t be blank. '

            if null_errors:
                errors += 'Field(s): ' + ', '.join(null_errors) + ' can\'t be null.'

            raise HTTPException(403, errors)

        try:
            obj = await self.model.objects.acreate(**to_save)

        except IntegrityError as error:
            error_message = str(error)
            if "Duplicate entry" in error_message:
                duplicate_value = error_message.split("'")[1].split('-')[1]
                error_message = f'{duplicate_value} já existe e não pode ter outro'

            raise HTTPException(409, error_message)

        self.obj = obj
        self.obj_id = obj.id
        result = await self.get_obj(obj.id)
        return await self.return_result(result)

    async def post(self, request):
        match = re_id.match(request.path_info)
        if match:
            raise HTTPException(403, 'Path not allowed')

        result = await self.create_obj(request, self.body)

        return await self.serialize(result)


class BaseTagsResource(BaseResource):

    async def add_m2m(self, result):
        super().add_m2m(result)

        if self.obj:
            result['tags'] = [tag.name async for tag in self.obj.tags.all()]

        return result


class BaseCustomResource(BaseResource):

    async def add_m2m(self, result):
        super().add_m2m(result)

        if not self.obj_id:
            return result

        fieldsets = {'default': {'name': 'Default',
                                 'order': 100000, 'fields': []}}
        cas_model = self.obj.custom_attributes.model
        cas = cas_model.objects.select_related(
            'fieldset'
        ).order_by('fieldset__order')

        has_type = False
        if hasattr(self.obj, 'card_type') and self.obj.card_type:
            has_type = True
            cas = cas.filter(
                card_type_id=self.obj.card_type.id).order_by('order')

        # definição dos custom fields
        fields = {}
        tmp = {}
        fieldsetId = 'default'
        cas = [ca async for ca in cas]
        for ca in cas:
            if has_type:
                if ca.presentation_id == 11:
                    fieldsetId = ca.presentation_name
                    fieldsets[fieldsetId] = {
                        'name': ca.presentation_name,
                        'order': ca.order,
                        'hide_if_empty': False,
                        'fields': []
                    }
                    continue

            else:
                if ca.fieldset:
                    fieldsetId = ca.fieldset.name
                    if fieldsetId not in fieldsets:
                        fieldsets[fieldsetId] = {
                            'name': ca.fieldset.name,
                            'order': ca.fieldset.order,
                            'hide_if_empty': ca.fieldset.hide_if_empty,
                            'fields': []
                        }
                else:
                    fieldsetId = 'default'

            fields[str(ca.id)] = model_to_dict(ca)
            tmp[ca.id] = fieldsetId

        filter = {}
        filter[
            self.obj.custom_attributes.source_field_name
        ] = self.obj.custom_attributes.instance

        # valores dos customs fields
        cas = [
            ca async for ca in self.obj.custom_attributes.through.objects.select_related(
                'custom_attribute', 'custom_attribute__fieldset'
            ).order_by('custom_attribute__fieldset__order').filter(**filter).all()
        ]
        for ca in cas:
            fields[str(ca.custom_attribute_id)]['value'] = ca.value
            result['ca__' + ca.custom_attribute.name] = ca.value

        fieldsetId = 'default'

        for _, field in fields.items():
            fieldId = field['id']
            fieldsetId = tmp[fieldId]
            fieldsets[fieldsetId]['fields'].append(field)

        fieldsets['default'] = fieldsets.pop('default')
        result['custom_attributes'] = fieldsets

        return result

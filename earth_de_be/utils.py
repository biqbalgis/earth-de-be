import logging
import traceback
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connections

from earth_de_be.middleware.current_user import get_current_user, get_request_path
from earth_de_be.models import ActivityLog


class Data_Logger():
    @classmethod
    def log_view_error_message(cls, request, e, act_log=None, redirect_path=None):
        error_message = str(e)
        cls.log_error_message(e)
        if request:
            messages.add_message(request, messages.ERROR, error_message)
            if redirect_path is None:
                redirect_path = request.META.get('HTTP_REFERER', '')
                if redirect_path == '':
                    redirect_path = "/"
            return redirect_path

        # response.write(error_message)

    @classmethod
    def log_error_message(cls, e, message_type="error", user_id=None):
        error_message = str(e)
        logger = logging.getLogger()
        # if act_log is not None: act_log.update_error_desc(error_message)
        logger.error(traceback.format_exc())
        act_log = ActivityLog()
        act_log.message_type = message_type
        act_log.message = error_message
        act_log.user = get_current_user() if user_id is None else User.objects.filter(pk=user_id).first()
        act_log.stack_trace = traceback.format_exc()
        act_log.save()
        return error_message, act_log.id

    @classmethod
    def log_message(cls, msg, message_type="log", user_id=None):
        logger = logging.getLogger()
        logger.error(msg) if message_type == "error" else logger.debug(msg)
        act_log = ActivityLog()
        act_log.message = msg
        act_log.message_type = message_type
        act_log.request_path = get_request_path()
        act_log.user = get_current_user() if user_id is None else User.objects.filter(pk=user_id).first()
        act_log.save()


class DB_Query(object):
    @classmethod
    def get_connection_key(cls, app_label, model_name=None, table_name=None):
        return 'default'

    @classmethod
    def execute_query_as_list(self, query, app_label='default'):
        connection_name = DB_Query.get_connection_key(app_label)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            result_list = list(cursor.fetchall())
            cursor.close()
        return result_list

    @classmethod
    def execute_query_as_dict(self, query, is_geom_include=True, app_label='default', model_name=None):
        connection_name = DB_Query.get_connection_key(app_label)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            if is_geom_include:
                result_dict = DB_Query.dictfetchall(cursor)
            else:
                result_dict = DB_Query.dictfetchallXGeom(cursor)
            cursor.close()
        return result_dict

    @classmethod
    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def dictfetchallXGeom(self, cursor):
        columns = []
        for col in cursor.description:
            if col[0] != "geom":
                columns.append(col[0])
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def execute_query_as_one(self, query, is_one=True, app_label='default', model_name=None):
        connection_name = DB_Query.get_connection_key(app_label, model_name)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            cur_res = cursor.fetchone()
            if cur_res is not None:
                result = cur_res[0]
            cursor.close()
        return result

    @classmethod
    def execute_dml(self, query, app_label='default'):
        connection_name = DB_Query.get_connection_key(app_label)
        connection = connections[connection_name]
        cursor = connection.cursor()
        res = cursor.execute(query)
        return res

    @classmethod
    def execute_query_as_geojson(cls, query, app_label='gis', geom_col='geom'):
        geo_json_query = "SELECT jsonb_build_object(" \
                         "'type',     'FeatureCollection'," \
                         "'features', jsonb_agg(feature)) " \
                         "FROM ( " \
                         "SELECT jsonb_build_object( " \
                         "'type', 'Feature', " \
                         "'geometry',   ST_AsGeoJSON(%s)::jsonb," \
                         "'properties', to_jsonb(row) - 'geom' -'geometry'" \
                         ") AS feature " \
                         "FROM (%s) row) features;" % (geom_col, query)
        result = DB_Query.execute_query_as_one(geo_json_query, app_label=app_label)
        return result


# class Model_Utils():
    # @classmethod
    # def get_model_filter_result_dict(cls, app_label, model_name, field_value, field_name='id'):
    #     model = apps.get_model(app_label=app_label, model_name=model_name)
    #     res = list(model.objects.filter(**{field_name: field_value}).values())
    #     return res

    # @classmethod
    # def get_model_fields_names(cls, app_label, model_name, include_geometry=False):
    #     model = apps.get_model(app_label=app_label, model_name=model_name)
    #     fields = model._meta.get_fields()
    #     field_names = [];
    #     skip_field_types = MODEL_FIELD_TYPES["relational"] + MODEL_FIELD_TYPES["spatial"] if not include_geometry else [
    #         "AutoField"]
    #     for field in fields:
    #         if field.get_internal_type() not in skip_field_types:
    #             field_names.append({"name": field.name, "db_col": field.column, "type": field.get_internal_type()})
    #     return field_names

    # @classmethod
    # def get_model_col_name(cls, model):
    #     fields_name = Model_Utils.get_model_fields_names(model._meta.app_label, model._meta.model_name)
    #     cols = []
    #     for field in fields_name:
    #         cols.append(field['name'])
    #     return cols

    # @classmethod
    # def get_model_spatial_cols_names(cls, model):
    #     fields = model._meta.get_fields()
    #     cols = []
    #     for field in fields:
    #         if field.get_internal_type() in MODEL_FIELD_TYPES["spatial"]:
    #             cols.append(field.name)
    #     return cols
    #
    # @classmethod
    # def get_model_foregin_cols_names(cls, model):
    #     fields = model._meta.get_fields()
    #     cols = []
    #     for field in fields:
    #         if field.get_internal_type() in MODEL_FIELD_TYPES["relational"]:
    #             if field.many_to_one == True:
    #                 cols.append(field.name)
    #     return cols


class MIDDLEWARE_Utils:
    @classmethod
    def get_request_url(cls, request):
        origin = request.META.get("HTTP_ORIGIN")
        if not origin:
            origin = request.META.get('HTTP_REFERER')
        if not origin:
            host = request.META.get("HTTP_HOST")
            origin = 'http://%s' % host
        url = urlparse(origin)
        return url


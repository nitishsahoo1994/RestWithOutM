from os import stat_result

from django.core.serializers import serialize
import json
from django.http import HttpResponse

class SerializeMixin():
    def serialize(self,qs):
        json_data=serialize('json',qs)
        emp_dict=json.loads(json_data)
        final_list=[]
        for obj in emp_dict:
            emp_list=obj['fields']
            final_list.append(emp_list)
        json_data=json.dumps(final_list)
        return json_data

class HttpResponseMixin():
    def render_to_http_response(self,json_data,status=200):
        return HttpResponse(json_data,content_type='application/json',status=status)
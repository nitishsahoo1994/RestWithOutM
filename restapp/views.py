from django.core.serializers import serialize
from django.shortcuts import render
from django.views.generic.base import View
from restapp.models import Employee
import json
from restapp.mixins import SerializeMixin,HttpResponseMixin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from restapp.utils import is_json
from restapp.forms import EmployeeForm

class EmployeeDetailCBV(HttpResponseMixin,SerializeMixin,View):
    def get(self,request,id,*args,**kwargs):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist :
            json_data=json.dumps({'msg':'This Value doesn\'t exit'})
            return self.render_to_http_response(json_data,status=400)
        else:
            json_data = self.serialize([emp, ])
            return self.render_to_http_response(json_data,status=200)


@method_decorator(csrf_exempt,name='dispatch')
class EmployeeListCBV(HttpResponseMixin,SerializeMixin,View):
    def get(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        json_data=self.serialize(qs)
        return HttpResponse(json_data,content_type='application/json')
    def post(self,request,*args,**kwargs):
        data=request.body
        valid_json=is_json(data)
        if not valid_json:
            json_data=json.dumps({'msg':'This is not valid json data'})
            return self.render_to_http_response(json_data, status=400)
        emp_data=json.loads(data)
        form=EmployeeForm(emp_data)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'msg':'Resource Created Successfully'})
            return self.render_to_http_response(json_data,status=200)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_http_response(json_data, status=400)
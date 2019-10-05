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

@method_decorator(csrf_exempt,name='dispatch')
class EmployeeDetailCBV(HttpResponseMixin,SerializeMixin,View):
    def get_object_by_id(self,id):
        try:
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp=None
        return emp
    def get(self,request,id,*args,**kwargs):
        try:
            emp = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            json_data=json.dumps({'msg':'This Value doesn\'t exit'})
            return self.render_to_http_response(json_data,status=400)
        else:
            json_data = self.serialize([emp, ])
            return self.render_to_http_response(json_data,status=200)

    def put(self,request,id,*args,**kwargs):
        emp=self.get_object_by_id(id)
        if emp is None:
            json_data=json.dumps({'msg':'This data doesn\'t exit'})
            return self.render_to_http_response(json_data,status=400)
        data=request.body
        valid_json=is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg': 'Upadates data is not valid'})
            return self.render_to_http_response(json_data, status=400)
        update_list=json.loads(data)
        origional_list={
            'eno':emp.eno,
            'ename': emp.ename,
            'esal': emp.esal,
            'eaddr': emp.eaddr,
        }
        origional_list.update(update_list)
        form=EmployeeForm(origional_list)
        if form.is_valid:
            form.save(commit=True)
            json_data = json.dumps({'msg': 'Resource update Successfully'})
            return self.render_to_http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.error)
            return self.render_to_http_response(json_data,status=400)








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
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
class EmployeeCRUDCBV(SerializeMixin,HttpResponseMixin,View):
    def get_object_by_id(self,id):
        try:
            emp=Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            emp=None
        return emp

    def get(self,request,*args,**kwargs):
        data=request.body
        valid_json=is_json(data)
        if not valid_json:
            json_data=json.dumps({'msg':'This is not a valid Json'})
            return self.render_to_http_response(json_data,status=404)
        pdata=json.loads(data)
        id=pdata.get('id',None)
        if id is not None:
            emp=self.get_object_by_id(id)
            if emp is None:
                json_data = json.dumps({'msg':'The request resource is not avialable with matched id:'})
                return self.render_to_http_response(json_data, status=404)
            json_data=self.serialize([emp,])
            return self.render_to_http_response(json_data)
        qs=Employee.objects.all()
        json_data = self.serialize(qs)
        return self.render_to_http_response(json_data)

    def post(self,request,*args,**kwargs):
        data=request.body
        valid_json=is_json(data)
        if not valid_json:
            json_data=json.dumps({'msg':'This is not a valid Json Data'})
            return self.render_to_http_response(json_data,status=404)
        emp_data=json.loads(data)
        form=EmployeeForm(emp_data)
        if form.is_valid():
            form.save(commit=True)
            json_data = json.dumps({'msg': 'Resource Submitted Successfully'})
            return self.render_to_http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=404)

    def put(self,request,*args,**kwargs):
        data=request.body
        valid_json=is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg':'This is not a valid Json'})
            return self.render_to_http_response(json_data, status=404)
        pdata=json.loads(data)
        id=pdata.get('id',None)
        if id is None:
            json_data = json.dumps({'msg':'To perform updation id is mandatory,Please provide id'})
            return self.render_to_http_response(json_data, status=404)
        emp=self.get_object_by_id(id)
        if emp is None:
            json_data = json.dumps({'msg':'The request source is not avialable with matched id:,Please provide valid id'})
            return self.render_to_http_response(json_data, status=404)
        update_data=json.loads(data)
        origional_data={
            'eno':emp.eno,
            'ename': emp.ename,
            'esal': emp.esal,
            'eaddr': emp.eaddr,
        }
        origional_data.update(update_data)
        form=EmployeeForm(origional_data,instance=emp)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'msg':'Updation is Success'})
            return self.render_to_http_response(json_data)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=404)

    def delete(self,request,*args,**kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg': 'This is not a valid Json'})
            return self.render_to_http_response(json_data, status=404)
        pdata = json.loads(data)
        id = pdata.get('id', None)
        if id is not None:
            emp = self.get_object_by_id(id)
            if emp is None:
                json_data = json.dumps({'msg': 'The request resource is not avialable with matched id:'})
                return self.render_to_http_response(json_data, status=404)
            status,deleted_items=emp.delete()
            if status==1:
                json_data=json.dumps({'msg':"Deleted successfully"})
                return self.render_to_http_response(json_data)
            json_data=json.dumps({'msg':'Unable to delete..plz try again'})
            return  self.render_to_http_response(json_data,status=400)
        json_data = json.dumps({'msg': 'To perform delete operation id is mandatory'})
        return self.render_to_http_response(json_data, status=400)
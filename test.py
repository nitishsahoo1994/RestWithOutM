import requests
import json

BASE_URI='http://127.0.0.1:8000/'
ENDPOINT='api/'

def get_resource(id=None):
    data={}
    if id is not None:
        data = {
            'id': id
        }
    resp = requests.get(BASE_URI + ENDPOINT, data=json.dumps(data))
    print(resp.status_code)
    print(resp.json())
def create_resource():
    new_emp = {
             'eno':999,
            'ename':'Rakul Preet',
            'esal':99999,
             'eaddr':'Chennai',
       }
    resp=requests.post(BASE_URI+ENDPOINT,data=json.dumps(new_emp))
    print(resp.status_code)
    print(resp.json())
def update_resource(id):
    new_emp={
        'id':id,
        'easl':9595,
        'eaddr':'Bhubaneswar,Odisha',
    }
    resp=requests.put(BASE_URI+ENDPOINT,data=json.dumps(new_emp))
    print(resp.status_code)
    print(resp.json())

def delete_resoure(id):
    data={
        'id':id
    }
    resp=requests.delete(BASE_URI+ENDPOINT,data=json.dumps(data))
    print(resp.status_code)
    print(resp.json())
delete_resoure(11)



































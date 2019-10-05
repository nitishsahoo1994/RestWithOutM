import requests
import json

BASE_URI='http://127.0.0.1:8000/'
ENDPOINT='api/'

def get_resource(id):
    resp=requests.get(BASE_URI+ENDPOINT+id+'/')
    print(resp.status_code)
    print(resp.json())

# id=input('Enter Employee Id:')
# get_resource(id)

def get_all():
    resp=requests.get(BASE_URI+ENDPOINT)
    print(resp.status_code)
    print(resp.json())

# get_all()

def create_resource():
    new_emp={
        'eno':502,
        'ename':'jay Sharma',
        'esal':19.25,
        'eaddr':'Kedarnath',
    }
    resp=requests.post(BASE_URI+ENDPOINT,data=json.dumps(new_emp))
    print(resp.status_code)
    print(resp.json())
create_resource()
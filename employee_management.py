import tornado.ioloop
import tornado.web
from kwikapi.tornado import RequestHandler
from kwikapi import API, Request
from pymongo import MongoClient
from bson import ObjectId

class EmployeesEndpoint(object):
    def create(self, req: Request, first_name: str, last_name: str, email: str, age: int) -> str:
        client = MongoClient()
        db = client.employees_records
        employee = db.employees.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'age': age
            })
        if employee.inserted_id:
            return {'employee_id': str(employee.inserted_id)}
        else:
            return {'error': 'unable to create record'}

    def delete(self, req: Request, employee_id: str) -> str:
        client = MongoClient()
        db = client.employees_records
        deleted_employee = db.employees.delete_one({'_id': ObjectId(employee_id)})
        if deleted_employee.deleted_count == 1:
            return {'message': 'deleted successfully'}
        else:
            return {'error':'unable to delete record'}

    def update(self, req: Request, employee_id:str, first_name: str, last_name: str, email: str, age:int) -> str:
        client = MongoClient()
        db = client.employees_records
        updated_employee = db.employees.update_one({'_id': ObjectId(employee_id)}, {'$set':{
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'age': age
            }})
        if updated_employee.modified_count == 1:
            return {'message': 'record updated successfully'}
        else:
            return {'error': 'unable to update.'}

    def show(self, req: Request, employee_id: str) -> str:
        client = MongoClient()
        db = client.employees_records
        employee = db.employees.find_one({'_id': ObjectId(employee_id)})
        if employee is None:
            return  {'error': 'Employee not found.'}
        else:
            return {
                    'First name': employee['first_name'],
                    'Last name': employee['last_name'],
                    'Email': employee['email'],
                    'Age': employee['age']
                }

api = API()
api.register(EmployeesEndpoint(), 'v1')

def make_app():
    return tornado.web.Application([
        (r'^/api/.*', RequestHandler, dict(api=api))
    ])
if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start() 


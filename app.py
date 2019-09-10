import time

import responder
# from tortoise import Tortoise
from orm import Person
# from marshmallow import Schema, fields

person_schema, person_schemas = None, None

api = responder.API(
    title='Render Test',
    version='1.0.0',
    openapi='3.0.2',
    docs_route='/docs'
)


# @api.on_event('startup')
# async def start_db_connection():
#     global person_schema, person_schemas
#
#     await Tortoise.init(
#         db_url='postgres://oldschool:apple@localhost:5432/tortoise_db_dev',
#         modules={'models': ['orm']}
#     )
#
#     await Tortoise.generate_schemas()
#
#     @api.schema('person_schema')
#     class PersonSchema(Schema):
#         id = fields.Int()
#         first_name = fields.Str()
#         last_name = fields.Str()
#         age = fields.Int()
#
#     person_schema = PersonSchema()
#     person_schemas = PersonSchema(many=True)


# @api.on_event('shutdown')
# async def close_db_connections():
#     await Tortoise.close_connections()


@api.route('/')
def hello_world(req, resp):
    resp.text = 'Hello World!'


@api.route('/hello/{someone}')
def greet_someone(req, resp, someone):
    resp.media = {'hello': someone}


@api.route('/teapot')
def teapot(req, resp):
    resp.status_code = api.status_codes.HTTP_416


@api.route('/divide/{num1}/by/{num2}')
def breaking(req, resp, num1, num2):
    resp.media = {'result': int(num1) / int(num2)}


# Receiving data and background tasks
@api.route('/background-sleep')
class Background:

    @staticmethod
    async def on_post(req, resp):

        @api.background.task
        def dummy_sleep(n: int):
            time.sleep(n)
            print('Done sleeping!!')

        data = await req.media()

        dummy_sleep(data['n'])
        resp.media = {'success': True}

    @staticmethod
    def on_get(req, resp):
        resp.status_code = api.status_codes.HTTP_405
        resp.text = 'Method Not Supported'


@api.route('/add_person/{f_name}/{l_name}/{age}')
async def add_person(req, resp, f_name, l_name, age):
    await Person.create(first_name=f_name, last_name=l_name, age=int(age))
    resp.media = {'success': 'ok'}


@api.route('/all-persons')
async def list_all(req, resp):
    resp.media = person_schemas.dump(await Person.all())


@api.route('/first-person')
async def list_all(req, resp):
    resp.media = person_schema.dump(await Person.first())


@api.route('/person/{identity}/{pkey_val}')
async def person_at_id(req, resp, identity, pkey_val):
    resp.media = person_schema.dump(await Person.filter(first_name=identity).first())


@api.route('/update-user/{id}/{attribute}/{val}')
async def update_person(req, resp, id, attribute, val):
    pass


if __name__ == '__main__':
    api.run()


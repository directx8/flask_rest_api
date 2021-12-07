import os
import json, yaml
from flask import Flask, after_this_request, send_file, safe_join, abort, request
from flask_restx import Resource, Api, fields
from flask_restx.api import Swagger
from py_postgres import PostgresFetcher

# Generate the api template
app = Flask(__name__)
api = Api(
    app=app,
    doc='/docs',
    version='0.0.1',
    default='Test Endpoints',
    default_label='These are the test APIs',
    title='TEST SWAGGER API CREATION',
    description='TEST SWAGGER API CREATION'
    )

# Response field template
response_fields = api.model(
    'Resource', {
    'argument': fields.String(required=True, min_length=1, max_length=200, description='example string')
})

# DB data from local postgres
postgres_data = api.model(
    'Dataset',{
        'id': fields.String(required=True, description='The data id'),
        'first_name': fields.String(required=True, description='The first name'),
        'second_name': fields.String(required=True, description='The second name'),
        'age': fields.String(required=True, description='The age')
    },
)

# This class will handle POST for string inputs
@api.route('/post_demo/', endpoint='post_demo')
@api.doc(responses={403: 'Not Authorized'})
class POST_Demo_String(Resource):
    @api.expect(response_fields, validate=True)
    @api.marshal_with(response_fields, code=200)
    def post(self):
        return request.get_json(force=True)


# This class convert json data for the swagger into a
# yaml swagger document
@api.route('/swagger', endpoint='swagger')
class GET_Swagger_APIs(Resource):
    def get(self):
        data = json.loads(json.dumps(api.__schema__))
        with open('yamldoc.yml', 'w') as yamlf:
            yaml.dump(data, yamlf, allow_unicode=True, default_flow_style=False)
            file = os.path.abspath(os.getcwd())
            try:
                @after_this_request
                def remove_file(resp):
                    try:
                        os.remove(safe_join(file, 'yamldoc.yml'))
                    except Exception as error:
                        print("Error removing or closing downloaded file handle", error)
                    return resp
                return send_file(safe_join(file, 'yamldoc.yml'), as_attachment=True, attachment_filename='yamldoc.yml', mimetype='application/x-yaml')
            except FileExistsError:
                abort(404)

# Get all data items
@api.route('/get_dataset_full', endpoint='get_dataset_full')
@api.response(404, 'No items can be found')
class GET_DATASET_JSON(Resource):
    @api.doc('get all data points')
    def get(self):
        payload = []
        postgres_client = PostgresFetcher()
        for item in postgres_client.get_all_rows():
            payload.append({
                'id':item[0],
                'first_name':item[1],
                'second_name':item[2],
                'age':item[3]
            })
        return payload

# Get an item from a dataset based on id
@api.route('/get_postgres_rows/<rows>', endpoint='get_postgres_rows/<rows>')
@api.param('rows', 'The amount of rows you want to get')
@api.response(404, 'Item cannot be found')
class GET_DATASET_JSON(Resource):
    @api.doc('show number of rows')
    @api.marshal_list_with(postgres_data, code=200)
    def get(self, rows):
        payload = []
        postgres_client = PostgresFetcher()
        for item in postgres_client.get_rows_from_db(int(rows)):
            payload.append({
                'id':item[0],
                'first_name':item[1],
                'second_name':item[2],
                'age':item[3]
            })
        return payload

# main driver function
if __name__ == '__main__':
    app.run(port=5001, debug=True)
 

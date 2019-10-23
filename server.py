#!/usr/bin/python3
from flask import Flask, render_template, abort, redirect
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from flask_swagger_ui import get_swaggerui_blueprint
from json import dumps

db_connect = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ensembl_website_97')
app = Flask(__name__)
api = Api(app)


class Gene(Resource):
    def get(self, gene_name, species_name=None):
        # enforce a minimum length of 3
        if len(gene_name) < 3:
            abort(400)
        
        # connect to database
        conn = db_connect.connect() 
        
        # form SQL command based on inputs
        sql = "SELECT display_label, species, stable_id FROM gene_autocomplete WHERE display_label LIKE :gene"
        if species_name:
            sql += " AND species = '%s'" % species_name
        
        # perform query and return json result
        query = conn.execute(text(sql), gene = gene_name + '%')
        
        # name the fields and return JSON 
        keys = ['name', 'species', 'id'];
        return {'genes': [dict(zip(keys ,i)) for i in query.cursor]}
        
    # ensure 405 error for all other methods
    def post(self, gene_name, species_name=None):
        abort(405)
    def put(self, gene_name, species_name=None):
        abort(405)
    def patch(self, gene_name, species_name=None):
        abort(405)

# point endpoints to relevant class
api.add_resource(Gene, '/gene/<gene_name>', '/gene/<gene_name>/<species_name>')

# redirect non-endpoint URLs to docs
@app.route('/')
def index():
    return redirect('/api/docs');
@app.route('/gene/')
def gene_page():
    return redirect('/api/docs');

# set up SwaggerUI for documentation
swagger_url = '/api/docs'
swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_url,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    'swagger.yml',
    config={'app_name': "Ensembl Flast REST API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True)

#!/usr/bin/python3
from flask import Flask, render_template, abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.sql import text
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

@app.route('/')
def index():
    url = 'http://giphygifs.s3.amazonaws.com/media/LSNqpYqGRqwrS/giphy.gif';
    return render_template('index.html', url=url)

if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True)

#!/usr/bin/python3
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from json import dumps

db_connect = create_engine('mysql://anonymous@ensembldb.ensembl.org:3306/ensembl_website_97')
app = Flask(__name__)
api = Api(app)


class Gene(Resource):
    def get(self, gene_name, species_name=None):
        conn = db_connect.connect() # connect to database
                
        sql = "SELECT display_label, species, stable_id FROM gene_autocomplete WHERE display_label LIKE :gene"
        if species_name:
            sql += " AND species = '%s'" % species_name
        query = conn.execute(text(sql), gene = gene_name + '%') # This line performs query and returns json result
        
        keys = ['name', 'species', 'id'];
        return {genes': [dict(zip(keys ,i)) for i in query.cursor]}

class Hello(Resource):
    def get(self, name, name2=None):
        name_list = [name]
        if name2:
            name_list.append(name2)
        return {'hello': name_list}

api.add_resource(Hello, '/hello/<name>', '/hello/<name>/<name2>')
api.add_resource(Gene, '/gene/<gene_name>', '/gene/<gene_name>/<species_name>')

@app.route('/')
def index():
    url = 'http://giphygifs.s3.amazonaws.com/media/LSNqpYqGRqwrS/giphy.gif';
    return render_template('index.html', url=url)


if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True)

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
    def get(self, gene_name):
        conn = db_connect.connect() # connect to database
        sql = "SELECT display_label, species, stable_id FROM gene_autocomplete WHERE display_label LIKE :gene_name"
        query = conn.execute(text(sql), gene_name = gene_name + '%') # This line performs query and returns json result
        return {'genes': [dict(zip((query.keys()) ,i)) for i in query.cursor]}

class Hello(Resource):
    def get(self, name):
        return {'hello': name}

# api.add_resource(HelloWorld, '/')
api.add_resource(Hello, '/hello/<name>')
api.add_resource(Gene, '/gene/<gene_name>')

@app.route('/')
def index():
    url = 'http://giphygifs.s3.amazonaws.com/media/LSNqpYqGRqwrS/giphy.gif';
    return render_template('index.html', url=url)


if __name__ == '__main__':
     app.run(host="0.0.0.0", debug=True)

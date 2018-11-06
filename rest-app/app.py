from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine

machine_types = ['Small', 'Large', 'Espresso']
flavors = ['vanilla', 'caramel', 'psl', 'mocha', 'hazelnut']

# Create engines for connecting to SQLite3.
m = create_engine('sqlite:///machines.db')
p = create_engine('sqlite:///pods.db')

app = Flask(__name__)
api = Api(app)

class Machines(Resource):
    def get(self, machine_type):
        #Connect to databse
        conn = m.connect()
        #Perform query and return JSON data
        query = conn.execute(f"SELECT {machine_type} FROM machines;")
        return {'Machines': [i[0] for i in query.cursor.fetchall()]}

class PodsByMachine(Resource):
    def get(self, machine_type):
        #Connect to databse
        conn = p.connect()
        #Perform query and return JSON data
        query = conn.execute(f"SELECT {machine_type} FROM pods WHERE {machine_type} IS NOT '';")
        return {'PodsByMachine': [i[0] for i in query.cursor.fetchall()]}

class PodsByFlavorByMachine(Resource):
    def get(self, machine_type, flavor):
        conn = p.connect()
        query = conn.execute(f"SELECT {machine_type} FROM pods WHERE flavor='{flavor}' \
                            AND {machine_type} IS NOT '';")
        result = {'PodsByFlavorByMachine': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class SmallestByMachine(Resource):
    def get(self, machine_type):
        conn = p.connect()
        queries = []
        results = []
        for flavor in flavors:
            query = conn.execute(f"SELECT {machine_type} FROM pods WHERE flavor='{flavor}' \
                                AND {machine_type} IS NOT '' LIMIT 1;")
            queries.append(query)
        for query in queries:
            results.append([dict(zip(tuple (query.keys()) ,i)) for i in query.cursor])
        return {'SmallestByMachine': results}

class SmallestByFlavor(Resource):
    def get(self, flavor):
        conn = p.connect()
        queries = []
        results = []
        for machine in machine_types:
            query = conn.execute(f"SELECT {machine} FROM pods WHERE flavor='{flavor}' \
                                AND {machine} IS NOT '' LIMIT 1;")
            queries.append(query)
        for query in queries:
            results.append([dict(zip(tuple (query.keys()) ,i)) for i in query.cursor])
        return {'SmallestByFlavor': results}


api.add_resource(Machines, '/coffee-machine/<string:machine_type>/')
api.add_resource(PodsByMachine, '/coffee-pods/<string:machine_type>/')
api.add_resource(PodsByFlavorByMachine, '/coffee-pods/<string:machine_type>/<string:flavor>/')
api.add_resource(SmallestByMachine, '/coffee-pods/<string:machine_type>/smallest-by-machine/')
api.add_resource(SmallestByFlavor, '/coffee-pods/<string:flavor>/smallest-by-flavor/')

if __name__ == '__main__':
     app.run(debug=True)

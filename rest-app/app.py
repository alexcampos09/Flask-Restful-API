from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

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
        query = conn.execute(f"SELECT {machine_type} FROM machines")
        return {'Machines': [i[0] for i in query.cursor.fetchall()]}

class Pods(Resource):
    def get(self, machine_type, flavor, smallest=None):
        conn = p.connect()
        query = conn.execute(f"SELECT {machine_type} FROM pods WHERE flavor='{flavor.lower()}'")
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'Pods': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class SmallestPods(Resource):
    def get(self, machine_type):
        if machine_type.lower() == "expresso":
            smallest = 3
        else:
            smallest = 1
        conn = p.connect()
        query = conn.execute(f"SELECT {machine_type} FROM pods WHERE packages='{smallest}'")
        result = {'SmallestPods': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

class SmallestPerFlavor(Resource):
    def get(self, flavor):
        conn = p.connect()

        query = conn.execute(f"SELECT small FROM pods WHERE packages=1 AND \
        flavor='{flavor.lower()}' UNION SELECT large FROM pods WHERE \
        packages=1 AND flavor='{flavor.lower()}' UNION SELECT expresso \
        FROM pods WHERE packages=3 AND flavor='{flavor.lower()}'")

        result = {'SmallestPerFlavor': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result

# localhost:5000/large
api.add_resource(Machines, '/<string:machine_type>')
# localhost:5000/large/caramel
api.add_resource(Pods, '/<string:machine_type>/<string:flavor>')
# localhost:5000/expresso/smallestpods
api.add_resource(SmallestPods, '/<string:machine_type>/smallestpods')
# localhost:5000/vanilla/smallestperflavor
api.add_resource(SmallestPerFlavor, '/<string:flavor>/smallestperflavor')

if __name__ == '__main__':
     app.run(debug=True)

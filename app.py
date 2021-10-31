from flask import Flask
from flask_restful import Resource, Api, reqparse

import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

users_path = './data/users.csv'
locations_path = './data/locations.csv'

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path)
        data = data.to_dict();
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required = True, type = int)
        parser.add_argument('name', required = True)
        parser.add_argument('city', required = True)
        args = parser.parse_args()

        data = pd.read_csv(users_path)

        if args['userId'] in data['userId']:
            return{
                'message': f"'{args['userId']}' already exists."
            }, 401
        else:
            data = data.append({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': [],
            }, ignore_index=True)
            data.to_csv(users_path, index=False)
            return {'data': data.to_dict()}, 200
    
    def delete(self):   
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required = True, type = int)
        args = parser.parse_args() 

        data = pd.read_csv(users_path)

        if args['userId'] in data['userId']:
            data = data[data['userId'] != args['userId']]
            data.to_csv(users_path, index=False)
            return {'data': data.to_dict()}, 200
        else:
            return{'message':f"'{args['userId']}' doesn't exist"
            }, 404

class Locations(Resource):
        pass

api.add_resource(Users, '/users')
api.add_resource(Locations, '/locations')

if __name__ == "__main__":
    app.run()
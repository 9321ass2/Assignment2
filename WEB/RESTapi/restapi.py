
import pymongo
from flask_cors import CORS
from flask import Flask
from flask_restplus import Api

client = pymongo.MongoClient("mongodb+srv://tommy:0000@comp9321-vlfpp.mongodb.net/test?retryWrites=true&w=majority")



app = Flask(__name__)
CORS(app)
api = Api(app, authorizations={
                'API-KEY': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'AUTH-TOKEN'
                }
            },
          security='API-KEY',
          default="",  # Default namespace
          title="COMP9321",  # Documentation Title
          description="Connect to MLAB CLOUD MongoDB ")  # Documentation Description


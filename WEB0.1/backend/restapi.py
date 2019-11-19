
import pymongo
from flask_cors import CORS
from flask import Flask
from flask_restplus import Api
import threading,datetime
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
          title="Restful API for Game Recommendation and Prediction",  # Documentation Title
          description="Connect to Atlas MongoDB ")  # Documentation Description

api_info = {'Date' : str(datetime.datetime.now()),'Recommendation' : 0, 'Prediction' : 0 ,'Data' : 0}


def DataToday():
    global api_info
    api_info = {'Date' : str(datetime.datetime.now()), 'Recommendation' : 0, 'Prediction' : 0 ,'Data' : 0}
    threading.Timer(86400, DataToday).start()



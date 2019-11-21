
import pymongo
from flask_cors import CORS
from flask import Flask
from flask_restplus import Api
import threading,datetime
import pandas as pd
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

api_info = {'Date' : str(datetime.datetime.now()), 'users' : 0,
                'games' : {"2019":0, "populargames":0, "topsales":0, "topscores":0} ,
                'countries' : 0,
                'recommends' : 0,
                'predict': {'esrb':0,'linear':0}
                }



def DataToday():
    global api_info
    api_info = {'Date' : str(datetime.datetime.now()), 'users' : 0,
                'games' : {"2019":0, "populargames":0, "topsales":0, "topscores":0} ,
                'countries' : 0,
                'recommends' : 0,
                'predict': {'esrb':0,'linear':0}
                }

    threading.Timer(86400, DataToday).start()


df = pd.read_csv('./ML/DataSet/KNN.csv')
df.rename(columns={'Rank':'Identifier'},inplace=True)
df.set_index('Identifier', inplace=True)
games_df = df.loc[df['Year'] >= 2019]

country_df = pd.read_csv('./ML/DataSet/sale_country.csv')
country_df.set_index('index', inplace=True)

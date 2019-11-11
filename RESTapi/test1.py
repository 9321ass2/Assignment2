
import pymongo
import codecs
import time
from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from flask_restplus import inputs
from flask_restplus import reqparse
client = pymongo.MongoClient(f"mongodb+srv://TommyLin:5219960@comp9321db-fhxu4.mongodb.net/test?retryWrites=true&w=majority")
db = client.test

app = Flask(__name__)
api = Api(app,
          default="",  # Default namespace
          title="COMP9321",  # Documentation Title
          description="Connect to MLAB CLOUD MongoDB ")  # Documentation Description
if __name__ == '__main__':

    app.run(debug=True)
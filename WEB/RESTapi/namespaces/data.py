from infra.function import *
from infra.models import *
from restapi import api, client, api_info
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from .authentication import requires_auth
from ML.datavisualize import Create_Top3Sales, Create_Popular30

UserDB = client.USER
TokenCollection = UserDB.tokens
FavoriteCollection = UserDB.preference
Data = api.namespace('Data', description=' Data collection')


@Data.route('/topsales', strict_slashes=False)
class TopSales(Resource):
    @Data.response(200, 'Success')
    @Data.doc(description="Generates a top3 selling game")
    def get(self):
        api_info['Data'] += 1
        top3 = Create_Top3Sales()
        return {'top3': top3}, 200


@Data.route('/apiusage', strict_slashes=False)
class APIUsage(Resource):
    @Data.response(200, 'Success')
    @Data.doc(description="Service Usage")
    def get(self):
        api_info['Data'] += 1
        return { 'Date': api_info['Date'],
                'Recommendation': api_info['Recommendation'],
                'Data': api_info['Data'],
                'Prediction': api_info['Prediction']
                }, 200


@Data.route('/populargames', strict_slashes=False)
class Popular30(Resource):
    @Data.response(200, 'Success')
    @Data.doc(description="DataSet of 30 popular games on different platforms")
    def get(self):
        g30 = Create_Popular30()
        return {'s': g30.replace('\"','')}, 200

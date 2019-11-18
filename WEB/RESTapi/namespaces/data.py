from infra.function import *
from infra.models import *
from restapi import api, client
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from .authentication import requires_auth
from ML.datavisualize import Create_Top3Sales
UserDB = client.USER
TokenCollection = UserDB.tokens
FavoriteCollection = UserDB.preference
Data = api.namespace('Data', description=' Data collection')


@Data.route('/topsales', strict_slashes=False)
class TopSales(Resource):
    @Data.response(200, 'Success')
    @Data.doc(description="Generates a top3 selling game")
    def get(self):
        top3 = Create_Top3Sales()
        return {'top3': top3},200

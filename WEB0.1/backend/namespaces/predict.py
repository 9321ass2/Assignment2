from infra.function import *
from infra.models import *
from restapi import api, client
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from .authentication import requires_auth
UserDB = client.USER
TokenCollection = UserDB.tokens
FavoriteCollection = UserDB.preference
predict = api.namespace('predict', description='predict Services')


@predict.route('/linear', strict_slashes=False)
class Prediction(Resource):
    @predict.response(200, 'Success')
    @predict.response(403, 'duplicate document')
    @predict.response(400, 'Wrong Format')
    @predict.expect(Format_Token)
    @requires_auth
    def post(self):
        if not request.json:
            abort(400, 'Wrong Format')
        user = request.json['username']
        query = FavoriteCollection.find_one({"username": user})
        if query is not None:
            abort(403, 'duplicate document')
        FavoriteCollection.insert_one(request.json)
        return {'status': 'ok'}, 200
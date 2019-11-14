from infra.function import *
from infra.models import *
from restapi import api, client
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from ML.recommend import Recommand_Game
from .authentication import requires_auth
user = api.namespace('USER', description='User Information Services')
@user.route('/Recommend', strict_slashes=False)
class Recommend(Resource):
    @user.response(200, 'Success')
    @user.response(403, 'Invalid Auth Token')
    @user.response(400, 'Malformed Request')
    @user.doc(description=''' User info''')
    #@requires_auth
    def get(self):
        df = Recommand_Game()

        return {"gamelist": list(df.columns)},200

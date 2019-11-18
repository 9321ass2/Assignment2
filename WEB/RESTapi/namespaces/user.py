from infra.function import *
from infra.models import *
from restapi import api, client
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from ML.recommend import Recommend_Game
from .authentication import requires_auth
UserDB = client.USER
TokenCollection = UserDB.tokens
FavoriteCollection = UserDB.preference
user = api.namespace('USER', description='User Information Services')

@user.route('/Recommend', strict_slashes=False)
class Recommend(Resource):
    @user.response(200, 'Success')
    @user.response(403, 'User not in TokenCollect')
    @user.response(400, 'Wrong Format')
    @user.response(406, 'User not in PrefCollect')
    @user.doc(description=''' User info''')
    @api.expect(Format_Token)
    @requires_auth
    def get(self):
        token = request.headers['Auth-Token']
        Query_token = TokenCollection.find_one({'token':token},{'username': 1})
        if Query_token is None:
            abort(403,'User not in TokenCollect')
        username = Query_token['username']
        Query_Pref = FavoriteCollection.find_one({'username':username},{'preference':1})
        if Query_Pref is None:
            abort(406,'User not in PrefCollect')
        PreferenceList = [int(element) for element in Query_Pref['preference']]
        print(PreferenceList)
        gamelist = Recommend_Game(PreferenceList)
        return {"games": gamelist},200

    @user.response(200, 'Success')
    @user.response(403, 'User not in PrefCollect')
    @user.response(400, 'Wrong Format')
    @user.response(406, 'Token:User unmatched')
    @api.expect(Format_Token,Format_Recommend)
    @requires_auth
    def put(self):
        if not request.json:
            abort(400, 'Wrong Format')
        token = request.headers['Auth-Token']
        username = request.json['username']
        if not User_Token(username,token):
            abort(406, 'Token:User unmatched')
        preferencelist = request.json['preference']
        query = FavoriteCollection.find_one({"username": username})
        if query is None:
            abort(403, 'User not in PrefCollect')
        FavoriteCollection.update_one({'username': username},{"$set": {"preference": preferencelist}})
        return{'status': 'ok'}, 200

    @user.response(200, 'Success')
    @user.response(403, 'duplicate document')
    @user.response(400, 'Wrong Format')
    @user.response(406, 'Token:User unmatched')
    @api.expect(Format_Token, Format_Recommend)
    @requires_auth
    def post(self):
        if not request.json:
            abort(400, 'Wrong Format')
        token = request.headers['Auth-Token']
        username = request.json['username']
        preferencelist = request.json['preference']
        if not User_Token(username,token):
            abort(406, 'Token:User unmatched')
        query = FavoriteCollection.find_one({"username": username})
        if query is not None:
            abort(403, 'duplicate document')

        FavoriteCollection.insert_one({'username':username,'preference': preferencelist})
        return {'status': 'ok'}, 200



from infra.function import *
from infra.models import *
from restapi import api, client, api_info
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from ML.recommend import Recommend_Game
from .authentication import requires_auth
from bson import ObjectId
import json
from ML.datavisualize import Create_Popular30
UserDB = client.USER
UserCollection = UserDB.data
TokenCollection = UserDB.tokens
FavoriteCollection = UserDB.preference
recom_route = api.namespace('recommends', description='User Information Services')


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@recom_route.route('', strict_slashes=False)
class RecommendsList(Resource):
    @recom_route.response(200, 'Success')
    @recom_route.doc(description=''' get recommendation list of each users ''')
    def get(self):
        ans = FavoriteCollection.find({}, {'_id': 0})
        ret = []
        for doc in ans:
            js = JSONEncoder().encode(doc)
            js = js.replace("\"", '')
            ret.append(js)
            api_info['recommends']['get'] += 1
        return ret

    @recom_route.response(200, 'Success')
    @recom_route.response(403, 'Forbidden')
    @recom_route.response(400, 'Wrong Format')
    @recom_route.response(406, 'Token:User unmatched')
    @recom_route.doc(description=''' create a new recommendation resource''')
    @api.expect(Format_Token, Format_Recommend_POST)
    @requires_auth
    def post(self):
        if not request.json:
            abort(400, 'Wrong Format')
        token = request.headers['Auth-Token']
        username = request.json['username']
        if not User_Token(username, token):
            abort(406, 'Token:User unmatched')
        query = FavoriteCollection.find_one({"username": username})
        if query is not None:
            abort(403, 'duplicate document')
        g30list = Create_Popular30(onlyID=True)
        print(g30list)
        preference_list = []
        for element in request.json['preference']:
            element = int(element)
            if element not in g30list:
                abort(403,'id {} is not in popular 30 games, check /games/populargames'.format(element))
            preference_list.append(element)
        preference_list = list(dict.fromkeys(preference_list))
        if len(preference_list) < 3:
            abort(400, 'games are less than 3')
        game_list = Recommend_Game(preference_list)
        FavoriteCollection.insert_one(
            {'username': username,  'recommendation': game_list})
        api_info['recommends']['post'] += 1
        return {'Message': 'Success'}, 200






@recom_route.route('/<string:username>', strict_slashes=False)
@recom_route.param('username', 'name_of_user')
class Recommend(Resource):
    @recom_route.response(200, 'Success')
    @recom_route.response(404, 'Not Found')
    @recom_route.doc(description=''' get the recommendation of specific user ''')
    @api.expect(Format_Token)
    @requires_auth
    def get(self,username):
        Query_User = UserCollection.find_one({'username': username}, {'_id': 0})
        if Query_User is None:
            abort(404, "Unknown User {} ".format(username))
        Query_Pref = FavoriteCollection.find_one({'username': username}, {'_id': 0})
        if Query_Pref is None:
            abort(404, 'User {} not have preference records')
        api_info['recommends']['get'] += 1
        return Query_Pref

    @recom_route.response(200, 'Success')
    @recom_route.response(403, 'Forbidden')
    @recom_route.response(404, 'Not Found')
    @recom_route.doc(description=''' update the record of specific user''')
    @api.expect(Format_Token, Format_Recommend_PUT)
    @requires_auth
    def put(self, username):
        token = request.headers['Auth-Token']
        if not User_Token(username, token):
            abort(403, 'Token:User unmatched')
        query = FavoriteCollection.find_one({"username": username})
        if query is None:
            abort(404, 'User {} not have preference records')
        preference_list = [int(element) for element in request.json['preference']]
        game_list = Recommend_Game(preference_list)
        FavoriteCollection.update_one({'username': username}, {"$set": {"recommendation": game_list}})
        api_info['recommends']['put'] += 1
        return {'Message': 'User {}\'s record has been updated'}, 200

    @recom_route.response(200, 'Success')
    @recom_route.response(403, 'Forbidden')
    @recom_route.response(404, 'Not Found')
    @recom_route.doc(description=''' delete user from entire system only user himself or admin is permitted''')
    @api.expect(Format_Token)
    @requires_auth
    def delete(self, username):
        query = UserCollection.find_one({'username': username})
        if query is None:
            abort(404, "User {} doesn't exist".format(username))
        token = request.headers['Auth-Token']
        if not User_Token(username, token) and not isAdmin(token):
            abort(403, 'Token:User unmatched')
        FavoriteCollection.delete_one({'username': username})
        api_info['recommends']['delete'] += 1
        return {"Message": "User {} has been deleted in recommendation DB".format(username)}, 200


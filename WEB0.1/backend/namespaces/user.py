from infra.function import *
from infra.models import *
from restapi import api, client,api_info
from flask_restplus import Resource, abort
from flask import request
from .authentication import requires_auth
from bson import ObjectId
import json
UserDB = client.USER
UserCollection = UserDB.data
TokenCollection = UserDB.tokens
FavoriteCollection = UserDB.preference
user_route = api.namespace('users', description='User Information Services')

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@user_route.route('', strict_slashes=False)
class UsersList(Resource):
    @user_route.response(200, 'Success')
    @user_route.doc(description=''' List of Users with email ''')
    @api.expect(Format_Token)
    @requires_auth
    def get(self):

            ans = UserCollection.find({},{'username':1,'email':1,'_id': 0})
            ret = []
            for doc in ans:
                js = JSONEncoder().encode(doc)
                js  = js.replace("\"",'')
                ret.append(js)
            api_info['users']['get'] += 1
            return ret
    @user_route.response(200, 'Success')
    @user_route.response(400, 'Wrong Format')
    @user_route.response(403, 'Duplicate Username')
    @api.expect(Format_Register)
    @user_route.doc(description='''
           Signup to get the membership
        ''')
    def post(self):

        if not request.json:
            abort(400, 'Wrong Format')
        user = str(request.json['username'])
        pwd = str(request.json['password'])
        if user == '' or pwd == '':
            abort(400, 'Wrong Format')
        query = UserCollection.find_one({"username": user})
        if query is not None:
            abort(403, 'Duplicate Username {}'.format(user))
        UserCollection.insert_one(request.json)
        instance = {'username': user, 'token': ''}
        TokenCollection.insert_one(instance)
        api_info['users']['post'] += 1
        return {"Message": "User {} has been successfully created".format(user)}, 200

@user_route.route('/<string:username>', strict_slashes=False)
@user_route.param('username', 'name_of_user')

class User(Resource):
    @user_route.response(200, 'Success')
    @user_route.doc(description=''' get basic info of specific user''')
    @api.expect(Format_Token)
    @requires_auth
    def get(self, username):
        query = UserCollection.find_one({'username':username},{'_id':0,'username':1,'email':1})
        if query is None:
            abort(404, "User {} doesn't exist".format(username))
        api_info['users']['get'] += 1
        return query

    @user_route.response(200, 'Success')
    @user_route.doc(description=''' update the info of user  only user himself or admin is permitted''')
    @api.expect(Format_Token,Format_User_PUT)
    @requires_auth
    def put(self, username):
        query = UserCollection.find_one({'username': username})
        if query is None:
            abort(404, "User {} doesn't exist".format(username))
        token = request.headers['Auth-Token']
        if not User_Token(username, token) and not isAdmin(token):
            abort(403, 'Token:User unmatched')
        email = request.json['email']
        UserCollection.update_one({'username': username}, {"$set": {"email": email}})
        api_info['users']['put'] += 1
        return {"Message": "User {} has been successfully updated".format(username)}, 200

    @user_route.response(200, 'Success')
    @user_route.response(404, 'Not Found')
    @user_route.response(403, 'Forbidden')
    @user_route.doc(description=''' delete user from entire system only admin is permitted''')
    @api.expect(Format_Token)
    @requires_auth
    def delete(self, username):
        if username == 'admin':
            abort(403, 'Admin cant be deleted')
        query = UserCollection.find_one({'username': username})
        if query is None:
            abort(404, "User {} doesn't exist".format(username))
        token = request.headers['Auth-Token']
        if not isAdmin(token):
            abort(403, 'Only Admin can delete resources')
        UserCollection.delete_one({'username':username})
        TokenCollection.delete_one({'username':username})
        FavoriteCollection.delete_one({'username':username})
        api_info['users']['delete'] += 1
        return {"Message": "User {} has been deleted".format(username)}, 200












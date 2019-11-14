from infra.function import *
from infra.models import *
from restapi import api, client
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from .authentication import
user = api.namespace('USER', description='User Information Services')
@user.route('/', strict_slashes=False)
class User(Resource):
    @user.response(200, 'Success', user_details)
    @user.response(403, 'Invalid Auth Token')
    @user.response(400, 'Malformed Request')
    @user.expect(auth_details)
    @user.param('id','Id of user to get information for (defaults to logged in user)')
    @user.param('username','username of user to get information for (defaults to logged in user)')
    @user.doc(description=''' User info''')
    def get(self):
        u = authorize(request)
        u_id = request.args.get('id', None)
        username = request.args.get('username', None)
        # extract information from paramtaters
        if u_id or username:
            try:
                if u_id and db.exists("USER").where(id=u_id):
                    u_id = int(u_id)
                elif username and db.exists("USER").where(username=username):
                    u_id = int(db.select("USER").where(username=username).execute()[0])
                else:
                    abort(400, 'Malformed Request')
            except:
                abort(400, 'Malformed Request')
        else:
            u_id = int(u[0])

        # get information
        u = db.select('USER').where(id=u_id).execute()
        u_username = u[1]

        follow_list = text_list_to_set(u[4])
        posts_raw = db.select_all('POST').where(author=u_username).execute()
        posts = [post[0] for post in posts_raw]
        return {
            'username': u[1],
            'name': u[2],
            'id'  : int(u[0]),
            'email': u[3],
            'following': [int(x) for x in follow_list],
            'followed_num': u[5],
            'posts': posts
        }


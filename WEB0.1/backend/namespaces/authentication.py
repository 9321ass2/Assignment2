from restapi import api, client
from flask_restplus import Resource, abort
from flask import request
from infra.models import *
from infra.function import *
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
from functools import wraps
from time import time

Authen = api.namespace('auth', description='Authentication')
UserDB = client.USER
DataCollection = UserDB.data
TokenCollection = UserDB.tokens


class AuthenticationToken:
    def __init__(self, secret_key, expires_in):
        self.secret_key = secret_key
        self.expires_in = expires_in
        self.serializer = JSONWebSignatureSerializer(secret_key)

    def generate_token(self, username):
        info = {
            'username': username,
            'creation_time': time()
        }

        token = self.serializer.dumps(info)
        return token.decode()

    def validate_token(self, token):
        info = self.serializer.loads(token.encode())

        if time() - info['creation_time'] > self.expires_in:
            raise SignatureExpired("The Token has been expired; get a new token")

        return info['username']


SECRET_KEY = "A SECRET KEY; USUALLY A VERY LONG RANDOM STRING"
expires_in = 6000
auth = AuthenticationToken(SECRET_KEY, expires_in)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get('AUTH-TOKEN')
        if not token:
            abort(401, 'Authentication token is missing')

        try:
            user = auth.validate_token(token)
        except SignatureExpired as e:
            abort(401, e.message)
        except BadSignature as e:
            abort(401, e.message)

        return f(*args, **kwargs)

    return decorated


@Authen.route('/token')
class Token(Resource):
    @Authen.response(200, 'Successful')
    @Authen.response(401,  "authorization has been refused for those credentials.")
    @Authen.doc(description="Generates a authentication token")
    @Authen.expect(Format_Credential1,Format_Credential2)
    def get(self):
        username = request.headers['username']
        password = request.headers['password']
        verification = DataCollection.find_one({"username": username, "password": password})
        if verification is not None:
            token = auth.generate_token(username)
            TokenCollection.update_one({'username': username}, {"$set": {"token": token}})
            return {"token": token}
        return {"message": "authorization has been refused for those credentials."}, 401



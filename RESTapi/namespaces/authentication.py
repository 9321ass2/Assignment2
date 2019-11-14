from restapi import api, client
from flask_restplus import Resource, abort
from flask import request
from infra.models import *
from flask_restplus import reqparse
from itsdangerous import SignatureExpired, JSONWebSignatureSerializer, BadSignature
from functools import wraps
from time import time

Authen = api.namespace('Authen', description='Authentication')
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
expires_in = 600
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


credential_parser = reqparse.RequestParser()
credential_parser.add_argument('username', type=str)
credential_parser.add_argument('password', type=str)


@Authen.route('/token')
class Token(Resource):
    @Authen.response(200, 'Successful')
    @Authen.doc(description="Generates a authentication token")
    @Authen.expect(credential_parser, validate=True)
    def get(self):
        args = credential_parser.parse_args()

        username = args.get('username')
        password = args.get('password')

        verification = DataCollection.find_one({"username": username, "password": password})
        if verification is not None:
            return {"token": auth.generate_token(username)}
        return {"message": "authorization has been refused for those credentials."}, 401


@Authen.route('/register', strict_slashes=False)
class Register(Resource):
    @Authen.response(200, 'Success', Format_Register)
    @Authen.response(400, 'Wrong Format')
    @Authen.response(403, 'Duplicate Username')
    @api.expect(Format_Register)
    @Authen.doc(description='''
           register and get the token
        ''')
    def post(self):
        if not request.json:
            abort(400, 'Wrong Format')
        user = str(request.json['username'])
        pwd = str(request.json['password'])
        if user == '' or pwd == '':
            abort(400, 'Wrong Format')
        query = DataCollection.find_one({"username": user})
        if query is not None:
            abort(403, 'Duplicate Username')
        DataCollection.insert_one(request.json)
        return {"Status": "Success"}, 200

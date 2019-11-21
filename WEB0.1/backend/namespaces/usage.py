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
apiusg_route = api.namespace('apiusages', description='Usage Record Services')

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@apiusg_route.route('', strict_slashes=False)
class UsageList(Resource):
    @apiusg_route.response(200, 'Success')
    @apiusg_route.doc(description=''' List of usage of each service ''')
    @api.expect(Format_Token)
    @requires_auth
    def get(self):
            return api_info

@apiusg_route.route('/<string:service>', strict_slashes=False)
@apiusg_route.param('service', 'name_of_services')
class Usage(Resource):
    @apiusg_route.response(200, 'Success')
    @apiusg_route.doc(description=''' individual usage of each service ''')
    @api.expect(Format_Token)
    @requires_auth
    def get(self,service):
        if service not in api_info.keys():
            abort(404,'service {} doest exist'.format(service))

        return api_info[service]

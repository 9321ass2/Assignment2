from infra.function import *
from infra.models import *
from restapi import api, client,api_info
from flask_restplus import Resource, abort, reqparse, fields
from flask import request
from .authentication import requires_auth
from ML.prediction import ESRB_predict,linear_predict
from ML.datavisualize import *
UserDB = client.USER
TokenCollection = UserDB.tokens
FavoriteCollection = UserDB.preference
predict = api.namespace('predict', description='Predict Services')


@predict.route('/linear', strict_slashes=False)
@api.doc(description="The number predict model use linear regression to predict the possible new game number "
                     "It can base on different background information to predict the new game number ,like in different genre, developers and platforms")
class LinearPrediction(Resource):
    @predict.response(200, 'Success')
    @predict.response(400, 'Invalid')
    @predict.expect(Format_Token,LinearP_parser)
    @requires_auth
    def get(self):
        args = TopSale_parser.parse_args()
        year = args.get('year')
        platform = args.get('platform')
        genre = args.get('genre')
        if year is None:
            year = 2020
        elif year < 2019:
            abort(400, 'invalid input {}'.format(year))
        if genre is not None and genre not in Genre_list:
            abort(400, 'invalid input {}'.format(genre))
        if platform is not None and platform not in Platform_list:
            abort(400, 'invalid input {}'.format(platform))
        ret = linear_predict(Platform=platform,Genre=genre,year=year)
        api_info['predict']['linear'] += 1
        return ret

@predict.route('/esrb', strict_slashes=False)
@api.doc(description="predict ESRB rating")
class ESRBrating(Resource):
    @predict.response(200, 'Success')
    @predict.expect(Format_Token, ESRB_parser)
    @requires_auth
    def get(self):
        args = ESRB_parser.parse_args()
        game_info = args.get('game_information')
        lst = []
        lst.append(game_info)
        ret = ESRB_predict(lst)
        api_info['predict']['esrb'] += 1
        return ret

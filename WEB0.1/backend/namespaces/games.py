
from infra.function import *
from infra.models import *
import json
import numpy as np
from restapi import api, client,api_info,games_df
from flask_restplus import Resource, abort,reqparse
from flask import request
from .authentication import requires_auth
from ML.datavisualize import *

games = api.namespace('games', description='User Information Services')


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

@games.route('/2019', strict_slashes=False)
class GamesList(Resource):
    @games.response(200, 'Success')
    @games.doc(description=''' get the list of games in 2019 ''')
    def get(self):
        json_str = games_df.to_json(orient='index')
        ds = json.loads(json_str)
        ret = []
        for idx in ds:
            game = ds[idx]
            game['Identifier'] = int(idx)
            ret.append(game)
        api_info['games']['get'] += 1
        return ret

    @api.response(200, 'Game Created Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new game with selling info")
    @api.expect(Format_Games_model)
    @requires_auth
    def post(self):
        game= request.json
        if 'Identifier' not in game:
            return {"message": "Missing Identifier"}, 400
        id = game['Identifier']
        if id in games_df.index:
            return {"message": "A Game with Identifier={} is already in the dataset".format(id)}, 400
        for key in game:
            if key not in Format_Games.keys():
                return {"message": "Property {} is invalid".format(key)}, 400
            if int(game['Year']) < 2019:
                return {"message": "please dont input the game before 2016"}, 400
            games_df.loc[id, key] = game[key]
        games_df.append(game, ignore_index=True)
        api_info['games']['post'] += 1
        return {"message": "game {} is created".format(id)}, 201


@games.route('/2019/<int:id>', strict_slashes=False)
@games.param('id', 'identifier of the game')
class Games_2019(Resource):
    @games.response(200, 'Success')
    @games.response(404, 'Cannot be found')
    @games.doc(description=''' get the sale of individual game ''')
    def get(self,id):
        if id not in games_df.index:
            abort(404, "Games {} doesn't exist".format(id))
        game = dict(games_df.loc[id])
        for x in game:
            if x == 'Year':
                game[x] = int(game[x])
            else:
                try:
                    game[x] = float(game[x])
                except:
                    pass
        api_info['games']['get'] += 1
        return game

    @games.response(200, 'Success')
    @games.response(400, 'Invalid')
    @games.doc(description=''' Update the sale of specific game ''')
    @api.expect(Format_Token,Format_Games_model)
    @requires_auth
    def put(self,id):
        if id not in games_df.index:
            abort(404, "game {} doesn't exist".format(id))
        game = request.json
        if 'Identifier' in game and id != game['Identifier']:
            return {"message": "Identifier cannot be changed".format(id)}, 400
        for key in game:
            if key not in Format_Games.keys():
                return {"message": "Property {} is invalid".format(key)}, 400
            if int(game['Year']) < 2019:
                return {"message": "please dont input the game before 2019" }, 400
            games_df.loc[id, key] = game[key]
        games_df.append(game, ignore_index=True)
        api_info['games']['put'] += 1
        return {"message": "Game {} has been successfully updated".format(id)}, 200

    @games.response(200, 'Success')
    @games.response(404, 'Cannot be found')
    @games.response(403,'Forbidden')
    @games.doc(description=''' delete the sale info of specific Game Only admin is permitted''')
    @games.expect(Format_Token)
    @requires_auth
    def delete(self, id):
        token = request.headers['Auth-Token']
        if id not in games_df.index:
            abort(404, "game {} doesn't exist".format(id))
        if not isAdmin(token):
            abort(403, "Only Admin is permitted".format(id))
        games_df.drop(id,inplace=True)
        api_info['games']['delete'] += 1
        return {"message": "Game {} is removed.".format(id)}, 200

    @games.route('/populargames', strict_slashes=False)
    class Popular30(Resource):
        @games.response(200, 'Success')
        @games.doc(description="DataSet of 30 popular games on different platforms")
        def get(self):
            g30 = Create_Popular30()
            api_info['games']['get'] += 1
            return g30

    @games.route('/topsales', strict_slashes=False)
    class Topsales(Resource):
        @games.response(200, 'Success')
        @games.doc(description="        By query with different combination(Genre,Platform,Region,Year),"
                               "Top Sales are provided by this service")
        @api.expect(TopSale_parser)
        def get(self):
            args = TopSale_parser.parse_args()
            year = args.get('year')
            top = args.get('top')
            region = args.get('region')
            genre = args.get('genre')
            platform = args.get('platform')
            if top is None:
                top = 10
            elif top < 1:
                abort(400, 'invalid input {}'.format(top))
            if year is None:
                year = 0
            elif year is not None and year < 1970:
                abort(400, 'invalid input {}'.format(year))
            if genre is not None and genre not in Genre_list:
                abort(400, 'invalid input {}'.format(genre))
            if platform is not None and platform not in Platform_list:
                abort(400, 'invalid input {}'.format(platform))
            if region is None:
                region = 'Global_Sales'
            elif region not in Region_list:
                abort(400, 'invalid input {}'.format(region))
            ret = top_sale_game(top=top, region=region, genre=genre, platform=platform, year=year)
            api_info['games']['get'] += 1
            return ret

        # @games.route('/topscores', strict_slashes=False)
        # class Topscores(Resource):
        #     @games.response(200, 'Success')
        #     @games.doc(description="DataSet of 30 popular games on different platforms")
        #     @api.expect(TopSale_parser)
        #     def get(self):
        #         args = Top10_parser.parse_args()
        #         year = args.get('year')
        #         top = args.get('top')
        #         region = args.get('region')
        #         genre = args.get('genre')
        #         platform = args.get('platform')
        #         if top is None:
        #             top = 10
        #         elif top < 1:
        #             abort(400, 'invalid input {}'.format(top))
        #         if year is None:
        #             year = 0
        #         elif year is not None and year < 1970:
        #             abort(400, 'invalid input {}'.format(year))
        #         if genre is not None and genre not in Genre_list:
        #             abort(400, 'invalid input {}'.format(genre))
        #         if platform is not None and platform not in Platform_list:
        #             abort(400, 'invalid input {}'.format(platform))
        #         if region is None:
        #             region = 'Global_Sales'
        #         elif region not in Region_list:
        #             abort(400, 'invalid input {}'.format(region))
        #         ret = top_sale_game(top=top, region=region, genre=genre, platform=platform, year=year)
        #         api_info['games']['get'] += 1
        #         return ret
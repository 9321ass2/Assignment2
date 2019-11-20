
from infra.function import *
from infra.models import *
import json
import numpy as np
from restapi import api, client,api_info,games_df
from flask_restplus import Resource, abort
from flask import request
from .authentication import requires_auth

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

@games.route('', strict_slashes=False)
class GamesList(Resource):
    @games.response(200, 'Success')
    @games.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
    def get(self):
        json_str = games_df.to_json(orient='index')
        ds = json.loads(json_str)
        ret = []
        for idx in ds:
            game = ds[idx]
            game['Identifier'] = int(idx)
            ret.append(game)
        return ret

    @api.response(201, 'Book Created Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new book")
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
        return {"message": "game {} is created".format(id)}, 201


@games.route('/<int:id>', strict_slashes=False)
@games.param('id', 'The game rank')
class Games(Resource):
    @games.response(200, 'Success')
    @games.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
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
        return  game

    @games.response(200, 'Success')
    @games.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
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
                return {"message": "please dont input the game before 2016" }, 400
            games_df.loc[id, key] = game[key]
        games_df.append(game, ignore_index=True)
        return {"message": "Game {} has been successfully updated".format(id)}, 200

    @games.response(200, 'Success')
    @games.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
    @requires_auth
    def delete(self, id):
        if id not in games_df.index:
            abort(404, "game {} doesn't exist".format(id))
        games_df.drop(id,inplace=True)
        return {"message": "Game {} is removed.".format(id)}, 200

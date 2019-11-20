from infra.function import *
from infra.models import *
import json
from restapi import api, client,api_info,country_df
from flask_restplus import Resource, abort
from flask import request
from .authentication import requires_auth

Countries_route = api.namespace('countries', description='countries sale')


@Countries_route.route('', strict_slashes=False)
class CountriesList(Resource):
    @Countries_route.response(200, 'Success')
    @Countries_route.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
    def get(self):
        json_str = country_df.to_json(orient='index')
        ds = json.loads(json_str)
        ret = []
        for idx in ds:
            country = ds[idx]
            country['Identifier'] = int(idx)
            ret.append(country)
        return ret

    @api.response(201, 'Book Created Successfully')
    @api.response(400, 'Validation Error')
    @api.doc(description="Add a new country")
    @api.expect(Format_Countries_model)
    @requires_auth
    def post(self):
        country= request.json
        if 'Identifier' not in country:
            return {"message": "Missing Identifier"}, 400

        id = country['Identifier']
        if id in country_df.index:
            return {"message": "A country with Identifier={} is already in the dataset".format(id)}, 400

        for key in country:
            if key not in Format_Countries.keys():
                return {"message": "Property {} is invalid".format(key)}, 400
            country_df.loc[id, key] = country[key]
        country_df.append(country, ignore_index=True)
        return {"message": "country {} is created".format(id)}, 201


@Countries_route.route('/<int:id>', strict_slashes=False)
@Countries_route.param('id', 'The country id')
class Countries(Resource):
    @Countries_route.response(200, 'Success')
    @Countries_route.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
    def get(self, id):
        if id not in country_df.index:
            abort(404, "Country {} isn't recorded".format(id))

        country = dict(country_df.loc[id])
        for x in country:
            if x == "Population" or x == "region_population" or x =="Identifier":
                country[x] = int(country[x])
            else:
                try:
                    country[x] = float(country[x])
                except:
                    pass
        return  country

    @Countries_route.response(200, 'Success')
    @Countries_route.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
    # @api.expect(Format_Token,Format_Countries_model)
    # @requires_auth
    def put(self,id):
        if id not in country_df.index:
            abort(404, "Country{} isn't recorded".format(id))
        country = request.json
        if 'Identifier' in country and id != country['Identifier']:
            return {"message": "Identifier cannot be changed".format(id)}, 400
        for key in country:
            if key not in Format_Countries.keys():
                return {"message": "Property {} is invalid".format(key)}, 400
            country_df.loc[id, key] = country[key]
        country_df.append(country, ignore_index=True)
        return {"message": "Country {} has been successfully updated".format(id)}, 200

    @Countries_route.response(200, 'Success')
    @Countries_route.doc(description=''' Get : retrieve the preference from DB then return the recommendation list ''')
    #@requires_auth
    def delete(self, id):
        if id not in country_df.index:
            abort(404, "Country {} isn't recorded".format(id))
        country_df.drop(id,inplace=True)
        return {"message": "Country {} is removed.".format(id)}, 200

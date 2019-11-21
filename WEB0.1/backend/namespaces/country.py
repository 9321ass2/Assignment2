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
    @Countries_route.doc(description=''' get the game sale list in each country ''')
    def get(self):
        json_str = country_df.to_json(orient='index')
        ds = json.loads(json_str)
        ret = []
        for idx in ds:
            country = ds[idx]
            country['Identifier'] = int(idx)
            ret.append(country)
        api_info['countries']['get'] += 1
        return ret

    @Countries_route.response(200, 'Country Created Successfully')
    @Countries_route.response(400, 'Validation Error')
    @Countries_route.doc(description="Add a new country")
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
        api_info['countries']['post'] += 1
        return {"message": "country {} is created".format(id)}, 201


@Countries_route.route('/<int:id>', strict_slashes=False)
@Countries_route.param('id', 'The country id')
class Countries(Resource):
    @Countries_route.response(200, 'Success')
    @Countries_route.response(404, 'Not Found')
    @Countries_route.doc(description=''' get the game sale info in specific country ''')
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
        api_info['countries']['get'] += 1
        return country

    @Countries_route.response(200, 'Success')
    @Countries_route.response(400, 'InValid')
    @Countries_route.response(404, 'Not Found')
    @Countries_route.doc(description=''' update the game sale info of specific country''')
    @api.expect(Format_Token,Format_Countries_model)
    @requires_auth
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
        api_info['countries']['put'] += 1
        return {"message": "Country {} has been successfully updated".format(id)}, 200

    @Countries_route.response(200, 'Success')
    @Countries_route.response(403, 'Forbidden')
    @Countries_route.response(404, 'Not Found')
    @Countries_route.doc(description=''' delete the sale record of specific country Only admin is permitted''')
    @api.expect(Format_Token)
    @requires_auth
    def delete(self, id):
        token = request.headers['Auth-Token']
        if not isAdmin(token):
            abort(403, 'Only Admin can delete resources')
        if id not in country_df.index:
            abort(404, "Country {} isn't recorded".format(id))
        country_df.drop(id,inplace=True)
        api_info['countries']['delete'] += 1
        return {"message": "Country {} is removed.".format(id)}, 200

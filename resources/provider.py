from flask_restful import Resource, reqparse
from models.provider import ProviderModel
from flask import request
import re

path_params = reqparse.RequestParser()
path_params.add_argument('name', type=str)
path_params.add_argument('cnpj', type=str)
path_params.add_argument('city', type=str)


class Providers(Resource):
    def get(self):
        return {'providers': [provider.json() for provider in ProviderModel.query.all()]}


class Provider(Resource):
    attribute = reqparse.RequestParser()
    attribute.add_argument('name', type=str, required=True,
                           help="The attribute is required.")

    attribute.add_argument('city', type=str)

    def get(self, cnpj):
        provider = ProviderModel.find_provider(cnpj)
        if provider:
            return provider.json(), 200
        return {'message': 'Not found'}, 204

    def delete(self, cnpj):
        provider = ProviderModel.find_provider(cnpj)
        if provider:
            provider.delete_provider()
            return {'message': 'Provider deleted.'}, 200
        return {'message': 'Provider not found.'}, 204

    def put(self, cnpj):
        provider_data = Provider.attribute.parse_args()
        provider_found = ProviderModel.find_provider(cnpj)

        if not provider_found:
            return {"message": "Provider CNPJ '{}' does not found.".format(cnpj)}, 204

        provider_found = ProviderModel.find_provider(cnpj)
        if provider_found:
            provider_found.update_provider(**provider_data)
            provider_found.save_provider()
            return provider_found.json(), 200
        provider = ProviderModel(cnpj,  **provider_data )

        try:
            provider.save_provider()
        except:
            return {'message': 'Internal error'}, 500
        return provider.json(), 201


class CreateProvider(Resource):

    def post(self):
        name = request.json['name']
        cnpj = re.sub('[^0-9]', '', request.json['cnpj'])
        city = request.json['city']

        if ProviderModel.find_provider(cnpj):
            return {"message": "CNPJ '{}' already exists.".format(cnpj)}, 400

        if not ProviderModel.validate_cnpj(cnpj):
            return {"message": "CNPJ '{}' is not valid.".format(cnpj)}, 400

        provider = ProviderModel(name, cnpj, city)

        try:
            provider.save_provider()
        except:
            return {"message": "An internal error ocurred trying to create a new provider"}, 500
        return provider.json()

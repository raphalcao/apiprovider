from flask_restful import Resource, reqparse
from models.product import ProductModel
from models.provider import ProviderModel

path_params = reqparse.RequestParser()
path_params.add_argument('name', type=str)
path_params.add_argument('code', type=int)
path_params.add_argument('price', type=float)


class Products(Resource):
    def get(self):
        return {'products': [product.json() for product in ProductModel.query.all()]}


class Product(Resource):
    attribute = reqparse.RequestParser()
    attribute.add_argument('name', type=str, required=True,
                           help="The attribute is required.")
    attribute.add_argument('code', type=int, required=True,
                           help="The attribute is required.")
    attribute.add_argument('price')

    attribute.add_argument('id_provider', type=int, required=True,
                           help="The attribute must be related to the supplier id.")

    def get(self, id_product):
        product = ProductModel.find_product(id_product)
        if product:
            return product.json()
        return {'message': 'Product not found'}, 204

    def put(self, id_product):
        product_data = Product.attribute.parse_args()
        products = ProductModel(**product_data)

        product = ProductModel.find_product(id_product)
        id_provider = ProductModel.find_id_provider(products.id_provider)

        if not id_provider:
            return {"message": "The id '{}' does not found.".format(products.id_provider)}, 404

        if not product:
            return {"message": "Product id '{}' does not found.".format(id_product)}, 404

        product_found = ProductModel.find_product(id_product)
        if product_found:
            product_found.update_product(**product_data)
            product_found.save_product()
            return product_found.json(), 200
        product = ProductModel(id_product, **product_data)

        try:
            product.save_product()
        except:
            return {'message': 'Internal error'}, 500
        return product.json(), 201

    def delete(self, id_product):
        product = ProductModel.find_product(id_product)
        if product:
            try:
                product.delete_product()
            except:
                return {'message': 'Internal error.'}, 500
            return {'message': 'Deleted product.'}, 201
        return {'message': 'Product not found.'}, 204


class CreateProduct(Resource):
    def post(self):

        product_data = Product.attribute.parse_args()
        product = ProductModel(**product_data)

        if not ProviderModel.find_by_id_provider(product.id_provider):
            return {'message': 'The product must be associated with a valid id. '}, 400

        try:
            product.save_product()
        except:
            return {'message': 'Internal error'}, 500
        return product.json(), 200

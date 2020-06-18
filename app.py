from flask import Flask
from flask_restful import Api
from resources.product import Products, Product, CreateProduct
from resources.provider import Providers, Provider, CreateProvider
import pymysql

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:33006/suppliercatalogs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_dbsupcatalogy():
    dbsupcatalogy.create_all()


api.add_resource(Providers, '/', '/providers/', methods=['GET'])
api.add_resource(Provider, '/provider/<int:cnpj>', methods=['GET', 'DELETE', 'PUT'])
api.add_resource(CreateProvider, '/provider/', methods=['POST'])

api.add_resource(Products, '/products/', methods=['GET'])
api.add_resource(Product, '/product/<int:id_product>', methods=['GET', 'DELETE', 'PUT'])
api.add_resource(CreateProduct, '/product/', methods=['POST'])

if __name__ == "__main__":
    from sql_alchemy import dbsupcatalogy

    dbsupcatalogy.init_app(app)
    app.run(debug=True)

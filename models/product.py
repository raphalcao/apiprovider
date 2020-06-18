from sql_alchemy import dbsupcatalogy


class ProductModel(dbsupcatalogy.Model):
    __tablename__ = 'product'

    id_product = dbsupcatalogy.Column(dbsupcatalogy.Integer, primary_key=True)
    name = dbsupcatalogy.Column(dbsupcatalogy.String(80))
    code = dbsupcatalogy.Column(dbsupcatalogy.Integer, nullable=False)
    price = dbsupcatalogy.Column(dbsupcatalogy.Float(precision=2), nullable=False)
    id_provider = dbsupcatalogy.Column(dbsupcatalogy.Integer, dbsupcatalogy.ForeignKey('provider.id_provider'),
                                       nullable=False)

    def __init__(self, name, code, price, id_provider):
        self.name = name
        self.code = code
        self.price = price
        self.id_provider = id_provider

    def json(self):
        return {
            'id_product': self.id_product,
            'name': self.name,
            'code': self.code,
            'price': self.price,
            'id_provider': self.id_provider
        }

    @classmethod
    def find_product(cls, id_product):
        product = cls.query.filter_by(id_product=id_product).first()
        if product:
            return product
        return None

    @classmethod
    def find_id_provider(cls, id_provider):
        product = cls.query.filter_by(id_provider=id_provider).first()
        if product:
            return product
        return None

    def save_product(self):
        dbsupcatalogy.session.add(self)
        dbsupcatalogy.session.commit()

    def update_product(self, name, code, price, id_provider):
        self.name = name
        self.code = code
        self.price = price
        self.id_provider = id_provider

    def delete_product(self):
        dbsupcatalogy.session.delete(self)
        dbsupcatalogy.session.commit()

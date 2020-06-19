from sql_alchemy import dbsupcatalogy
import re


class ProviderModel(dbsupcatalogy.Model):
    __tablename__ = 'provider'

    id_provider = dbsupcatalogy.Column(dbsupcatalogy.Integer, primary_key=True)
    name = dbsupcatalogy.Column(dbsupcatalogy.String(80))
    cnpj = dbsupcatalogy.Column(dbsupcatalogy.String(20))
    city = dbsupcatalogy.Column(dbsupcatalogy.String(20))
    product = dbsupcatalogy.relationship('ProductModel')  

    def __init__(self, name, cnpj, city):
        self.name = name,
        self.cnpj = cnpj,
        self.city = city

    def json(self):
        return {
            'id_provider': self.id_provider,
            'name': self.name,
            'cnpj': self.cnpj,
            'city': self.city,
            'product': [prod.json() for prod in self.product]

        }

    @classmethod
    def find_provider(cls, cnpj):
        provider = cls.query.filter_by(cnpj=cnpj).first()
        if provider:
            return provider
        return None

    @classmethod
    def validate_cnpj(cls, cnpj):

        cnpj = ''.join(re.findall('\d', str(cnpj)))

        if (not cnpj) or (len(cnpj) < 14):
            return False

        integer = list(map(int, cnpj))
        new = integer[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(new) < 14:
            r = sum([x * y for (x, y) in zip(new, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            new.append(f)
            prod.insert(0, 6)

        if new == integer:
            return cnpj
        return False

    @classmethod
    def find_by_id_provider(cls, id_provider):
        provider = cls.query.filter_by(id_provider=id_provider).first()
        if provider:
            return provider
        return None

    def save_provider(self):
        dbsupcatalogy.session.add(self)
        dbsupcatalogy.session.commit()

    def update_provider(self, name, city):
        self.name = name
        self.city = city

    def delete_provider(self):

        [prod.delete_product() for prod in self.product]
        dbsupcatalogy.session.delete(self)
        dbsupcatalogy.session.commit()

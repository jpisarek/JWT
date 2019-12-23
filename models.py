from run import db
from sqlalchemy.orm import relationship

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()  

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    ingredients = db.relationship('IngredientModel', backref='associated_ingredient', lazy='dynamic')
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'name': x.name
            }
        return {'recipes': list(map(lambda x: to_json(x), RecipeModel.query.all()))}

    @property
    def serialize(self):
        return {
            self.name,
        }


class IngredientModel(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String(120), unique = False, nullable = False)
    recipe = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'item': x.item,
                'recipe': x.recipe
            }
        return {'ingredients': list(map(lambda x: to_json(x), IngredientModel.query.all()))}

    @property
    def serialize(self):
        return {
            'item': self.item,
        }
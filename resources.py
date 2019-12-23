from flask_restful import Resource, reqparse
from models import UserModel, RecipeModel, IngredientModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('name', help = 'This field cannot be blank', required = True)

ingredient_parser = reqparse.RequestParser()
ingredient_parser.add_argument('item', help = 'This field cannot be blank', required = True)
ingredient_parser.add_argument('recipe', help = 'This field cannot be blank', required = True)

class RegistrationWithGenerateToken(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}

        new_user = UserModel(
            username = data['username'],
            password = data['password']
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class LoginWithGenerateToken(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if data['password'] == current_user.password:
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}


class CheckIfTokenIsExspiered(Resource):
    @jwt_required
    def get(self):
        return {
            'message': 'Access to the data is possible because JWT Token is actual'
        }


class AllRecipe(Resource):
    def post(self):
        data = recipe_parser.parse_args()
        new_recipe = RecipeModel(
            name = data['name'],
        )
        try:
            new_recipe.save_to_db()
            return {
                'message': 'Recipe {} was created'.format( data['name'])
            }
        except:
            return {'message': 'Something went wrong'}, 500

    # @jwt_required
    def get(self):
        return RecipeModel.return_all()


class AllIngredient(Resource):
    def post(self):
        data = ingredient_parser.parse_args()
        new_ingredient = IngredientModel(
            item = data['item'],
            recipe = data['recipe']
        )
        try:
            new_ingredient.save_to_db()
            return {
                'message': 'Ingredient {} was added'.format( data['item'])
            }
        except:
            return {'message': 'Something went wrong'}, 500

    # @jwt_required
    def get(self):

        recipes = RecipeModel.query.all()
        ingredients = IngredientModel.query.all()
        recipe_to_ingredients = {recipe: list(recipe.ingredients) for recipe in RecipeModel.query.all()}
        for recipe in recipes:
            recipe_to_ingredients[recipe] = []
            for ingredient in ingredients:
                if ingredient.recipe == recipe.id:
                    recipe_to_ingredients[recipe].append(ingredient)
        print(recipe_to_ingredients)
        return jsonify({recipe.name: [y.serialize for y in recipe_to_ingredients[recipe]]})
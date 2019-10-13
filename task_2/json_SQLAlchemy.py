from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sdjdsokjdskdskmdskmos'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/mydatabase'

# Using JSONs and SQLAlchemy

db = SQLAlchemy(app)
nav = Nav(app)
nav.register_element('my_navbar', Navbar(
    'thenav',
    View('Home Page', 'index'),
    View('Recipes', 'recipes'),
    View('Ingredients', 'ingredients')
))

# Models
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    method = db.Column(db.String(500))
    ingredients = db.Column(db.String(500))

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    ingredient = db.Column(db.String(200))

# Routes
@app.route('/')
def index():
    return "hello api"

@app.route('/ingredients', methods=['GET'])
def get_all_ingredients():

    ingredients = Ingredients.query.all()

    if len(ingredients) == 0:
        return jsonify({'ingredients' : "There are no ingredients"})

    output = []

    for ingredient in ingredients:
        ingredient_data = {}
        ingredient_data['id'] = ingredient.id
        ingredient_data['description'] = ingredient.description
        ingredient_data['ingredient'] = ingredient.ingredient
        output.append(ingredient_data)

    return jsonify({'ingredients' : output})

@app.route('/ingredients/<id>', methods=['GET'])
def get_ingredient(id):

    ingredient = Ingredients.query.filter_by(id=id).first()

    if not ingredient:
        return jsonify({'message' : 'No ingredient found!'})

    ingredient_data = {}
    ingredient_data['id'] = ingredient.id
    ingredient_data['description'] = ingredient.description
    ingredient_data['ingredient'] = ingredient.ingredient

    return jsonify({'ingredient' : ingredient_data})

@app.route('/delete_ingredient/<id>', methods=['DELETE'])
def delete_ingredient(id):

    ingredient = Ingredient.query.filter_by(id=id).first()

    if not ingredient:
        return jsonify({'message' : 'No ingredient found!'})

    db.session.delete(ingredient)
    db.session.commit()

    return jsonify({'message' : 'The ingredient has been deleted!'})


@app.route('/recipes', methods=['GET'])
def get_all_recipes():

    recipes = Recipes.query.all()

    if len(recipes) == 0:
        return jsonify({'recipes' : "There are no recipes"})

    output = []

    for recipe in recipes:
        recipe_data = {}
        recipe_data['id'] = recipe.id
        recipe_data['name'] = recipe.name
        recipe_data['method'] = recipe.method
        recipe_data['ingredients'] = recipe.ingredients
        output.append(recipe_data)

    return jsonify({'recipes' : output})

@app.route('/recipes/<id>', methods=['GET'])
def get_recipe(id):

    recipe = Recipes.query.filter_by(id=id).first()

    if not recipe:
        return jsonify({'message' : 'No recipe found!'})

    recipe_data = {}
    recipe_data['id'] = recipe.id
    recipe_data['description'] = recipe.description
    recipe_data['recipe'] = recipe.recipe

    return jsonify({'recipe' : recipe_data})

@app.route('/delete_recipe/<id>', methods=['DELETE'])
def delete_recipe(id):

    recipe = Recipes.query.filter_by(id=id).first()

    if not recipe:
        return jsonify({'message' : 'No recipe found!'})

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({'message' : 'The recipe has been deleted!'})

if __name__ == '__main__':
    app.run(debug=True)
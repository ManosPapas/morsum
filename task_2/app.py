from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

app = Flask(__name__)

app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']       = 'mydatabase'

mysql = MySQL(app)
nav = Nav(app)

nav.register_element('my_navbar', Navbar(
	'thenav',
	View('Home Page', 'index'),
	View('Recipes', 'recipes'),
	View('Ingredients', 'ingredients')
))

@app.route('/')
def index():
	return render_template("index.html", header = "Homepage")

@app.route('/ingredients')
def ingredients():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM ingredients")
	data = cur.fetchall()
	cur.close()

	return render_template("ingredients.html", ingredients = data, header = "Ingredients")

@app.route('/recipes')
def recipes():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM recipes")
	recipes = cur.fetchall()
	cur.execute("SELECT * FROM ingredients")
	ingredients = cur.fetchall()
	cur.close()

	return render_template("recipes.html", recipes = recipes, ingredient_list = ingredients, header = "Recipes")

@app.route('/add_recipes', methods=["POST"])
def add_recipes():
	method      = request.form['method']
	name        = request.form['name']
	ingredients = request.form.getlist('ingredients[]')
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO recipes (name, method, ingredients) VALUES (%s, %s, %s)", (name, method, str(ingredients)))
	cur.execute("SELECT * FROM recipes")
	mysql.connection.commit()
	cur.close()

	return redirect("/recipes")

@app.route('/delete_recipes/<string:id>', methods=["DELETE", "POST"])
def delete_recipes(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM recipes WHERE id = %s", [id])
	cur.execute("SELECT * FROM recipes")
	data = cur.fetchall()
	mysql.connection.commit()
	cur.close()

	return redirect("/recipes")

@app.route('/edit_recipes/<string:id>', methods=["POST"])
def edit_recipes(id):
	name        = request.form['name']
	method      = request.form['method']
	ingredients = request.form.getlist('ingredients[]')
	cur = mysql.connection.cursor()
	cur.execute("UPDATE recipes SET name=%s, method=%s, ingredients=%s WHERE id=%s", [name, method, str(ingredients), id])
	cur.execute("SELECT * FROM recipes")
	data = cur.fetchall()
	mysql.connection.commit()
	cur.close()

	return redirect("/recipes")

@app.route('/add_ingredient', methods=["POST"])
def add_ingredients():
	description      = request.form['description']
	ingredient        = request.form['ingredient']
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO ingredients (description, ingredient) VALUES (%s, %s)", (description, ingredient))
	cur.execute("SELECT * FROM ingredients")
	mysql.connection.commit()
	cur.close()

	return redirect("/ingredients")

@app.route('/delete_ingredient/<string:id>', methods=["DELETE", "POST"])
def delete_ingredients(id):
	cur = mysql.connection.cursor()
	cur.execute("DELETE FROM ingredients WHERE id = %s", [id])
	cur.execute("SELECT * FROM ingredients")
	mysql.connection.commit()
	cur.close()

	return redirect("/ingredients")

@app.route('/edit_ingredient/<string:id>', methods=["POST"])
def edit_ingredients(id):
	description = request.form['description']
	ingredient  = request.form['ingredient']
	cur = mysql.connection.cursor()
	cur.execute("UPDATE ingredients SET description=%s, ingredient=%s WHERE id=%s", [description, ingredient, id])
	cur.execute("SELECT * FROM ingredients")
	data = cur.fetchall()
	mysql.connection.commit()
	cur.close()

	return redirect("/ingredients")

if __name__ == "__main__":
	app.run(debug=True)
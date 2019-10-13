class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    method = db.Column(db.String(500))
    ingredients = db.Column(db.String(500))

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    ingredient = db.Column(db.String(200))
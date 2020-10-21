import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    add_recipes = mongo.db.add_recipes.find()
    return render_template("index.html", add_recipes=add_recipes)


@app.route("/add_recipes", methods=["GET", "POST"])
def add_recipes():
    if request.method == "POST":
        recipe = {
            "author": request.form.get("author"),
            "recipe_name": request.form.get("recipe_name"),
            "image_url": request.form.get("image_url"),
            "description": request.form.get("description"),
            "preptime": request.form.get("preptime"),
            "bakingtime": request.form.get("bakingtime"),
            "serves": request.form.get("serves"),
            "ingredients": request.form.get("ingredients"),
            "method": request.form.get("method")
        }

        mongo.db.add_recipes.insert_one(recipe)
        flash("Recipe Uploaded")
        return redirect(url_for("add_recipes"))
    return render_template("add_recipes.html")


@app.route("/view_more/<recipe_id>")
def view_more(recipe_id):
    recipe = mongo.db.add_recipes.find({'_id': ObjectId(recipe_id)})
    return render_template("view_more.html", recipe=recipe)


@app.route("/update_recipe/<recipe_id>", methods=["GET", "POST"])
def update_recipe(recipe_id):
    recipe = mongo.db.add_recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("update_recipe.html", recipe=recipe)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

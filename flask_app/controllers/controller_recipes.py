from flask_app import app
from flask import Flask, render_template, request,redirect,session
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_recipe


@app.route('/recipes/add', methods =["POST"])          # The "@" decorator associates this route with the function immediately following
def create_recipe():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    is_valid = model_recipe.Recipe.validate_recipe(request.form)

    if not is_valid:
        return redirect("/recipes/new")


    data = {
        "user_id": session["uuid"],
        "name" : request.form["name"],
        "description": request.form["description"],
        "under_30" : request.form["under_30"],
        "instructions" : request.form["instructions"],
        "date_made" : request.form["date_made"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    Recipe.save_recipe(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/dashboard')

@app.route('/recipes/new')
def add_recipe():
    return render_template("new_recipe.html")

@app.route('/recipes/<int:id>')
def show_recipes(id):
    recipes = Recipe.get_one({'id' : id})
    return render_template("show_recipe.html", recipes=recipes,user = User.get_by_id({"id":session["uuid"]}))

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    
    recipes= Recipe.get_one({'id' : id})
    return render_template("edit_recipe.html", recipes=recipes)

@app.route('/recipes/<int:id>/update', methods =['POST'])
def update_recipe(id):
    is_valid = model_recipe.Recipe.validate_recipe(request.form)

    if not is_valid:
        return redirect(f"/recipes/edit/{id}")

    data = {
        **request.form,
        'id' : id
    }
    Recipe.update_one(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/dashboard')

@app.route('/recipes/<int:id>/delete')
def delete_user(id):
    Recipe.delete_one({'id' : id})
    return redirect('/dashboard')
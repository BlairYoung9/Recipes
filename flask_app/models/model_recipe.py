from flask import flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL


class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_30 = data['under_30']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    #Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes').query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod
    def save_recipe(cls, data ):
        query = "INSERT INTO recipes ( name, description, under_30, instructions, date_made,user_id, created_at, updated_at ) VALUES (%(name)s, %(description)s, %(under_30)s, %(instructions)s, %(date_made)s,%(user_id)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL('recipes').query_db(query,data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def update_one(cls, data):
        query = 'UPDATE recipes SET name = %(name)s,description=%(description)s, under_30=%(under_30)s, instructions=%(instructions)s, date_made =%(date_made)s WHERE id = %(id)s'
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL('recipes').query_db(query,data)

    @staticmethod
    def validate_recipe(post_data):
        is_valid = True

        if len(post_data["name"]) < 3:
            flash("name must be at least 3 characters.")
            is_valid = False
        
        if len(post_data["description"]) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False

        if len(post_data["instructions"]) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        
        if len(post_data["date_made"]) < 3:
            flash("Date must be selected.")
            is_valid = False

        return is_valid
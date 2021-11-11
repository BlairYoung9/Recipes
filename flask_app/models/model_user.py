from flask import flash
from flask_bcrypt import Bcrypt
import re
from flask_app import app
from flask_app.models import model_recipe
from flask_app.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)


class  User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes').query_db(query)

        users = []
        for row in results:
            users.append(User(row))

        return users
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL('recipes').query_db(query,data)

        user = cls(results[0])

        for row in results:
            recipe_data = {
                "id" : row['recipes.id'],
                "user_id": row['user_id'],
                "name": row['name'],
                "description" : row['description'],
                "instructions" : row['instructions'],
                "under_30" : row['under_30'],
                "date_made" : row['date_made'],
                'created_at' : row['recipes.created_at'],
                'updated_at' : row['recipes.updated_at']
            }
    
            user.recipes.append(model_recipe.Recipe(recipe_data))
        return user


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query,data)

        if len(results) < 1:
            return False

        return User(results[0]) 

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)

        if len(results) < 1:
            return False

        return User(results[0]) 

    @classmethod
    def create(cls,data):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes').query_db( query, data )

    @staticmethod
    def register_validator(post_data):
        is_valid = True

        if len(post_data["first_name"]) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        
        if len(post_data["last_name"]) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            flash("Invalid Email")
            is_valid = False
        else: 
            user = User.get_by_email({"email": post_data['email']})
            if user:
                flash("Email already in use")
                is_valid = False
        
        if len(post_data["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        
        if post_data["password"] != post_data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False

        return is_valid

    @staticmethod
    def login_validator(post_data):
        user = User.get_by_email({"email": post_data['email']})

        if not user:
            flash("Invalid credentials")
            return False

        if not bcrypt.check_password_hash(user.password, post_data["password"]):
            flash("Invalid credentials")
            return False

        return True

from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re
from flask_bcrypt import Bcrypt
from flask_app.models import plant
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.plants = []
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['firstname']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user['lastname']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash ("Invalid email address.")
            is_valid = False
        elif User.search_for_existing(user):
            flash("Email already registered.")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords must match.")
            is_valid = False
        return is_valid
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO users ( firstname, lastname, email, password, created_at, updated_at ) VALUES ( %(firstname)s , %(lastname)s , %(email)s , %(password)s , NOW() , NOW() );"
        return connectToMySQL('plant_app_schema').query_db( query, data)
    @classmethod
    def get_one( cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('plant_app_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def get_one_by_id( cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL('plant_app_schema').query_db(query, data)
        return cls(result[0])
    @classmethod
    def search_for_existing( cls, data ):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('plant_app_schema').query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return True
    @classmethod
    def get_plants_by_user(cls, data):
        query = "SELECT * FROM users LEFT JOIN plants ON plants.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('plant_app_schema').query_db( query, data )
        user = cls( results[0] )
        for current_position in results:
            plant_data = {
                "id": current_position['plants.id'],
                "name": current_position['name'],
                "sciname": current_position['sciname'],
                "leafshape": current_position['leafshape'],
                "created_at": current_position['plants.created_at'],
                "updated_at": current_position['plants.updated_at']
            }
            user.plants.append( plant.Plant( plant_data ) )
        return user


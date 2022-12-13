from sqlite3 import connect
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re
from flask_bcrypt import Bcrypt
from flask_app.models import user
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Plant:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.sciname = data['sciname']
        self.leafshape = data['leafshape']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
    @staticmethod
    def validate_plant(plant):
        is_valid = True
        if len(plant['name']) < 5:
            flash("Name must be at least 5 characters.")
            is_valid = False
        if len(plant['sciname']) < 5:
            flash("Scientific Name must be at least 5 characters.")
            is_valid = False
        if len(plant['leafshape']) < 1:
            flash("Leaf Shape must be filled in.")
            is_valid = False
        return is_valid
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM plants;"
        results=connectToMySQL('plant_app_schema').query_db(query)
        plants=[]
        for oneplant in results:
            plants.append( cls(oneplant) )
        return plants
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM plants WHERE id = %(id)s;"
        results = connectToMySQL('plant_app_schema').query_db(query, data)
        return cls(results[0])
    @classmethod
    def save( cls, data ):
        query = "INSERT INTO plants ( name, sciname, leafshape, user_id, created_at, updated_at ) VALUES ( %(name)s , %(sciname)s , %(leafshape)s , %(user_id)s , NOW() , NOW() );"
        return connectToMySQL('plant_app_schema').query_db( query, data)
    @classmethod
    def edit(cls, data):
        query = "UPDATE plants SET name = %(name)s, sciname = %(sciname)s, leafshape = %(leafshape)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL('plant_app_schema').query_db(query, data)
        return True
    @classmethod
    def delete(cls, data):
        query = "DELETE from plants WHERE id = %(id)s;"
        connectToMySQL('plant_app_schema').query_db(query, data)
        return
    @classmethod
    def get_all_plants_with_creator(cls):
        query = "SELECT * FROM plants JOIN users ON plants.user_id = users.id;"
        results = connectToMySQL('plant_app_schema').query_db(query)
        all_plants = []
        for one in results:
            one_plant = cls(one)
            one_plants_creator_info = {
                "id": one['users.id'],
                "firstname": one['firstname'],
                "lastname": one['lastname'],
                "email": one['email'],
                "password": one['password'],
                "created_at": one['users.created_at'],
                "updated_at": one['users.updated_at']
            }
            author = user.User(one_plants_creator_info)
            one_plant.creator = author
            all_plants.append(one_plant)
        return all_plants

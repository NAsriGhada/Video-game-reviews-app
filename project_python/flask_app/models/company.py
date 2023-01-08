from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Company:
    db_name = "gamers"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.password = data['password']
        self.is_verified = data['is_verified']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']




   #CRUD
    #REGISTER company
        #CREATE
    @classmethod
    def register_company(cls,data):
        query = "INSERT INTO companies (name,email,password) VALUES(%(name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)      

#READ ONE
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM companies WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])


#GET ONE BY EMAIL
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM companies WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


#GET ALL USERS
    @classmethod
    def get_all_companies(cls):
        query = "SELECT * FROM companies;"
        results = connectToMySQL(cls.db_name).query_db(query)
        companies = []
        for row in results:
            companies.append( cls(row))
        return companies
     

#very Company 
    @classmethod
    def update_company(cls, data):
        query = "UPDATE companies SET is_verified=0 , updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)




#DELETE COMPANY
    @classmethod
    def delete_company(cls,data):
        query = "DELETE FROM companies WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)





     #REGISTER VALIDATION
    @staticmethod
    def validate_register_company(company):
        is_valid = True
        query = "SELECT * FROM companies WHERE email = %(email)s;"
        results = connectToMySQL(Company.db_name).query_db(query,company)
        if len(results) >= 1:
            flash("Email already taken.","register_comp")
            is_valid=False
        if not EMAIL_REGEX.match(company['email']):
            flash("Invalid Email!!!","register_comp")
            is_valid=False
        if len(company['name']) < 3:
            flash(" name must be at least 3 characters","register_comp")
            is_valid= False
        if len(company['password']) < 8:
            flash("Password must be at least 8 characters","register_comp")
            is_valid= False
        if company['password'] != company['confirm']:
            flash("Passwords don't match","register_comp")
            is_valid= False
        return is_valid
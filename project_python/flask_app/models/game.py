from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.review import Review

class Game:
    db_name = "gamers"
    def __init__(self,data):
        self.id = data['id']
        self.company_id = data['company_id']
        self.title = data['title']
        self.description = data['description']
        self.image = data['image']
        self.video = data['video']
        self.avg = 0
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


#CRUD
    
        #CREATE
    @classmethod
    def add_game(cls,data):
        query = "INSERT INTO games (company_id,title,description,image,video) VALUES(%(company_id)s,%(title)s,%(description)s,%(image)s,%(video)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)           



#GET ALL Games
    @classmethod
    def get_all_games(cls, data):
        query = "SELECT * FROM games WHERE company_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        games = []
        for row in results:
            games.append( cls(row))
        return games


    @classmethod
    def get_all_games1(cls):
        query = "SELECT * FROM games;"
        results = connectToMySQL(cls.db_name).query_db(query)
        games = []
        for row in results:
            games.append( cls(row))
        return games

    #READ ONE
    @classmethod
    def get_game_id(cls,data):
        query = "SELECT * FROM games WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])



    @classmethod
    def delete_game(cls,data):
        query = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def update_game(cls,data):
        query = "UPDATE games SET title=%(title)s, description=%(description)s, image=%(image)s, video=%(video)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def avg_review(cls,data):
        query="SELECT AVG(reviews.rate) AS count FROM reviews WHERE reviews.game_id=%(id)s;"
        result=connectToMySQL(cls.db_name).query_db(query,data) 
        if result[0]['count'] == None:
            return 0
        else:
            return int(result[0]['count'])






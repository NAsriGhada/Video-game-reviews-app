from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash




class Review:
    db_name = "gamers"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.content = data['content']
        self.rate = data['rate']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        # self.a = data['count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def add_review(cls,data):
        query = "INSERT INTO reviews (user_id,game_id,content,rate) VALUES(%(user_id)s,%(game_id)s,%(content)s,%(rate)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)     



#GET ALL USERS
    @classmethod
    def get_all_reviews(cls,data):
        query = "SELECT * FROM users JOIN reviews ON users.id=reviews.user_id WHERE reviews.game_id=%(id)s  ORDER BY reviews.created_at;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        reviews = []
        for row in results:
            reviews.append( cls(row))
        return reviews


    #GET AVG REVIEW
  
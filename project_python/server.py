from flask_app import app

#DONT FORGET CONTROLLERS
from flask_app.controllers import users
from flask_app.controllers import companies
from flask_app.controllers import games
if __name__=="__main__":
    app.run(debug=True, port=5012)
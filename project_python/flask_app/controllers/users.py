
from flask import Flask, render_template, request, redirect,session, flash
from flask_app import app
import math
from flask_app.models.company import Company
from flask_app.models.game import Game
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if "user_id" not in session:
        list_games=Game.get_all_games1()
        return render_template('home.html',list_games=list_games)
    else:
        this_user=User.get_by_id({"id":session['user_id']})
        list_games=Game.get_all_games1()
        # avg=Review.avg_review()
    return render_template('home.html',list_games=list_games, this_user=this_user)

@app.route('/games')
def games():
    if "user_id" not in session:
        return redirect('/register_login')
    else:
        this_user=User.get_by_id({"id":session['user_id']})
        list_games = []
        for game in Game.get_all_games1():
            data = {'id':game.id}
            game.avg = game.avg_review(data)
            list_games.append(game)
    return render_template('games_list.html',list_games=list_games, this_user=this_user)



@app.route('/register_login')
def register_login():
    return render_template('register_login.html')





@app.route('/register', methods=['POST'])
def post_register():
    if not User.validate_register(request.form):
        return redirect('/register_login')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.register(data)
    session['user_id'] = id
    
    return redirect('/')    




@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/register_login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/register_login')
    session['user_id'] = user.id
    if user.type_user==0:
        return redirect('/dashboard_admin')
    return redirect('/')



@app.route('/dashboard_admin')
def admin():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    
    this_user=User.get_by_id(data)
    if  this_user.type_user==0:
        return render_template('dashboard_admin.html', this_user = this_user)
    return redirect('/')




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/admin/users')
def list_of_users():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    list_users=User.get_all_users()
    return render_template('users_list.html',list_users=list_users)

@app.route('/admin/users/delete/<int:id>')
def destroy_user(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    User.delete(data)
    return redirect('/admin/users')


@app.route('/admin/comapies')
def list_of_companies():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    list_companies=Company.get_all_companies()
    return render_template('companies_list.html',list_companies=list_companies)




@app.route('/admin/companies/accept/<int:id>')
def accepted_company(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    company=Company.get_by_id({"id":id})
    Company.update_company({"id":id})
    return redirect('/admin/comapies') 



@app.route('/admin/company/delete/<int:id>')
def destroy_company(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Company.delete_company({"id":id})
    return redirect('/admin/comapies')


@app.route('/<int:game_id>/add/review',methods=['POST'])
def add_review(game_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id'],
        'game_id':game_id,
        **request.form
    }
    Review.add_review(data)
    
    return redirect(f'/games/{game_id}')  




@app.route('/games/<int:id>')
def show_game1(id):
    if 'user_id' not in session:
        return redirect('/register_login')
    data = {
            "id":id
        }
    this_game= Game.get_game_id(data)
    list_reviews=Review.get_all_reviews(data)
    this_game.avg = this_game.avg_review(data)
    return render_template('show_game.html',this_game=this_game,list_reviews=list_reviews)



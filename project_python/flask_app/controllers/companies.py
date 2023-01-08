from flask import Flask, render_template, request, redirect,session, flash
from flask_app import app
from flask import flash
from flask_app.models.company import Company
from flask_app.models.game import Game
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/companies/register')
def auth_companies():
   
    return render_template('company_auth.html')



@app.route('/create', methods=['POST'])
def company_register():
    if not Company.validate_register_company(request.form):
        return redirect('/companies/register')
    data ={ 
        "name": request.form['name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Company.register_company(data)
    session['company_id'] = id
    return redirect('/companies/not_verif')    




@app.route('/company/login',methods=['POST'])
def login_company():
    company=Company.get_by_email(request.form)
    if not company:
        flash("Invalid Email","login_comp")
        return redirect('/companies/register')
    if not bcrypt.check_password_hash(company.password, request.form['password']):
        flash("Invalid Password","login_comp")
        return redirect('/companies/register')
    session['company_id'] = company.id
    if company.is_verified==0:
        return redirect('/companies/dashbord')
    return redirect('/companies/not_verif')


@app.route('/companies/not_verif')
def verif_not_companies():
    if 'company_id' not in session :
        return redirect('/')
    data ={
        'id': session['company_id']
    } 

    return render_template('verified_company.html')


@app.route('/companies/dashbord')
def dash_companies():
    if 'company_id' not in session :
        return redirect('/')
    data ={
        'id': session['company_id']
    } 
    list_games= Game.get_all_games(data)
    list_games = []
    for game in Game.get_all_games(data):
        data = {'id':game.id}
        game.avg = game.avg_review(data)
        list_games.append(game)
    return render_template('dashbord_company.html', list_games= list_games)


@app.route('/company/post/delete/<int:id>')
def destroy_post(id):
    if 'company_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Company.delete(data)
    return redirect('/companies/dashbord')


@app.route('/company/games/<int:id>')
def show_game(id):
    if 'company_id' not in session:
        return redirect('/companies/dashbord')
    data = {
            "id":id
        }
    this_game= Game.get_game_id(data)
    list_reviews=Review.get_all_reviews(data)
    this_game.avg = this_game.avg_review(data)

    return render_template('show_game.html',this_game=this_game,list_reviews=list_reviews)
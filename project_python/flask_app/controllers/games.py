from flask import Flask, render_template, request, redirect,session, flash
from flask_app import app
from flask_app.models.company import Company
from flask_app.models.game import Game
from flask_app.models.review import Review




@app.route('/add/games')
def add_game():
    if 'company_id' not in session:
        return redirect('/logout')
    return render_template('add_game.html')


    
@app.route('/add/games/new', methods=['post'])
def create_game():
   if 'company_id' not in session:
       return redirect('/logout')

   Game.add_game(request.form) 
   return redirect('/companies/dashbord')
   


@app.route('/game/delete/<int:id>')
def destroy_game(id):
    if 'company_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Game.delete_game(data)
    return redirect('/companies/dashbord')


# 

   





@app.route('/edit/game/<int:id>')
def edit_game(id):
    if 'company_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    company_data = {
        "id":session['company_id']
    }

    return render_template("edit_game.html",edit=Game.get_game_id(data),company= Company.get_by_id(company_data))

@app.route('/update/game',methods=['POST'])
def update_game():
    if 'company_id' not in session:
        return redirect('/logout')
    # if not Recipe.validate_recipe(request.form):
    #     return redirect('/new/recipe')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "image": request.form["image"],
        "video": request.form["video"],
        "id": request.form['id'],
        "company_id": request.form['company_id']
    }
    Game.update_game(data)
    return redirect('/companies/dashbord')

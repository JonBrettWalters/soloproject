from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.plant import Plant
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route ('/newplant')
def newplantpage():
    if 'user_id' not in session:
        return redirect('/')
    return render_template("newplant.html")
@app.route('/plant/add', methods=['POST'])
def add_plant():
    if not Plant.validate_plant(request.form):
        return redirect('/newplant')
    new_plant_info = {
        "user_id": session['user_id'],
        "name": request.form["name"],
        "sciname": request.form["sciname"],
        "leafshape": request.form["leafshape"]
    }
    Plant.save(new_plant_info)
    return redirect('/')
@app.route('/edit_plant/<int:id>', methods = ['POST'])
def edit_plant(id):
    if not Plant.validate_plant(request.form):
        return redirect(f'/plant/edit/{id}')
    data = {
        "id": id,
        "name": request.form["name"],
        "sciname": request.form["sciname"],
        "leafshape": request.form["leafshape"]
    }
    Plant.edit(data)
    return redirect('/')
@app.route('/plant/edit/<int:id>')
def edit_plant_page(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    one_plant = Plant.get_one(data)
    return render_template('editsighting.html', one_plant = one_plant)
@app.route('/plant/delete/<int:id>')
def delete_plant(id):
    data = {
        'id': id
    }
    Plant.delete(data)
    return redirect('/')
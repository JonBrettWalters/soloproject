from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.plant import Plant
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route('/')
def home():
    return render_template("logandreg.html")
@app.route('/register', methods=['POST'])
def registerfunc():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    user_info = {
        "firstname": request.form["firstname"],
        "lastname": request.form["lastname"],
        "email": request.form["email"],
        "password": pw_hash
    }
    user_id = User.save(user_info)
    session['user_id'] = user_id
    session['user_first'] = request.form['firstname']
    session['user_last'] = request.form['lastname']
    return redirect('/home')
@app.route('/home')
def login_success():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_plants = Plant.get_all_plants_with_creator()
    user_plants = User.get_plants_by_user(data)
    return render_template("home.html", all_plants = all_plants, user_plants = user_plants)
@app.route('/login', methods=['POST'])
def login():
    user_info = {"email": request.form["email"] }
    target_user = User.get_one(user_info)
    if not target_user:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(target_user.password, request.form['password']):
        flash("Email and Password do not match")
        return redirect('/')
    session['user_id'] = target_user.id
    session['user_first'] = target_user.firstname
    session['user_last'] = target_user.lastname
    return redirect('/home')
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


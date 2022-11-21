from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from modules import app
from modules import port as p
from modules.forms import RegisterForm, LoginForm
from modules.models import User
from modules import db


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home_page():
    if request.method == 'POST':
        ip_address = request.form['ip']
        port_range = request.form['pr']
        if ip_address:
            if port_range:
                data = p.port_scanner(ip_address, port_range)
                return render_template("result.html", ip=ip_address, data=data)
            else:
                msg = "Input Port Range"
                return render_template("index.html", msg=msg)
        else:
            msg = "Input IP Address and Port Range"
            return render_template("index.html", msg=msg)

    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account creared, your logged in as: {user_to_create.name}", category="success")


        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error with account creation: {err_msg}", category="danger")

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_pass_correct(attempted_pass=form.password.data):
            login_user(attempted_user)
            flash(f"Success! you are logged in as: {attempted_user.name}", category="success")
            return redirect(url_for('home_page'))
        else:
            flash("Email or password is not correct! Try agaimn.",category="danger")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You've been logged out", category='info')
    return redirect(url_for('login_page'))
from functools import wraps
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .utils import empty, generate_password_from_salt
import flaskr

mod = Blueprint('authentication', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user-type']
        
        if empty(username) or empty(password) or (user_type != "admin" and user_type != "tests_owner"):
            flash("Please fill-in all the fields", "danger")
            
        else:
            if user_type == "admin":
                count = flaskr.database.select("admins", ["id", "password", "salt"], "username='{}'".format(username))
                """ SELECT id, password, salt FROM admins WHERE username=$username
                    count[0][0] = id
                    count[0][1] = password
                    count[0][2] = salt
                """
            else:
                count = flaskr.database.select("test_owners", ["id", "password", "salt", "disabled"], "username='{}'".format(username))
                """ SELECT id, password, salt FROM test_owners WHERE username=$username
                    count[0][0] = id
                    count[0][1] = password
                    count[0][2] = salt
                    count[0][3] = disabled
                """


            if len(count) > 0 and generate_password_from_salt(count[0][2], password) == count[0][1]:
                disabled = 0
                if user_type == "tests_owner":
                    disabled = count[0][3]

                if disabled == 1:
                    flash("This user is disabled by his administrator", "danger")
                else:
                    session['user_id'] = count[0][0]
                    session['user_type'] = user_type

                    return redirect(url_for('search.search'))

            else:
                flash("Wrong username or password", "danger")
            
    return render_template("index.html")


@mod.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop("user_id", None)
    session.pop("user_type", None)
    return redirect(url_for('authentication.login'))


def required_login(func):
    """ Required login decorator
        If the user is not logged in, redirect him to the login page
    """
    @wraps(func)
    def dec(*args, **kwargs):
        if session.get("user_id") is None or session.get('user_type') != "tests_owner":
            return redirect(url_for('authentication.login'))
        return func(*args, **kwargs)
    return dec


def required_admin(func):
    """ Required login (Administrator) decorator
        If the admin is not logged in, redirect him to the login page
    """
    @wraps(func)
    def dec(*args, **kwargs):
        if session.get("user_id") is None or session.get('user_type') != "admin":
            return redirect(url_for('authentication.login'))
        return func(*args, **kwargs)
    return dec


def required_admin_and_user(func):
    """ Required login (Administrator & Test Owner - User -) decorator
        If the admin/user is not logged in, redirect him to the login page
    """
    @wraps(func)
    def dec(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('authentication.login'))
        return func(*args, **kwargs)
    return dec


from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .auth import required_admin_and_user
from .utils import generate_salt, generate_password_from_salt, empty
import flaskr


mod = Blueprint('settings', __name__)


@mod.route('/settings', methods=['GET', 'POST'])
@required_admin_and_user
def settings():
    user_id = session.get("user_id")
    user_type = session.get("user_type")
    if user_type == "admin":
        user_data = flaskr.database.select("admins", ["username", "password", "email", "salt"], "id={}".format(user_id))
        user_data = user_data[0]
        current_username = user_data[0]
        current_email = user_data[2]
        user_table = "admins"
    else:
        user_data = flaskr.database.select("test_owners", ["username", "password", "salt"], "id={}".format(user_id))
        user_data = user_data[0]
        current_username = user_data[0]
        current_email = ""
        user_table = "test_owners"

    """
        Admin:
        user_data[0] = 'username' column
        user_data[1] = 'password' column
        user_data[2] = 'email' column
        user_data[3] = 'salt' column
        User:
        user_data[0] = 'username' column
        user_data[1] = 'password' column
        user_data[2] = 'salt' column        
    """

    if request.method == 'POST':
        username = request.form['username']
        email = request.form.get('email') if user_type == "admin" else ""
        new_password = request.form['new-password']
        re_new_password = request.form['re-new-password']
        current_password = request.form['current-password']


        updated_data = {}
        if not empty(username) and username != user_data[0]:
            #user_data[0] = 'username' column
            updated_data.update({"username": username})

        if not empty(email) and email != user_data[2] and user_type == "admin":
            #user_data[2] = 'email' column
            updated_data.update({"email": email})

        if not empty(new_password) and new_password == re_new_password:
            salt = generate_salt()
            generated_password = generate_password_from_salt(salt, new_password)
            updated_data.update({"password": generated_password, "salt": salt})

        if empty(username) or (empty(email) and user_type == 'admin'):
            flash("Please fill in all the fields", "danger")

        if empty(current_password):
            flash("Please enter your current password to confirm the chages", "danger")

        if len(updated_data) > 0:
            if len(user_data) == 3:
                salt = user_data[2]
            else:
                salt = user_data[3]
            if generate_password_from_salt(salt, current_password) != user_data[1]:
                flash("Your current password is incorrect", "danger")
            else:
                update_query = flaskr.database.update(user_table, updated_data, "id={}".format(user_id))
                if update_query:
                    flash("Your settings have been updated successfully", "success")
                    current_username = username
                    current_email = email

    return render_template("settings.html", current_username=current_username, current_email=current_email, user_type=user_type)

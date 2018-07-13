from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .auth import required_login
from .utils import empty
import flaskr

mod = Blueprint('manage', __name__)


@mod.route("/testing-environments", methods=["POST", "GET"])
@required_login
def testing_environments():

    if request.method == 'POST':
        name = request.form['name']
        platform = request.form['platform']
        description = request.form['description']
        default = request.form.get('default')
        if empty(name) or empty(platform) or empty(description):
            flash("Please fill in all the fields", "danger")
        else:
            existing = flaskr.database.select("testing_environment", ["name"], "name='{}'".format(name))
            if len(existing) > 0:
                flash("This testing environment's name is already existing", "danger")
            else:
                dictionary_of_data = {
                    "test_owner_id": session.get("user_id"),
                    "name": name,
                    "platform": platform,
                    "description": description
                }
                row_id = flaskr.database.insert("testing_environment", dictionary_of_data)
                if row_id:
                    added_text = ""
                    if default:
                        update_data = {"default_testing_environment": row_id}
                        updated = flaskr.database.update("test_owners", update_data, "id={}".format(session.get("user_id")))
                        if updated:
                            added_text = "<br />And it is set as default for this tests owner."
                    flash("This environment has been created successfully" + added_text, "success")

    testing_environments = flaskr.database.select("testing_environment", ["id", "name", "platform"], "test_owner_id={}".format(session.get("user_id")))
    default_testing_environment = flaskr.database.select("test_owners", ["default_testing_environment"], "id={}".format(session.get("user_id")))[0][0]

    return render_template("LIST_NEW_testing_environment.html", testing_environments=testing_environments, default_testing_environment=default_testing_environment)


@mod.route("/testing-environments/edit/<int:id>", methods=["POST", "GET"])
@required_login
def edit_testing_environment(id):

    user_id = session.get("user_id")

    if request.method == 'POST':
        name = request.form['name']
        platform = request.form['platform']
        description = request.form['description']
        default = request.form.get('default')
        if empty(name) or empty(platform) or empty(description):
            flash("Please fill in all the fields", "danger")
        else:
            existing = flaskr.database.select("testing_environment", ["name"], "name='{}'".format(name))
            if len(existing) > 0 and name != existing[0][0]:
                flash("This testing environment's name is already existing", "danger")
            else:
                dictionary_of_data = {
                    "name": name,
                    "platform": platform,
                    "description": description
                }
                row_id = flaskr.database.update("testing_environment", dictionary_of_data, "id={} and test_owner_id={}".format(id, user_id))
                if default:
                    update_data = {"default_testing_environment": id}
                    flaskr.database.update("test_owners", update_data, "id={}".format(session.get("user_id")))
                else:
                    checkIfDefault = flaskr.database.select("test_owners", ["default_testing_environment"], "id={}".format(user_id))[0][0]
                    checkIfDefault = True if checkIfDefault == id else False
                    if checkIfDefault == True:
                        update_data = {"default_testing_environment": 0}
                        flaskr.database.update("test_owners", update_data, "id={}".format(session.get("user_id")))
                if row_id:
                    flash("Your data has been updated successfully", "success")


    data = flaskr.database.select("testing_environment", ["name", "platform", "description"], "id={} and test_owner_id={}".format(id, user_id))
    if len(data) == 0:
        return redirect(url_for("manage.testing_environments"))
    data = data[0]

    default = flaskr.database.select("test_owners", ["default_testing_environment"], "id={}".format(user_id))[0][0]
    default = True if default == id else False

    dictionary_of_data = {
        "name": data[0],
        "platform": data[1],
        "description": data[2],
        "default": default
    }
    return render_template("EDIT_testing_environment.html", data=dictionary_of_data)


@mod.route("/testing-environments/view/<int:id>", methods=["GET"])
@required_login
def view_testing_environment(id):
    user_id = session.get("user_id")
    data = flaskr.database.select("testing_environment", ["name", "platform", "description"], "id={} and test_owner_id={}".format(id, user_id))
    if len(data) == 0:
        return redirect(url_for("manage.testing_environments"))
    data = data[0]
    default = flaskr.database.select("test_owners", ["default_testing_environment"], "id={}".format(user_id))[0][0]
    default = True if default == id else False

    dictionary_of_data = {
        "name": data[0],
        "platform": data[1],
        "description": data[2],
        "default": default
    }
    return render_template("VIEW_testing_environment.html", data=dictionary_of_data)


@mod.route("/testing-environments/default/<int:id>", methods=["GET"])
@required_login
def default_testing_environment(id):
    user_id = session.get("user_id")
    data = flaskr.database.select("testing_environment", ["name", "platform", "description"], "id={} and test_owner_id={}".format(id, user_id))
    if len(data) == 0:
        return redirect(url_for("manage.testing_environments"))
    else:
        data_of_update = {"default_testing_environment": id}
        flaskr.database.update("test_owners", data_of_update, "id={}".format(user_id))
        return redirect(url_for("manage.testing_environments"))
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .auth import required_login
from .utils import allowed_file
from werkzeug.utils import secure_filename
import flaskr
import json
import os

mod = Blueprint('main', __name__)


@mod.route('/', methods=['GET', 'POST'])
def home():
    if session.get("user_id"):
        return redirect(url_for('search.search'))
    else:
        return redirect(url_for('authentication.login'))


@mod.route("/websites", methods=['GET', 'POST'])
def websites():
    websites_data = flaskr.database.select("test_data_websites", ["url", "name"])
    return render_template("test_data_websites.html", websites=websites_data)


@mod.route("/upload", methods=['GET', 'POST'])
@required_login
def upload():

    allowed_extensions = ["db", "xml"]
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'danger')
        else:
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'danger')

            if file and allowed_file(file.filename, allowed_extensions):
                filename = secure_filename(file.filename)
                file.save(os.path.join(flaskr.app.config['UPLOAD_FOLDER'], filename))
                flash(filename, "success")
            else:
                flash("This file's extension is not allowed", "danger")
    testing_environments = flaskr.database.select("testing_environment", ["id", "name", "platform", "description"], "test_owner_id={}".format(session.get("user_id")))
    default = flaskr.database.select("test_owners", ["default_testing_environment"], "id={}".format(session.get("user_id")))
    default = default[0] # Default Testing Environment


    return render_template("upload_xml.html", testing_environments=testing_environments, default_testing_environment=default[0])


@mod.route("/testing-environment/<int:id>", methods=['GET'])
@required_login
def testing_environment(id):
    testing_environment = flaskr.database.select("testing_environment", ["id", "name", "platform", "description"],
                                                  "test_owner_id={} and id={}".format(session.get("user_id"), id))
    return json.dumps(testing_environment[0])
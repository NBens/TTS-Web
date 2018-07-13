from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .auth import required_login
from .utils import empty
import flaskr

mod = Blueprint('search', __name__)


@mod.route('/search', methods=['GET', 'POST'])
@required_login
def search():
    data = ""
    submitted = False
    if request.method == 'POST':
        keyword = request.form.get("keyword")
        category = request.form.get("category")
        test_result = request.form.get("test-result")
        platform = request.form.get("platform")
        os_release = request.form.get("os")
        date = request.form.get("date").replace("/", "-")
        submitted = True

        if empty(keyword):
            flash("Please enter a keyword", "danger")
        else:
            if category == "tp":
                sql_query = """
                SELECT DISTINCT tests.* FROM tests 
                INNER JOIN test_programs on test_programs.absolute_path LIKE '%{}%'
                AND tests.id = test_programs.test_id
                """.format(keyword)

            else:
                if test_result in ['failed', 'skipped', 'expected_failure', 'passed']:
                    if category == "tc":
                        sql_query = """
                        SELECT DISTINCT tests.* FROM tests 
                        INNER JOIN test_cases on test_cases.name LIKE '%{}%' and test_cases.result = '{}'
                        INNER JOIN test_programs on test_cases.test_program_id = test_programs.id
                        AND tests.id = test_programs.test_id
                        """.format(keyword, test_result)
                    elif category == "stderr":
                        sql_query = """
                        SELECT DISTINCT tests.* FROM tests 
                        INNER JOIN files ON files.content LIKE '%{}%' and files.file_type = '__STDERR__'
                        INNER JOIN test_cases on test_cases.id = files.test_case_id and test_cases.result = '{}'
                        INNER JOIN test_programs on test_cases.test_program_id = test_programs.id
                        AND tests.id = test_programs.test_id
                        """.format(keyword, test_result)
                    elif category == "stdout":
                        sql_query = """
                        SELECT DISTINCT tests.* FROM tests 
                        INNER JOIN files ON files.content LIKE '%{}%' and files.file_type = '__STDOUT__'
                        INNER JOIN test_cases on test_cases.id = files.test_case_id and test_cases.result = '{}'
                        INNER JOIN test_programs on test_cases.test_program_id = test_programs.id
                        AND tests.id = test_programs.test_id
                        """.format(keyword, test_result)
                    elif category == "std":
                        sql_query = """
                        SELECT DISTINCT tests.* FROM tests 
                        INNER JOIN files ON files.content LIKE '%{}%'
                        INNER JOIN test_cases on test_cases.id = files.test_case_id and test_cases.result = '{}'
                        INNER JOIN test_programs on test_cases.test_program_id = test_programs.id
                        AND tests.id = test_programs.test_id
                        """.format(keyword, test_result)
                else:
                    flash("Please select a valid test result")

            data = flaskr.database.execute(sql_query).fetchall()
    return render_template("search.html", data=data, submitted=submitted)


# sql_query = """
# SELECT DISTINCT tests.* FROM tests
# INNER JOIN files ON files.content LIKE '%User%'
# INNER JOIN test_cases on files.test_case_id = test_cases.id
# INNER JOIN test_programs on test_cases.test_program_id = test_programs.id
# AND tests.id = test_programs.test_id
# """
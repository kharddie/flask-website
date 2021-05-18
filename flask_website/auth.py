import functools
from os import wait
import time
import datetime
import pdb
import sys
import pprint
import logging
import json

from sqlite3.dbapi2 import Error

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.wrappers import Request
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flask_website.db import get_db
from flask_website.db import get_database_table_details
from flask_website.db import get_db_tables

from flask_website.forms.login_form import LoginForm
from flask_website.forms.register_form import RegisterForm
from flask_website.helper.constants import SELECT_ALL_FROM_USER

bp = Blueprint("auth", __name__, url_prefix="/auth")

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    print(':::: login_required(decorator)')

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            print(':::: g.user is None')
            return redirect(url_for("login"))

        print(':::: g.user =', g.user)
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    # Store in g, applicable for this request and this user only
    g.start_time = time.time()
    # pdb.set_trace()
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    print('::: before_app_request   ----> inside load_logged_in_user()')

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("{} WHERE id = {}".format(
                SELECT_ALL_FROM_USER, user_id)).fetchone()
        )

        print('::: Request for user ====  g.user = ', {g.user})


@bp.teardown_request
def teardown_request(exception=None):
    time_taken = time.time() - g.start_time   # Retrieve from g
    print(time_taken)


@bp.route("/register", methods=("GET", "POST"))
def register():
    _form = RegisterForm()  # Construct an instance of RegisterForm
    error = None

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "Email is required."
        elif (
       
            db.execute("SELECT id, email FROM user WHERE username = ?",(username,)).fetchone() 
            #We access the data from the while loop. When we read the last row, the loop is terminated.
            is not None
        ):
            error = f"User {username} or {email} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), email),
            )

            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html", form=_form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    _form = LoginForm()  # Construct an instance of LoginForm
    error = None

    print('::: before_app_request   ----> inside logging()')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me')
        is_remember = bool(remember_me)
        print('::: request.form[remember_me]   ---->', is_remember)

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['remember'] = is_remember
            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/login.html", form=_form)


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))


@login_required
@bp.route("/users")
def users():
    _tables = get_database_table_details()
    print(f'len(_tables)={len(_tables)} === {_tables}')

    while len(_tables) < 1:
        print('Create JSON')
        
    _data_json = json.dumps(
        _tables, indent=4, separators=(", ", ": "), default = str)

        #pprint.pprint(_data_json)
    print(_data_json)
    

    return render_template("admin/admin.html", tables = _tables)

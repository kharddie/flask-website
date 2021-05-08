import functools 
import pdb
import sys
import pprint

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
from flask_website.forms.login_form import LoginForm




bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    print(':::: login_required(decorator)')

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            print(':::: g.user is None')
            return redirect(url_for("auth/login"))

        print(':::: g.user =',g.user)
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():  
    #pdb.set_trace()
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    #print('This is error output', file=sys.stderr)
    #print('This is standard output', file=sys.stdout)

    print('::: before_app_request   ----> inside load_logged_in_user()')

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )

        print('::: Request for user ====  g.user = ',{g.user})



@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute("SELECT id FROM user WHERE username = ?",
                       (username,)).fetchone()
            is not None
        ):
            error = f"User {username} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            return redirect(url_for("auth/login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods = ("GET", "POST"))
def login():
    _form = LoginForm()  # Construct an instance of LoginForm
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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
            return redirect(url_for('index'))

        flash(error)

    return render_template("auth/wtf_login.html",form = _form)


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))


@bp.route('/wtf_login',methods = ("GET", "POST"))
def wtf_login():
    #pdb.set_trace()
    _form = LoginForm()  # Construct an instance of LoginForm
    error = None

    print('inside wtf_login =',request.method)
    
    if request.method == "POST":
        print('inside ############################################# --- wtf_login')
        pdb.set_trace()
        username = request.form('username')
        password = request.form('password')
        remember_me = request.form["remember_me"]

        pdb.set_trace()
        assert request.form.get('wtf_login') 
        
        print(request.form.get('wtf_login')) 
        
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorect user name or password."
        elif not check_password_hash(user["password"], password):
                error = "Incorrect Password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
            
        flash(error)

    return render_template("auth/wtf_login.html",form = _form)


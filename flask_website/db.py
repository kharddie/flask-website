import sqlite3
from sqlite3.dbapi2 import Error
import click

from flask import current_app
from flask import g

from flask.cli import with_appcontext

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        print("::  Opened database successfully")
        g.db.row_factory = sqlite3.Row
        # row_factory = sqlite3.Row Sets the row_factory to the callable sqlite3.Row, 
        # which converts the plain tuple into a more useful object.

    return g.db


##  This function accepts the connection object and the SELECT query and returns the selected record.

def execute_read_query(connection ,query):
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        #print(type(r))  ### <class 'list'>
        #print(r)  ### [<sqlite3.Row object at 0x7ffab2d77df0>, <sqlite3.Row object at 0x7ffab2d77450>, <sqlite3.Row object at 0x7ffab2d774b0>]
        
        results = [tuple(row) for row in rows]
        print(results)  ### [(1, 'xx', 'xx@xx.com', 'pbkdf2:sha256:150000$voe95VEj$e5d4ca6b1497ab496d30a783363455c2b58122c230fd49fcf2a959857bf82bb4'), (2, 'yy', 'yy@yy.com', 'pbkdf2:sha256:150000$iaL51psF$62ddbc1f1c050c8a1c0afe123b055fbf9aca4d7c40c3fc95a0d987526fb769af'), (3, 'zz', 'zz@zz.com', 'pbkdf2:sha256:150000$1fVxbzNN$ff887d65e7c175eb29fa2fa460b57dd83f1a2ccf5d427a3bf838ec5ab52cf78e')]
        print()

        return results
        
    except Error as e:
        print("The error {:< 30},".format(e))    



def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

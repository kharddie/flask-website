import sqlite3
import click
import pdb
import pprint


from flask import current_app
from flask import flash
from flask import g

from sqlite3.dbapi2 import Error

from flask.cli import with_appcontext

from flask_website.helper.constants import FORMAT_COMMENTS_STRING_HEADER


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # Create a database in RAM
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        print("::  Opened database successfully")
        g.db.row_factory = sqlite3.Row
        # row_factory = sqlite3.Row Sets the row_factory to the callable sqlite3.Row,
        # which converts the plain tuple into a more useful object.
        g.db.row_factory = sqlite3.Row

    return g.db

# This function accepts the connection object and the SELECT query and returns the selected record.


def execute_read_query(connection, query):
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(query)
        # sqlite3 object  == [<sqlite3.Row object at 0x7fcdc2c6e570>, <sqlite3.Row object at 0x7fcdc2c77050>, <sqlite3.Row object at 0x7fcdc2c7
        rows = cursor.fetchall()
        results = [tuple(row) for row in rows]

        print(FORMAT_COMMENTS_STRING_HEADER.format(
            ' RESULTS FROM SELECT QUERY '))
        print(type(results))
        pprint.pprint(results)
        print(FORMAT_COMMENTS_STRING_HEADER.format(
            ' END RESULTS FROM SELECT QUER '))

        return results

    except Error as e:
        print("The error {},".format(e))

"""
def convert_tuple_elements_to_str(tuple_el):
    if type(tuple_el) is tuple:
        (a, b, c, d) = tuple_el
        return [str(a), str(b), str(c), str(d)]

    flash(message='{} is not a tuple. its a ,{}'.format(tuple_el, type(tuple)), category='error')
"""

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

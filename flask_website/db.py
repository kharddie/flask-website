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

def get_db_tables():
    """Returns a set of all database tables names"""
    db = get_db()
    q = "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY 1;"
    try:
        rows = {''.join(tuple(row)) for row in db.execute(q).fetchall()}
        
        if rows:
            print(FORMAT_COMMENTS_STRING_HEADER.format(
                ' RESULTS FROM SELECT QUERY '))
            print(f'>>>>>>>> QUERY={q}')
            print(type(rows))
            pprint.pprint(rows)
            print(FORMAT_COMMENTS_STRING_HEADER.format(
                ' END RESULTS FROM SELECT QUER '))
            return rows
            
        return None

    except Error as e:
        print("The error {},".format(e))

def get_database_table_details():
    """ 
    Returns db tables. table names and rows  if null returns {}
    """
    db = get_db()

    ## Get datatable tables
    try:
        q = "SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ORDER BY 1;"

        db_tables = [''.join(tuple(row)) for row in db.execute(q).fetchall()]
        #pdb.set_trace()
        cursor = db.cursor()  # == false
        db_details = {}  # == false
        temp_dict = {}  # == false

    except Error as e:
        err = f'The error {e},'
        print(err)
        return err

    ## Loop through the no of tables and retreave details 
    for i, t in enumerate(db_tables):

        print(f'::: --- table ---{t}--- i = {i}')

        q = f'SELECT * FROM {t}'

        try:
            table_rows = [tuple(row) for row in cursor.execute(q).fetchall()]
            table_col_names = [(name[0]) for name in cursor.description]

        except Error as e:
            err = f'The error {e},'
            print(err)
            return err

        temp_dict = {"table_name": t ,"col_names": table_col_names ,"table_rows": table_rows}

        print(f"table_name: {t} ,col_names: {table_col_names} ,table_rows: {table_rows}")

        db_details[str(i)] = temp_dict
        temp_dict= {}

    return db_details

    
    

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



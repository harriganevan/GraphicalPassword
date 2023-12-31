from flask import current_app, g
import sqlite3
import click

def get_db():
    #g is a special flask object unique for each request
    #if g does not have a db attribute, it will create it
    if 'db' not in g: 
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))  #execute script in schema.sql

#run 'flask --app app init-db' from the command line to initialize the database
#THIS WILL DELETE ALL ADDED DATABASE CONTENT (ANY REGISTERED USERS WILL BE DELETED)
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


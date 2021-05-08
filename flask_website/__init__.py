import os
import warnings 
import pdb; 

from flask import Flask
from flask.globals import request 


#pdb.set_trace()

def create_app(test_config=None):

    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY = 'xbfu\xdeZn\x94\x8eO\xf2\x13YT\xa1\xca\x1e\x89' , 
        # store the database in the instance folder
        DATABASE =os.path.join(app.instance_path, "flask_website.sqlite"),
        DEBUG = True,
        SEND_FILE_MAX_AGE_DEFAULT = 0,
        TEMPLATES_AUTO_RELOAD = True,
        CACHE_TYPE = 'SimpleCache',
    )
    
    if test_config is None:
        #pdb.set_trace()
        # load the instance config, if it exists, when not testing  eg app.testing = True
        #: Method A: During instantiation of class
        app.config.from_pyfile("config.py", silent=True)
        app.jinja_env.auto_reload = True

    else:
        # load the test config if passed in
       
        app.config.update(
            test_config)

    # ensure the instance folder exists

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    from flask_website import db

    #A number of packages provide an init_app() method. It's a way of constructing an instance of the particular package, then letting it know about the Flask instance (e.g., so that configuration details can be copied)
    db.init_app(app)

    from flask_website import auth, blog

    #pdb.set_trace()
    

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app

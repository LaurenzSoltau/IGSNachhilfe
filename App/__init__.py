import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        # path where the sqlite Database is saved
        DATABASE=os.path.join(app.instance_path, "herbruecke.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in                             
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/test")
    def test():
        return "Hello, World!"

    # import register function and call it to register the functions
    from . import db
    db.init_app(app)

    # register the auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import index
    app.register_blueprint(index.bp)

    from . import post
    app.register_blueprint(post.bp)

    from . import marketplace
    app.register_blueprint(marketplace.bp)
    
    return app


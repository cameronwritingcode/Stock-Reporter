import os

from flask import Flask 

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'src.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import finance
    app.register_blueprint(finance.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/<ticker2>', endpoint='saved')

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import auth
    app.register_blueprint(auth.bp)

    return app



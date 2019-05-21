import os, sentry_sdk

from flask import Flask, g, logging
from flask_wtf.csrf import CSRFProtect

from sentry_sdk.integrations.flask import FlaskIntegration


def create_app(test_config=None):
    sentry_sdk.init(
        dsn="https://fdf6a2e9e8ea4f3086d2d6c40c101703@sentry.io/1365555",
        integrations=[FlaskIntegration()]
    )
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'solar.sqlite3')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    csrf = CSRFProtect()
    csrf.init_app(app)

    @app.context_processor
    def utility_processor():
        def system_info():
            import flask, jinja2
            return [
                {'key': 'flask_version', 'value': flask.__version__},
                {'key': 'jinja2_version', 'value': jinja2.__version__},
            ]
        return dict(system_info=system_info)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import tickets
    app.register_blueprint(tickets.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    from . import profile
    app.register_blueprint(profile.bp)

    app.add_url_rule('/', endpoint='tickets.index')

    return app
    

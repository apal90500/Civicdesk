from flask import Flask
from config.settings import Config
from models import db


from routes.auth_routes import auth_bp
from routes.complaint_routes import complaint_bp
from routes.admin_routes import admin_bp


def create_app():

    app = Flask(__name__)

    
    app.config.from_object(Config)

    
    db.init_app(app)

    
    app.register_blueprint(auth_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(admin_bp)

    
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
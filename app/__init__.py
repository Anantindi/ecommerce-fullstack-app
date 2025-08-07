from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '56e0968a5b5b532f19c871f9a7713cb0a5e1dcf17d1c3d5fcdf8e70486ff8826'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'

    # Flask-Mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'hulkandtheagentsofsmash2@gmail.com'
    app.config['MAIL_PASSWORD'] = 'tmzkiiejjvwjtvvm'
    app.config['MAIL_DEFAULT_SENDER'] = 'hulkandtheagentsofsmash2@gmail.com'

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    from .api_routes import api  # <-- Include this line
    app.register_blueprint(main)
    app.register_blueprint(api)  # <-- And register it

    return app

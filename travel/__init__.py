# import flask module from Flask package
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

#place this outside as it needs to be imported in models.py
db=SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application
def create_app():
    app = Flask(__name__)

    # we use this utility module to display forms quickly
    Bootstrap5(app)

    # A secret key for the session object
    app.secret_key = 'somerandomvalue'

    # Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    # config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
     # initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id==user_id))
    
    # add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    @app.errorhandler(404) 
    # inbuilt function which takes error as parameter 
    def not_found(e): 
      return render_template("404.html", error=e)

    return app
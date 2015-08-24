from flask import Flask      


#http://flask.pocoo.org/docs/0.10/patterns/appfactories/
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    #Init SQLAlchemy
    from app.users.models import db
    db.init_app(app)
    
     

    #Init flask-login
    from app.users.views import login_manager
    login_manager.init_app(app)  
    

    
    
    #Blueprints
    from app.sites.views import sites
    app.register_blueprint(sites, url_prefix='/sites')
    from app.roles.views import roles
    app.register_blueprint(roles, url_prefix='/roles')
    from app.users.views import users
    app.register_blueprint(users, url_prefix='/users')
  

    return app

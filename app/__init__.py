from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Set a secret key for session management and security
    app.config['SECRET_KEY'] = 'fbvas86r89bc68796b897687c6asw8r'
    
    # Import and register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app

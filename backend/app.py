from flask import Flask
from flask_cors import CORS
from models import db
from flask_migrate import Migrate
from routes.auth_routes import auth_bp
from routes.report_summary import report_bp
from routes.project_routes import project_bp
from routes.complaint_routes import complaint_bp
from routes.moderation_callback import moderation_bp
from config import Config

def create_app():
    app = Flask(__name__)
    CORS(app, origins="*")

    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(report_bp, url_prefix='/api')
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(complaint_bp, url_prefix='/api')
    app.register_blueprint(moderation_bp, url_prefix='/api')

    @app.route("/")
    def health():
        return "ok", 200

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

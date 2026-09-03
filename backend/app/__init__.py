from flask import Flask,request
from config import Config

from utils.respones import fail 

from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config.from_object(Config)

    # 配置json_ascii为False
    app.json.ensure_ascii = False

    @app.before_request
    def before_request():
        print(f"[req] {request.method} {request.path}")

    @app.after_request
    def after_request(response):
       response.headers['Content-Type'] = 'application/json'
       return response

    @app.errorhandler(404)
    def not_found(e):
        return fail(msg='not found',http=404)
    
    from .blueprints.Wuhan_Buildings import Wuhan_Buildings_bp
    app.register_blueprint(Wuhan_Buildings_bp)
    from .blueprints.Wuhan_roads import Wuhan_roads_bp
    app.register_blueprint(Wuhan_roads_bp)
    from .blueprints.Wuhan_events import Wuhan_events_bp
    app.register_blueprint(Wuhan_events_bp)

    return app
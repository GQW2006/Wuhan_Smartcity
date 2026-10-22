from .exceptions import APIError, NotFoundError, ConflictError, AuthError

# 注册业务 API Blueprint（flask-smorest 的 Api 统一挂载，附带 OpenAPI 文档）
from ..Wuhan_Buildings import Wuhan_Buildings_bp
from ..Wuhan_events import Wuhan_events_bp
from ..Wuhan_roads import Wuhan_roads_bp


def register_blueprints(api):
    api.register_blueprint(Wuhan_Buildings_bp)
    api.register_blueprint(Wuhan_events_bp)
    api.register_blueprint(Wuhan_roads_bp)


__all__ = ["APIError", "NotFoundError", "ConflictError", "AuthError", "register_blueprints"]

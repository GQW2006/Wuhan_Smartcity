import traceback
import logging
from werkzeug.exceptions import HTTPException

from .exceptions import APIError

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """注册全局错误处理器（必须在 api.init_app(app) 之后调用）"""

    @app.errorhandler(APIError)
    def handle_api_error(e):
        """业务异常 -> 统一错误格式"""
        return {
            "error": {
                "code": e.code,
                "message": e.message,
                "details": e.details,
            }
        }, e.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Werkzeug HTTP 异常（404/405/400 等）统一收口"""
        return {
            "error": {
                "code": e.code,
                "message": e.description,
            }
        }, e.code

    @app.errorhandler(Exception)
    def handle_unhandled(e):
        """兜底：绝不让堆栈泄露给前端"""
        logger.exception("Unhandled exception: %s", traceback.format_exc())
        return {
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "服务器内部错误",
            }
        }, 500
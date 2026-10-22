"""
errors/exceptions.py - 统一业务异常定义
"""


class APIError(Exception):
    """统一业务异常基类"""
    def __init__(self, status_code, code, message, details=None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or []
        super().__init__(message)


class NotFoundError(APIError):
    def __init__(self, resource="资源"):
        super().__init__(404, "NOT_FOUND", f"{resource}不存在")


class ConflictError(APIError):
    def __init__(self, message="资源冲突错误"):
        super().__init__(409, "CONFLICT", message)


class AuthError(APIError):
    def __init__(self, message="需要认证"):
        super().__init__(401, "UNAUTHORIZED", message)

class UnauthorizedError(APIError):
    def __init__(self, message="未授权访问"):
        super().__init__(401, "UNAUTHORIZED", message)

class ForbiddenError(APIError):
    def __init__(self, message="没有权限访问"):
        super().__init__(403, "FORBIDDEN", message)

class ValidationError(APIError):
    def __init__(self, message="参数验证错误"):
        super().__init__(400, "VALIDATION_ERROR", message)

class BusinessError(APIError):
    def __init__(self, message="业务错误"):
        super().__init__(400, "BUSINESS_ERROR", message)

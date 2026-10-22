import os

try:
    from dotenv import load_dotenv
    load_dotenv()          # 有 .env 就加载；没装 python-dotenv 也不影响运行
except ImportError:
    pass

class Config:
    # 驱动必须写 psycopg2：postgresql+psycopg2://用户:密码@主机:端口/库名
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQL_ECHO=1 时终端会打印 ORM 生成的真实 SQL（排查 N+1 最好的方式）
    SQLALCHEMY_ECHO = os.environ.get("SQL_ECHO") == "1"
    # 连接池预检：连接被数据库断开后自动重连，避免长跑服务拿到死连接
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 1800}

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    JSON_ENSURE_ASCII = False

    # flask-smorest 配置（键名必须是 API_*/OPENAPI_*，flask-smorest 通过 app.config 读取）
    API_VERSION = "v1"
    API_TITLE = "GIS Layers API"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/docs"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/"


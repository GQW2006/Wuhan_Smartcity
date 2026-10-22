import os
import sys
from datetime import timedelta

from flask import Flask

# 保证从任何入口导入时，backend 目录内的一级模块（extensions/config/schemas/utils/app）都能被找到
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extensions import db, migrate, api, jwt

from app.blueprints.errors.handlers import register_error_handlers
from app.blueprints.errors import register_blueprints


def create_app(config_object="config.Config"):
    """应用工厂：创建 app、绑定扩展、注册蓝图与错误处理"""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # JWT 配置
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=360)
    # 返回中文不转义、字段顺序保持（Flask 3 用 app.json，替代已移除的 JSON_AS_ASCII）
    app.json.ensure_ascii = False
    app.json.sort_keys = False

    db.init_app(app)
    # compare_type：检测字段类型变化；render_as_batch：让 SQLite 也能改列（PG 下用不到，留着无害）
    migrate.init_app(app, db, compare_type=True, render_as_batch=True)
    api.init_app(app)
    jwt.init_app(app)

    # 注册全局错误处理器
    register_error_handlers(app)

    # 注册 API Blueprint
    register_blueprints(api)

    return app

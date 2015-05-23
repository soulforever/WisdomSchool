# -*- coding: utf-8 -*-
__author__ = 'guti'

# 安全密钥配置
SECRET_KEY = '\xa5\xd6\xa1\xc2\xb6DN\xc2(\n4\xf8\xbc\xa4J[c\x14F\xf9\xc7#)\xcc'

# 缓存配置
CACHE_TYPE = 'simple'

# 数据库配置
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

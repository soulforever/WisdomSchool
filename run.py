#!flask/bin/python
# -*- coding: utf-8 -*-
"""
服务器启动脚本
"""

__author__ = 'guti'


from app import app
if __name__ == '__main__':
    app.run(host=app.config['SERVER_VISION'], port=app.config['SERVER_PORT'])

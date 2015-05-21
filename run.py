#!flask/bin/python
# -*- coding: utf-8 -*-
"""
服务器启动脚本
"""

__author__ = 'guti'


from app import app
app.run(debug=True)
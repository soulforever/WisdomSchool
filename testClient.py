# -*- coding: utf-8 -*-
__author__ = 'guti'

import urllib
import urllib2
import json

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

def getValCode():
    response = opener.open('http://127.0.0.1:5000/ws/api/valcode')
    data = response.read()
    return data


def postCourse(tNum, valCode, semester):
    url = 'http://127.0.0.1:5000/ws/api/teacher'
    values = {'semester': semester, 'teacher_id': tNum, 'val_code': valCode}
    headers = {"Content-Type": "application/json"}
    data = json.dumps(values)
    request = urllib2.Request(url, data, headers)
    response = opener.open(request)
    return response.read()


def postCourse2(tNum, semester):
    url = 'http://127.0.0.1:5000/ws/api/teacher'
    values = {'semester': semester, 'teacher_id': tNum}
    headers = {"Content-Type": "application/json"}
    data = json.dumps(values)
    request = urllib2.Request(url, data, headers)
    response = opener.open(request)
    return response.read()

if __name__ == '__main__':
    f = open('d:/test.jpeg', 'wb')
    f.write(getValCode())
    f.close()
    val_code = raw_input('val_code:')
    print postCourse('0000321', val_code, '20141')
    # print postCourse2('0000063', '20141')
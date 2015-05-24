# -*- coding: utf-8 -*-

"""
视图函数
"""

__author__ = 'guti'

import json
import WSHttp
import time
from app import app, db, cache
from flask import request, abort, jsonify, session
from models import TeacherCourse, CourseInfo, ClassroomInfo


c_dict = dict()

@app.route('/ws/api/valcode')
def getValCode():
    """
    验证码获取视图
    """
    if 'id' not in session:
        tag = time.time()
        session['id'] = tag
        client = c_dict[tag] = WSHttp.WSHttp()
    else:
        client = c_dict[session['id']]
    return client.getValCode()


@cache.cached(timeout=50)
@app.route('/ws/api/teacher', methods=['POST'])
def teacherCourse():
    """
    教师信息获取，无验证码表示从本地查询，带有验证码表示从远端获取
    """
    if not request.json or 'teacher_id' not in request.json:
        abort(404)
    teacher_id = request.json['teacher_id']
    semester = '20141'
    val_code = ''
    if 'val_code' in request.json:
        val_code = request.json['val_code']
    if 'semester' in request.json:
        semester = request.json['semester']
    # 分离查询逻辑
    if val_code == '':
        data = localGetTeacherCourse(teacher_id, semester)
    else:
        data = webGetTeacherCourse(teacher_id, val_code, semester)
        saveTeacherCourseData(teacher_id, semester, data)
    return jsonify(data), 201


def localGetTeacherCourse(teacher_id, semester):
    """
    本地查询教师课程
    """
    print 'localGetTeacherCourse'
    teacher_course = TeacherCourse.query.filter_by(teacher_id=teacher_id, semester=semester).first()
    if teacher_course is None:
        data = {'status': WSHttp.LOCAL_DATA_MISS}
    else:
        data = json.loads(teacher_course.course_data, encoding='utf-8')
    return data


def webGetTeacherCourse(teacher_id, val_code, semester):
    """
    远端获取教师课程数据
    """
    print 'webGetTeacherCourse'
    if 'id' not in session:
        abort(400)
    data = c_dict[session['id']].teacherCourseWrapper(teacher_id, val_code, semester)
    del c_dict[session['id']]
    return data


def saveTeacherCourseData(teacher_id, semester, data):
    """
    保存远端下载的教师课程数据到本地数据库
    """
    print 'saveTeacherCourseData'
    j_data = json.dumps(data)
    teacher_course = TeacherCourse.query.filter_by(teacher_id=teacher_id, semester=semester).first()
    if teacher_course is None:
        teacher_course = TeacherCourse(teacher_id=teacher_id, semester=semester, course_data=j_data)
    else:
        teacher_course.course_data = j_data
    db.session.add(teacher_course)
    db.session.commit()


@cache.cached(timeout=50)
@app.route('/ws/api/course', methods=['POST'])
def courseInfo():
    """
    课程信息获取，无验证码从本地查询，带有验证码从远端获取
    """
    if not request.json or 'course_id' not in request.json:
        abort(404)
    course_id = request.json['course_id']
    semester = '20141'
    val_code = ''
    if 'val_code' in request.json:
        val_code = request.json['val_code']
    if 'semester' in request.json:
        semester = request.json['semester']
    # 分离网络本地查询
    if val_code == '':
        data = localGetCourseIndfo(course_id, semester)
    else:
        data = webGetCourseInfo(course_id, val_code, semester)
        saveCourseInfoData(course_id, semester, data)
    return jsonify(data), 201


def localGetCourseIndfo(course_id, semester):
    """
    本地查询课程信息
    """
    print 'localGetCourseInfo'
    course_info = CourseInfo.query.filter_by(course_id=course_id, semester=semester).first()
    if course_info is None:
        data = {'status': WSHttp.LOCAL_DATA_MISS}
    else:
        data = json.loads(course_info.course_data, encoding='utf-8')
    return data


def webGetCourseInfo(course_id, val_code, semester):
    """
    远端获取课程信息数据
    """
    print 'webGetCourseInfo'
    if 'id' not in session:
        abort(400)
    data = c_dict[session['id']].courseInfoWrapper(course_id, val_code, semester)
    del c_dict[session['id']]
    return data


def saveCourseInfoData(course_id, semester, data):
    """
    保存远端下载的课程信息数据到本地
    """
    print 'saveCourseInfoData'
    j_data = json.dumps(data)
    course_info = CourseInfo.query.filter_by(course_id=course_id, semester=semester).first()
    if course_info is None:
        course_info = CourseInfo(course_id=course_id, semester=semester, course_data=j_data)
    else:
        course_info.course_data = j_data
    db.session.add(course_info)
    db.session.commit()


@cache.cached(timeout=50)
@app.route('/ws/api/classroom', methods=['POST'])
def classroomInfo():
    """
    教室信息获取，无验证码从本地查询，带有验证码从远端获取
    """
    if not request.json or 'room_id' not in request.json:
        abort(404)
    room_id = request.json['room_id']
    semester = '20141'
    val_code = ''
    if 'val_code' in request.json:
        val_code = request.json['val_code']
    if 'semester' in request.json:
        semester = request.json['semester']
    # 分离网络本地查询
    if val_code == '':
        data = localGetClassroomInfo(room_id, semester)
    else:
        data = webGetClassroomInfo(room_id, val_code, semester)
        saveClassroomInfoData(room_id, semester, data)
    return jsonify(data), 201


def localGetClassroomInfo(room_id, semester):
    """
    本地查询教室信息
    """
    print 'localGetClassroomInfo'
    classroom_info = ClassroomInfo.query.filter_by(room_id=room_id, semester=semester).first()
    if classroom_info is None:
        data = {'status': WSHttp.LOCAL_DATA_MISS}
    else:
        data = json.loads(classroom_info.course_data, encoding='utf-8')
    return data


def webGetClassroomInfo(room_id, val_code, semester):
    """
    远端获取教室信息数据
    """
    print 'webGetClassroomInfo'
    if 'id' not in session:
        abort(400)
    print room_id[0], room_id[:2], room_id
    data = c_dict[session['id']].classroomInfoWrapper(room_id[0], room_id[:2], room_id, val_code, semester)
    del c_dict[session['id']]
    return data


def saveClassroomInfoData(room_id, semester, data):
    """
    保存远端下载的教室信息数据到本地
    """
    print 'saveCourseInfoData'
    j_data = json.dumps(data)
    classroom_info = ClassroomInfo.query.filter_by(room_id=room_id, semester=semester).first()
    if classroom_info is None:
        classroom_info = ClassroomInfo(room_id=room_id, semester=semester, course_data=j_data)
    else:
        classroom_info.course_data = j_data
    db.session.add(classroom_info)
    db.session.commit()

@app.errorhandler(404)
def error_404(error):
    return jsonify({'status': 404})


@app.errorhandler(500)
def error_500(error):
    return jsonify({'status': 500})

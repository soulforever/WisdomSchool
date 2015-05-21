# -*- coding: utf-8 -*-
__author__ = 'guti'

from app import db


class TeacherCourse(db.Model):
    teacher_id = db.Column(db.String(15), primary_key=True)
    semester = db.Column(db.String(5))
    course_data = db.Column(db.String(1500))

    def __repr__(self):
        return '<TeacherCourse %r>' % self.teacher_id


class CourseInfo(db.Model):
    course_id = db.Column(db.String(15), primary_key=True)
    semester = db.Column(db.String(5))
    course_data = db.Column(db.String(1500))

    def __repr__(self):
        return '<CourseInfo %r>' % self.course_id

# -*- coding: utf-8 -*-
"""
HTTP请求模块，基本的HTTP请求函数，生成HTTP解析数据
"""

__author__ = 'guti'

import urllib
import urllib2
import cookielib
from lxml import etree

VAL_CODE_INCORRECT = 2000
LOCAL_DATA_MISS = 2001

class WSHttp():
    """
    处理网络数据读取的
    """
    def __init__(self):
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)

    def getValCode(self):
        """
        获取验证码图片数据, 并保存cookie
        :return: str, 验证码图片数据
        """
        response = self.opener.open('http://gl.sycm.com.cn/Jwweb/sys/ValidateCode.aspx')
        data = response.read()
        return data

    def resolveTeacherDict(self):
        """
        获取教师字典，工号为键，姓名为值
        :return: dict
        """
        return self.resolveOptionDict('../Data/Teacher.html')

    def resolveSemesterDict(self):
        """
        获取学年学期字典，数字数据为键，文字标识为值
        :return: dict
        """
        return self.resolveOptionDict('../Data/Semester.html')

    def resolveCourseDict(self):
        """
        解析课程列表
        :return:
        """
        return  self.resolveOptionDict('../Data/Course.html')

    def resolveOptionDict(self, fileName):
        """
        辅助函数，作用域option value格式的html文件，获取value为键，option为值的字典
        :param fileName: 文件名
        :return: dict
        """
        parser = etree.HTMLParser(recover=True, encoding='utf-8')
        root = etree.parse(fileName, parser=parser)
        options = root.findall('//option[@value]')
        result_dict = dict()
        for option in options:
            result_dict[option.attrib['value']] = option.text
        return result_dict

    def postTeacherCourse(self, teacher_id, valCode, semester, type):
        """
        提交post数据，获取教师的课程信息
        :return: str
        """
        url = 'http://gl.sycm.com.cn/Jwweb/ZNPK/TeacherKBFB_rpt.aspx'
        values = {'Sel_XNXQ': semester, 'Sel_JS': teacher_id, 'txt_yzm': valCode, 'type': type}
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
        request.add_header('Referer', 'http://gl.sycm.com.cn/Jwweb/ZNPK/TeacherKBFB.aspx')
        response = self.opener.open(request)
        page = response.read()
        return page.decode('gbk', 'ignore').encode('utf-8')

    def postCourseInfo(self, course_id, valCode, semester, type):
        """
        提交post数据，获取课程信息
        :return: str
        """
        url = 'http://gl.sycm.com.cn/Jwweb/ZNPK/KBFB_LessonSel_rpt.aspx'
        values = {'Sel_XNXQ': semester, 'Sel_KC': course_id, 'txt_yzm': valCode, 'gs': type}
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        request.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
        request.add_header('Referer', 'http://gl.sycm.com.cn/Jwweb/ZNPK/KBFB_LessonSel.aspx')
        response = self.opener.open(request)
        page = response.read()
        return page.decode('gbk', 'ignore').encode('utf-8')

    def isCorrectValCode(self, page):
        if page.find('验证码错误') == -1:
            return True
        else:
            return False

    def resolveCourseTable(self, page):
        """
        解析课程数据，以字典形式返回
        :param page: str, post取得的数据
        :return: dict
        """
        c_dict = dict()
        parser = etree.HTMLParser(recover=True, encoding='utf-8')
        root = etree.fromstring(page, parser=parser)
        # 检查数据是否为空
        t_info_path = root.xpath('/html/body/table/tr/td/table[2]/tr/td')
        course_tab_path = root.xpath('/html/body/table/tr/td/table[3]')
        if not t_info_path and not course_tab_path:
            return c_dict
        # 获取教师个人信息
        t_info = t_info_path[0].text
        c_dict['info'] = t_info.split()
        # 获取教师对应课程表
        course_tab = course_tab_path[0].findall("tr")
        data = list()
        for course in course_tab:
            data.append([c.xpath('./text()') for c in course.getchildren()])
        # 数据格式整理
        data = data[1:]
        data[0] = data[0][1:]
        data[2] = data[2][1:]
        data = [c[1:] for c in data]
        data = zip(*data)
        c_dict['course'] = data
        return c_dict

    def teacherCourseWrapper(self, teacher_id, valCode, semester, type='1'):
        """
        供view视图调用的包装函数，提供教师课程查询的字典数据
        :return: dict
        """
        try:
            page = self.postTeacherCourse(teacher_id, valCode, semester, type)
            if not self.isCorrectValCode(page):
                return {'status': VAL_CODE_INCORRECT}
            return self.resolveCourseTable(page)
        except urllib2.HTTPError, e:
            return {'status': e.code}
        except urllib2.URLError, e:
            return {'status': e.errno}
            pass

    def courseInfoWrapper(self, course_id, valCode, semester, type='1'):
        """
        供view视图调用的包装函数，提供课程信息的查询字典数据
        :return:
        """
        try:
            page = self.postCourseInfo(course_id, valCode, semester, type)
            if not self.isCorrectValCode(page):
                return {'status': VAL_CODE_INCORRECT}
            return self.resolveCourseTable(page)
        except urllib2.HTTPError, e:
            return {'status': e.code}
        except urllib2.URLError, e:
            return {'status': e.errno}
            pass

if __name__ == '__main__':
    client = WSHttp()
    f = open('/home/guti/Downloads/test.jpeg', 'w')
    f.write(client.getValCode())
    f.close()
    val_code = raw_input('val_code:')
    # print client.courseDictWrapper('0000063', val_code, '20141')
    print client.courseInfoWrapper('000003', val_code, '20141')
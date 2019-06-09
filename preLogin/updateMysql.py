import time

from ehallTool import *
import requests, json
from linkMysql import connect


class Update(object):
    def __init__(self, username, password, cookie):
        self.username = username
        self.password = password
        self.cookie = cookie

        self.db = connect.EhallMysql()  # 连接数据库
        self.update_user()  # 更新用户
        terms = self.update_term()  # 更新学期
        self.update_data(terms)  # 更新数据

    # 更新 User 表
    def update_user(self):
        self.db.save_user(self.username, self.password)

    # 更新 Terms 表
    def update_term(self):

        # 成绩查询接口
        url = "http://ehall.ynu.edu.cn/jwapp/sys/cjcx/modules/cjfx/xscjtjcx.do"
        r = requests.post(url, headers=self.cookie, data={'TJLX': '02'})

        if r.status_code == 200:
            data_rows = json.loads(r.text)['datas']['xscjtjcx']['rows']
            terms = []

            for row in data_rows:
                terms.append(row['XNXQDM'])

            # 最后一个为上一学期，2017-2018-2，需要增加本学期
            this_year = time.localtime(time.time())[0]
            if terms[-1][-1] == "2" and terms[-1][-6:-3] != str(this_year):
                terms.append(str(this_year-1) + "-" + str(this_year) + "-1")
            elif terms[-1][-1] == "1" and terms[-1][-6:-3] == str(this_year):
                terms.append(terms[-1][:-2] + "-2")

            self.db.save_term(self.username, terms)

            return terms

    # 更新 Course、Exam、Grades 表
    def update_data(self, terms):

        for term in terms:

            # Course
            courses = Course.get_CourseSchedual(self.cookie, term)
            self.db.save_course(self.username, term, courses)

            # Exam
            exams = Exam.get_ExamSchedual(self.cookie, term)
            self.db.save_exam(self.username, term, exams)

            # Grades
            grades = Grades.get_Grades(self.cookie, term)
            self.db.save_grades(self.username, term, grades)



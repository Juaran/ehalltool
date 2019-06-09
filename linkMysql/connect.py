import pymysql, warnings, json
warnings.filterwarnings("ignore")

from config import *        # 导入数据库连接信息


class EhallMysql(object):
    def __init__(self):
        """ 初始化 """
        self.connect_()  # 连接数据库
        self.db.select_db(DATABASE)  # 选择ehall数据库

    def connect_(self):
        """ 连接数据库 """
        self.db = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, charset='utf8')
        self.cursor = self.db.cursor()

        # 创建数据库
        sql = "CREATE DATABASE IF NOT EXISTS %s" % DATABASE
        self.cursor.execute(sql)

    def check_table(self):
        """ 创建表 """

        # 学号表
        sql = """CREATE TABLE IF NOT EXISTS `User` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `username` char(100) DEFAULT NULL,
              `password` char(100) DEFAULT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8; """

        self.cursor.execute(sql)

        # 课程表
        sql = """CREATE TABLE IF NOT EXISTS `Course` (
              `username` char(100) NOT NULL,
              `term` varchar(255) DEFAULT NULL,
              `courses` varchar(16383) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        self.cursor.execute(sql)

        # 成绩表
        sql = """CREATE TABLE IF NOT EXISTS `Grades` (
                  `username` varchar(255) NOT NULL,
                  `term` varchar(255) DEFAULT NULL,
                  `grades` varchar(16383) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        self.cursor.execute(sql)

        # 考试表
        sql = """CREATE TABLE IF NOT EXISTS `Exam` (
                  `username` varchar(255) NOT NULL,
                  `term` varchar(255) DEFAULT NULL,
                  `exams` varchar(16383) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        self.cursor.execute(sql)

        # 学期表
        sql = """CREATE TABLE IF NOT EXISTS `Terms` (
              `username` varchar(255) NOT NULL,
              `terms` varchar(255) DEFAULT NULL,
              PRIMARY KEY (`username`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        self.cursor.execute(sql)

    """ 检查用户是否在数据库中 """
    def check_in(self, username, password):

        sql = "SELECT * FROM `User` WHERE `username` = %s AND `password` = %s"
        isExists = self.cursor.execute(sql, (username, password))

        return isExists

    """ 保存新用户 """
    def save_user(self, username, password):

        sql = "INSERT INTO `User`(`username`, `password`) VALUES(%s, %s)"
        self.cursor.execute(sql, (username, password))
        self.db.commit()

    """ 保存学期 """
    def save_term(self, username, terms):

        sql = """INSERT INTO `Terms`(`username`, `terms`) VALUES(%s, %s)"""
        self.cursor.execute(sql, (username, str(terms)))
        self.db.commit()

    """ 保存课程 """
    def save_course(self, username, term, courses):

        sql = """INSERT INTO `Course`(`username`, `term`, `courses`) VALUES(%s, %s, %s)"""
        self.cursor.execute(sql, (username, term, str(courses)))
        self.db.commit()

    """ 保存成绩 """
    def save_grades(self, username, term, grades):

        sql = """INSERT INTO `Grades`(`username`, `term`, `grades`) VALUES(%s, %s, %s)"""
        self.cursor.execute(sql, (username, term, str(grades)))
        self.db.commit()

    """ 保存考试 """
    def save_exam(self, username, term, exams):

        sql = """INSERT INTO `Exam`(`username`, `term`, `exams`) VALUES(%s, %s, %s)"""
        self.cursor.execute(sql, (username, term, str(exams)))
        self.db.commit()

    """ 读取课程 """
    def read_course(self, username, term):

        sql = "SELECT `courses` FROM `Course` WHERE `username` = %s AND `term` = %s"
        self.cursor.execute(sql, (username, term))
        try:
            courses = self.cursor.fetchone()[0]
            courses = json.loads(courses.replace("'", '"'))
            return courses

        except TypeError:
            return None

    """ 读取成绩 """
    def read_grades(self, username, term):

        sql = "SELECT `grades` FROM `Grades` WHERE `username` = %s AND `term` = %s"
        self.cursor.execute(sql, (username, term))

        try:
            grades = self.cursor.fetchone()[0]
            grades = json.loads(grades.replace("'", '"'))

            return grades

        except TypeError:
            return None

    """ 读取考试 """
    def read_exam(self, username, term):

        sql = "SELECT `exams` FROM `Exam` WHERE `username` = %s AND `term` = %s"
        self.cursor.execute(sql, (username, term))
        try:
            exams = self.cursor.fetchone()[0]

            if exams != '[]':
                exams = json.loads(exams.replace("'", '"'))
                return exams
            if exams == '[]':
                return None

        except TypeError:
            return None

    """ 读取学期 """
    def read_term(self, username):

        sql = "SELECT `terms` FROM `Terms` WHERE `username` = %s"
        self.cursor.execute(sql, (username))
        terms = self.cursor.fetchone()[0]

        terms = json.loads(terms.replace("'", '"'))

        return terms

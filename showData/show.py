from linkMysql import connect


class Show(object):
    def __init__(self, username):
        self.db = connect.EhallMysql()  # 连接数据库
        self.terms = self.db.read_term(username)
        self.username = username

    def course(self, term):

        courses = self.db.read_course(self.username, term)

        print(courses)

        if courses is None:
            return

        week_day_dict = {
            '1': '星期一',
            '2': '星期二',
            '3': '星期三',
            '4': '星期四',
            '5': '星期五',
            '6': '星期六',
            '7': '星期日',
        }

        int_courses = []
        for course in courses:
            course['weekDay'] = week_day_dict[course['weekDay']]
            # course['startTime'] = int(course['startTime'])
            # course['endTime'] = int(course['endTime'])
            int_courses.append(course)

        return int_courses

    def grades(self, term):
        grades = self.db.read_grades(self.username, term)

        print(grades)

        return grades

    def exam(self, term):
        exams = self.db.read_exam(self.username, term)

        print(exams)

        return exams



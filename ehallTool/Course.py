"""

    获取课表信息

"""

# from main import Cookie

import requests, json, operator


def get_CourseSchedual(cookie, term):
    """ 课表查询API，参数 XNXQDM 为学期 """

    print("获取 {} 课程表信息...".format(term))

    url = "http://ehall.ynu.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do"
    r = requests.post(url, headers=cookie, data={'XNXQDM': term})

    """ 解析json数据重新封装，排序 """
    if r.status_code == 200:

        data_rows = json.loads(r.text)['datas']['xskcb']['rows']
        courses = []

        for row in data_rows:
            course = {}

            course['name'] = row['KCM']  # 课程名称
            course['teacher'] = row['SKJS']  # 授课老师
            course['weekDay'] = row['SKXQ']  # 星期几
            course['startTime'] = row['KSJC']  # 第几节课开始
            course['endTime'] = row['JSJC']  # 第几节课结束
            course['classRoom'] = row['JASMC']  # 教室
            course['weeks'] = row['ZCMC']  # 上课周数

            if course['classRoom'] is None:
                course['classRoom'] = "暂无上课地点"
            if course['teacher'] is None:
                course['teacher'] = "暂无上课上课教师"

            courses.append(course)

        """ 按上课时间排序 """
        courses = sorted(courses, key=operator.itemgetter('weekDay', 'startTime'))

        return courses


def print_CourseSchedual(courses, term):
    """ 终端输出显示 """

    print("=" * 50)
    if term.split('-')[2] == '1':
        title = "我的课表 " + term.split('-')[1] + "年 春季学期"
        print(title.center(50))
    elif term.split('-')[2] == '2':
        title = "我的课表 " + term.split('-')[1] + "年 秋季学期"
        print(title.center(50))
    print("=" * 50)

    week_day_dict = {
        '1': '星期一',
        '2': '星期二',
        '3': '星期三',
        '4': '星期四',
        '5': '星期五',
        '6': '星期六',
        '7': '星期日',
    }

    for course in courses:

        print("| " + week_day_dict[course['weekDay']] + " |", course['startTime'] + "-" + course['endTime'] + "节 |",
              course['name'] + " |",
              course['teacher'] + " |", course['weeks'] + " |", course['classRoom'] + " | ")

        print("-" * 50)




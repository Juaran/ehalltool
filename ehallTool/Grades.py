import requests, json, operator


def get_Grades(cookie, term):

    print("获取 {} 成绩信息...".format(term))

    url = "http://ehall.ynu.edu.cn/jwapp/sys/cjcx/modules/cjcx/xscjcx.do"
    r = requests.get(url, headers=cookie)

    if r.status_code == 200:

        data_rows = json.loads(r.text)['datas']['xscjcx']['rows']
        grades = []

        for row in data_rows:
            if row["XNXQDM"] == term:
                grade = {}

                grade['name'] = row['KCM']  # 考试名称
                grade['score'] = str(row['ZCJ'])  # 分数
                grade['getPoint'] = str(row['XFJD'])  # 绩点
                grade['xueFen'] = str(row['XF'])  # 学分

                grade['pscj'] = row['PSCJ']  # 平时成绩
                grade['qzcj'] = row['QZCJ']  # 其中成绩
                grade['qmcj'] = row['QMCJ']  # 期末成绩

                if grade['pscj'] is None:
                    grade['pscj'] = ''
                if grade['qzcj'] is None:
                    grade['qzcj'] = ''
                if grade['qmcj'] is None:
                    grade['qmcj'] = ''

                grades.append(grade)

            grades = sorted(grades, key=operator.itemgetter('score'), reverse=True)

        return grades


def print_Grades(grades, term):
    # grades = get_Grades(cookie, term)

    print("=" * 50)
    if term.split('-')[2] == '1':
        title = "成绩查询 " + term.split('-')[1] + "年 春季学期"
    if term.split('-')[2] == '2':
        title = "成绩查询 " + term.split('-')[1] + "年 秋季学期"
    print(title.center(50))
    print("=" * 50)

    for grade in grades:
        print("| " + grade['name'],
              "| " + str(grade['score']) + "分 | " + str(grade['getPoint']) + "绩点 | " + str(grade['xueFen']) + "学分 | ")
        print("-" * 50)



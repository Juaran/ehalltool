import requests, json, operator


def get_ExamSchedual(cookie, term):

    print("获取 {} 考试安排...".format(term))

    url = "http://ehall.ynu.edu.cn/jwapp/sys/studentWdksapApp/modules/wdksap/wdksap.do"
    r = requests.post(url, headers=cookie, data={'XNXQDM': term})

    if r.status_code == 200:

        data_rows = json.loads(r.text)['datas']['wdksap']['rows']
        exams = []

        for row in data_rows:
            exam = {}

            exam['name'] = row['KCM']  # 考试名称
            exam['teacher'] = row['ZJJSXM']  # 授课老师
            exam['classRoom'] = row['JASMC']  # 考试地点
            exam['examTime'] = row['KSSJMS']  # 考试时间

            if exam['classRoom'] is None:
                exam['classRoom'] = '未安排'
            if exam['examTime'] is None:
                exam['examTime'] = '未安排'
            if exam['teacher'] is None:
                exam['teacher'] = '未安排'

            exams.append(exam)

        exams = sorted(exams, key=operator.itemgetter('examTime'))

        return exams


def print_ExamSchedual(exams, term):
    # exams = get_ExamSchedual(cookie, term)

    print("=" * 50)
    if term.split('-')[2] == '1':
        title = "我的考试安排 " + term.split('-')[1] + "年 春季学期"
    if term.split('-')[2] == '2':
        title = "我的考试安排 " + term.split('-')[1] + "年 秋季学期"
    print(title.center(50))
    print("=" * 50)

    for exam in exams:

        print("| " + exam['examTime'], "| " + exam['name'], "| " + exam['teacher'], "| " + exam['classRoom'] + " | ")

        print("-" * 50)




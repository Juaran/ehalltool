from . import seleniumLogin
from linkMysql import connect
from . import updateMysql

""" 从app传入username和password，进行校验 """


def get_result(username, password):

    ehallDb = connect.EhallMysql()  # 连接数据库
    ehallDb.check_table()  # 检查表
    user_in_database = ehallDb.check_in(username, password)  # 检查用户 1 有 0 无

    if user_in_database:
        # 已存在数据库
        return True

    else:
        # 不存在数据库
        cookie = seleniumLogin.getCookie(username, password)  # 调用登录

        if cookie is not None:
            # 登录成功

            updateMysql.Update(username, password, cookie)  # 更新数据
            return True

        else:
            # 登录失败
            return False


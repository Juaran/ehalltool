"""

    Selenium + Chrome(headless) 登录获取 Cookie

"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from config import *


Cookie = ''     # 待获取 cookie 信息


def getCookie(UserName, PassWord):
    """ 需要获取的主要cookie参数 """

    print("\n正在登录...", end="")

    """ 浏览器设置 """
    chrome_options = Options()

    if HEAD_LESS:
        chrome_options.add_argument("--headless")  # 无界面加载

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')

    if IMAGE_LESS:
        prefs = {"profile.managed_default_content_settings.images": 2}  # 无图加载
        chrome_options.add_experimental_option("prefs", prefs)

    """ 创建浏览器对象 """
    wb = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER_PATH)

    """ 打开统一登录页面 """
    wb.get("http://ehall.ynu.edu.cn/login?service=http://ehall.ynu.edu.cn/new/index.html")

    try:
        """ 填写用户名和密码 """
        username = WebDriverWait(wb, 5).until(EC.visibility_of_element_located((By.ID, "username")))
        username.send_keys(UserName)

        password = WebDriverWait(wb, 5).until(EC.visibility_of_element_located((By.ID, "password")))
        password.send_keys(PassWord)

        """ 回车登录进入主页 """
        password.send_keys(Keys.RETURN)

        time.sleep(0.1)

        try:

            """ 处理异常：登录失败 """
            if wb.find_element_by_class_name("auth_error"):

                print("登录失败！")

                time.sleep(0.1)

                """ 异常处理：二次认证 """
                try:
                    if wb.find_element_by_class_name("color-dark-green"):
                        password = WebDriverWait(wb, 5).until(EC.visibility_of_element_located((By.ID, "password")))
                        password.send_keys(PassWord)

                        """ 回车二次登录进入主页 """
                        password.send_keys(Keys.RETURN)
                        print("二次认证登录成功！\n")

                except:
                    return None

        except:
            print("登录成功！\n")

        """ 在主页获取第一个cookie: MOD_AUTH_CAS """
        cookies = wb.get_cookies()
        for cookie in cookies:
            if cookie['name'] == 'MOD_AUTH_CAS':
                #                 print("GetCookie-MOD_AUTH_CAS:", cookie['value'])
                global Cookie
                Cookie = 'MOD_AUTH_CAS=' + cookie['value']

        time.sleep(0.1)

        """ 点击进入一个桌面应用 """
        course_schedual = WebDriverWait(wb, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="widget-hot-01"]/div[1]/widget-app-item[1]/div/div/div[2]/div[1]')))
        course_schedual.click()

        time.sleep(0.1)

        try:
            """ 出现进入提示，点击进入 """
            amp_enter = WebDriverWait(wb, 5).until(EC.element_to_be_clickable((By.ID, 'ampDetailEnter')))
            amp_enter.click()

            time.sleep(0.1)

        except:
            pass

        """ 打来新标签，切换到应用窗口 """
        all_handles = wb.window_handles
        for handle in all_handles:
            wb.switch_to.window(handle)  # 切换窗口

            cookies = wb.get_cookies()
            for cookie in cookies:
                if cookie['name'] == '_WEU':
                    #                     print("GetCookie-_WEU:", cookie['value'])
                    Cookie = Cookie + ';_WEU=' + cookie['value']

        return {'Cookie': Cookie}

    finally:

        """ 关闭浏览器 """
        wb.quit()


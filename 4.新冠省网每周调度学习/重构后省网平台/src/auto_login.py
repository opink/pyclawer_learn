import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_cookies():
    """Returns : requests_session, cruser """
    # 1.首先连接VPN。
    # 启动selenium登录省网
    denglu_link = 'http://10.60.0.52:83/sysmanage_sd/systems.jsp'
    cruser = webdriver.Firefox()
    cruser.get(denglu_link)
    time.sleep(random.randint(1, 2))
    cruser.find_element_by_id('username').send_keys('******')
    cruser.find_element_by_id('password').send_keys('******')
    cruser.find_element_by_id('vaildCode').send_keys('')
    time.sleep(random.randint(1, 2))
    WebDriverWait(cruser,
                  60).until(EC.presence_of_all_elements_located(
                      (By.ID, 'app')))
    # print('1.登录成功时的cookies')
    # print(cruser.get_cookies())
    name = cruser.find_elements_by_xpath(
        "//div[@class='centerBox']//a[@title='预防接种信息管理']/img")[0]
    name.click()
    time.sleep(random.randint(1, 2))
    # print('2.点击跳转后的cookies')
    # print(cruser.get_cookies())
    # 2.到达jsp页面 获得cookies转为requests.session直接post请求
    requests_session = requests.Session()
    requests_session.headers.update({
        'Accept':
        'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control':
        'max-age=0',
        'Connection':
        'keep-alive',
        'Content-Type':
        'application/x-www-form-urlencoded',
        'Host':
        '10.60.0.16:83',
        'Origin':
        'http://10.60.0.16:83',
        'Referer':
        'http://10.60.0.16:83/ShanDong/gjdc/xgRptArea_query.action',
        'Upgrade-Insecure-Requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'
    })
    sd_cookie = cruser.get_cookies()[0]['value']
    requests_session.headers.update(
        {'cookie': f'JSESSIONID_shandong={sd_cookie}'})

    return requests_session, cruser

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
s = requests.Session()
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(3)
driver.get('https://authserver.szu.edu.cn/authserver/login?service=https%3A%2F%2Felearning.szu.edu.cn%2Fwebapps%2Fcbb-sdgxtyM-BBLEARN%2FcasSSO.jsp')
driver.find_elements_by_xpath("//input[@name='username']")[0].send_keys('151881')
driver.find_elements_by_xpath("//input[@name='password']")[0].send_keys('60923569')
driver.find_elements_by_xpath("//button")[0].click()
cookies = driver.get_cookies()
driver.close()
# 获得登录的cookie以访问其他页面
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])
p = s.get(url='https://elearning.szu.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1')
print p.text

#喵喵折1：先收藏商品

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from priceSpiderr import writePrice 似乎没用到writePrice
import time

options = webdriver.ChromeOptions()
extension_path = r'C:\Users\文化哥\AppData\Local\Google\Chrome\User ' \
                 r'Data\Default\Extensions\ekbmhggedfdlajiikminikhcjffbleac\6.0.1.0_0.crx '
options.add_extension(extension_path)
browser = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(browser, 20)


def login_miao(): #登录
    try:
        browser.get('http://www.henzan.com/login')
        submit1 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#bd > div > div.login-wrap > div.bd > dl > dd > a.xl > i'))
        )
        submit1.click()

        username = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#userId'))
        )
        password = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#passwd'))
        )
        submit2 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#outer > div > div.WB_panel.oauth_main > form > div > '
                                                         'div.oauth_login_box01.clearfix > div > p > '
                                                         'a.WB_btn_login.formbtn_01'))
        )
        username.send_keys('15822726282')
        password.send_keys('cyx726282')
        submit2.click()
        browser.add_cookie({'name': '15822726282', 'value': 'cyx726282'})

    except TimeoutException:
        return login_miao()


def search_collect():               #逐个打开link文件中的商品链接，点击收藏
    f = open('link.txt', 'r')
    index = 1
    while True:
        link = f.readline()
        if link == '':
            break
        print('第' + str(index) + '件商品: '+link)
        browser.get(link)
        collect = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[@title='收藏后，商品降价/到货会有提醒哦']"))
        )
        collect.click()
        index = index + 1
    f.close()


def main():
    login_miao()
    time.sleep(5)
    search_collect()


if __name__ == '__main__':
    main()

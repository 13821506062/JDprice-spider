#喵喵折2：获取收藏商品的id

import re
import xlwt
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 20)


def login_miao():   #登录
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


def mouse_chain():  #模拟鼠标操作 具体没看
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#hd > div > div.hd-wrap-menu.fr > div > div > div.userinfo '
                                                     '> div > a'))
    )
    chain = ActionChains(browser)
    implement = browser.find_element_by_xpath('//*[@id="hd"]/div/div[2]/div/div/div[1]/div/a')
    chain.move_to_element(implement).perform()
    collect = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#hd > div > div.hd-wrap-menu.fr > div > div > '
                                                     'div.menu.popup-box > ul > li:nth-child(3) > a'))
    )
    collect.click()

    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#bd > div > div.tab-body > div > div > div.bd > ul > li:nth-child(1) > div > div > a'))
    )

    for i in range(20):
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        ActionChains(browser).key_down(Keys.DOWN).perform()

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#bd > div > div.tab-body > div > div > div.bd > ul > '
                                                         'li:nth-child(141) > div > a > img'))
    )
    html = browser.page_source
    return html


def parse_page(html): #爬取商品id
    pattern = re.compile('<li class="fl" data-id="(.*?)" data-ref="2" data-ourl="(.*?)">', re.S)
    items = re.findall(pattern, html)

    for item in items:
        yield {
            '链接': item[1],
            'id': item[0]
        }


def write_to_excel(content, worksheet, val1, val2): #写入excel表格
    for key, value in content.items():
        if key == '链接':
            worksheet.write(val1, 0, value)
        elif key == 'id':
            worksheet.write(val2, 4, value)
        else:
            pass


def main():
    login_miao()
    html = mouse_chain()

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    val1 = 1
    val2 = 1

    worksheet.write(0, 0, label='链接')
    worksheet.write(0, 4, label='id')

    for item in parse_page(html):
        write_to_excel(item, worksheet, val1, val2)
        val1 += 1
        val2 += 1
    workbook.save('E:\python_data\id1.xls')


if __name__ == '__main__':
    main()

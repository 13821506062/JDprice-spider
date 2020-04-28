import requests
import re
import xlwt
from requests import RequestException

#http://www.miaomiaozhe.com/api/goodspricetrend/-1557135013821929431网址格式，里面直接存储日期和价格
def get_one_page(num):
    url = "http://www.miaomiaozhe.com/api/goodspricetrend/" + num #获取网址，num需要通过收藏得到
    try:
        res = requests.get(url)
        res.encoding = 'utf-8'
        if res.status_code == 200:
            return res.text
        else:
            return None
    except RequestException:
        print('请求失败！！')
        return None

#{"dt":"2018\/03\/04","pr":6399},  ←无营销策略
def parse_one_page(html):
    pattern = re.compile(r'{"dt":"(.*?)","pr":(.*?)}', re.S) #正则表达式
    items = re.findall(pattern, html) #找到所有的日期和价格

    for item in items:
        if len(item[1]) < 10:  #有营销策略的价格长度大于10
            yield {
                '日期': item[0].replace('\/', '-'),
                '价格': item[1],
                '营销策略': ''
            }
        else:
            yield {
                '日期': item[0].replace('\/', '-'),
                '价格': item[1].split(':')[0][:-7], #以冒号分割，分成四块，第一块的0：倒数七位是价格
                '营销策略': item[1].split(':')[3][1:19]#以冒号分割，分成四块，第四块的1:19位是营销策略
            }


def write_to_excel(content, worksheet, val1, val2, val3):#content：item
    for key, value in content.items():
        if key == '日期':
            worksheet.write(val1, 0, value)#日期写入第val1行，第0列
        elif key == '价格':
            worksheet.write(val2, 2, float(value))#价格写入第val2行，第2列
        elif key == '营销策略':
            worksheet.write(val3, 4, value.encode('utf-8').decode('unicode_escape'))#营销策略写入第val3行，第4列
        else:
            pass


def main():
    f = open('number.txt', 'r') #打开存有网址编号的文件
    index = 1
    while True:
        num = f.readline()#一行行读取num
        if num == '':
            break
        print('第' + str(index) + '件商品: ' + num)

        workbook = xlwt.Workbook(encoding='utf-8')#新建一个excel文件
        worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        val1 = 1
        val2 = 1
        val3 = 1
        worksheet.write(0, 0, label='日期')
        worksheet.write(0, 2, label='价格')#应该改成1
        worksheet.write(0, 4, label='营销策略')#应该改成2

        html = get_one_page(num)#获取网址
        for item in parse_one_page(html):#抓取
            write_to_excel(item, worksheet, val1, val2, val3)#调用函数，逐行写入excel
            val1 += 1   #下一行（其实可以只定义一个val，val1、2、3值一直相同）
            val2 += 1
            val3 += 1
        workbook.save('E:' + str(index) + '.xls')
        index = index + 1
    f.close()


if __name__ == '__main__':
    main()

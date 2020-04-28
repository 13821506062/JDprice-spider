#日期格式转化

import datetime
import xlrd
import xlutils.copy
from xlrd import xldate_as_tuple


def main():
    for excel in range(1, 152):
        print('正在改第' + str(excel) + '个表格...')
        readbook1 = xlrd.open_workbook('E:\python_data\京东零食\零食（' + str(excel) + '）.xlsx')
        readbook2 = xlrd.open_workbook('E:\python_data\零食2\零食_' + str(excel) + '.xls')
        wb1 = xlutils.copy.copy(readbook1)
        ws1 = wb1.get_sheet(0)
        sheet1 = readbook1.sheet_by_name('Sheet1')
        sheet2 = readbook2.sheet_by_name('sheet1')
        lst1 = sheet1.col_values(0, 3)
        lst2 = sheet2.col_values(0, 1)
        for i in range(len(lst1)):
            if sheet1.cell(i+3, 0).ctype == 3:#如果格式是日期
                d = xldate_as_tuple(sheet1.cell(i+3, 0).value, 0)
                date = str(datetime.datetime(*d))[0:-9]
                for j in range(len(lst2)):
                    if sheet2.cell_value(j+1, 0) == date:
                        if sheet2.cell_value(j + 1, 1) != '':
                            ws1.write(i+3, 5, sheet2.cell_value(j+1, 1))
                        else:
                            pass
        wb1.add_sheet('Sheet2', cell_overwrite_ok=True)
        wb1.save('E:\python_data\京东零食价格\零食（' + str(excel) + '）.xls')#转化后存进京东零食价格


if __name__ == '__main__':
    main()

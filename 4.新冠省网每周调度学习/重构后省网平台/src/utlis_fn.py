from pathlib import Path
import calendar
from datetime import datetime


def half_year_ago(date: datetime.date) -> str:
    """半年前日期字符串，月底对应月底
    Parameters
    ----------
    date : datetime.date

    Returns
    -------
    str
    """
    month = date.month - 6
    if month == 0:
        month = 12
        year = int(date.year - 1)
    else:
        year = int(date.year + month / 12)
    if month < 0:
        month = 12 + month
    day = min(date.day, calendar.monthrange(year, month)[1])
    dt = date.replace(year=year, month=month, day=day)
    # print(dt)
    dt = str(dt)
    return dt


def three_month_ago(date: datetime.date) -> str:
    """3个月前日期，月底对应月底
    Parameters
    ----------
    date : datetime.date
        上周末日期
    Returns
    -------
    str
    """
    month = date.month - 3
    if month == 0:
        month = 12
        year = int(date.year - 1)
    else:
        year = int(date.year + month / 12)
    if month < 0:
        month = 12 + month
    day = min(date.day, calendar.monthrange(year, month)[1])
    dt = date.replace(year=year, month=month, day=day)
    # print(dt)
    dt = str(dt)
    return dt


def open_path_file(file_name, time_h):
    """根据日期字符串和时间字符串创建文件夹"""
    P = Path('./dfiles/' + file_name + '/' + time_h)
    P.mkdir(parents=True, exist_ok=True)


def do_save(table, pst_tables, time_h, name):
    """保存响应网页的表格为csv"""
    open_path_file(pst_tables.date, time_h)
    table.to_csv(f'./dfiles/{pst_tables.date}/{time_h}/{name}.csv',
                index=False, encoding='utf-8_sig')
    print(f'下载完成！ 保存地址 ./dfiles/{pst_tables.date}/{time_h}/{name}.csv')

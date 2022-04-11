import datetime


def monitor_delta(date, num):
    # 月份计算
    delta_month = date.month + num
    new_month = delta_month % 12
    if new_month == 0:
        new_month = 12
    if delta_month < 1:
        new_date = date.replace(year=(date.year - 1 + int(delta_month / 12)), month=new_month, day=1) + datetime.timedelta(days=date.day-1)
    else:
        new_date = date.replace(year=(date.year + int((delta_month - 1) / 12)), month=new_month, day=1) + datetime.timedelta(days=date.day-1)
    return new_date


def get_tomorrow(date):
    tomorrow = date + datetime.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    return tomorrow


def work_days(start_date, end_date):
    count = 0
    while start_date < end_date:
        if start_date.isoweekday() < 6:
            count += 1
        start_date += datetime.timedelta(1)
    return count


week_day_zh = {
    0: '一',
    1: '二',
    2: '三',
    3: '四',
    4: '五',
    5: '六',
    6: '日',
}
holiday_zh = {
    'Mid-autumn Festival': '中秋',
    'National Day': '国庆',
    "New Year's Day": '元旦',
}


def shift_strptime(shift):
    start_time, end_time = shift.split(' - ')
    return datetime.datetime.strptime(start_time, '%H:%M'), datetime.datetime.strptime(end_time, '%H:%M')


if __name__ == '__main__':
    print(monitor_delta(datetime.date(2021, 8, 31), 1))

# 调度./tasks/中定义好的任务
import time
from src.auto_login import get_cookies
from tasks import task1, task2

dd = 'Today'
# dd = 'Yesterday'


def main(dd=dd):
    time_h = time.strftime('%H%M')
    requests_session, driver = get_cookies()
    task1.main(dd, requests_session, time_h)
    task2.main(dd, requests_session, time_h)
    driver.quit()


if __name__ == '__main__':
    main(dd=dd)

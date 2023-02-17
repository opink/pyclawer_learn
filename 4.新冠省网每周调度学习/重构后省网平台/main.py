# 调度./tasks/中定义好的任务
import time
from src.auto_login import get_cookies
from tasks import task1, task2


def main(dd: str, requests_session, time_h):
    task1.main(dd, requests_session, time_h)
    task2.main(dd, requests_session, time_h)


if __name__ == '__main__':
    time_h = time.strftime('%H%M')
    requests_session, driver = get_cookies()
    # main('Today', requests_session, time_h)
    main('Yesterday', requests_session, time_h)
    driver.quit()

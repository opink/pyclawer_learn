import time
from typing import List, Union
from src.auto_login import get_cookies
# 调度./tasks/中定义好的任务
from tasks import task3


def main(dd: Union[str, List[str]], requests_session, time_h: str):
    task3.main(dd, requests_session, time_h)


if __name__ == '__main__':
    time_h = time.strftime('%H%M')
    requests_session, driver = get_cookies()
    # main('Today', requests_session, time_h)
    main(['2023-04-03', '2023-04-09'], requests_session, time_h)
    driver.quit()

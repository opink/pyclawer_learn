# 每个task代表一个通报表格的从前到后,主要用于描述后处理过程
from src.posttable import pst_factory
from src.tabular import Tabular
from src.utlis_fn import do_save


task_duty = {
    # 户籍类型占比统计表，不包含狂犬门诊，0-7岁儿童0-1、1-2、2-3...7-8岁
    '8-1-1': {'cmodid': '29117', 'age': [0, 1, 2, 3, 4, 5, 6, 7]} 
            }


def main(dd, requests_session, time_h):
    task = {}
    for name, param in task_duty.items():
        tabular = Tabular(**param, dd=dd)
        dftable = pst_factory(param['cmodid'])(tabular).pst(requests_session, name)
        do_save(dftable, tabular, time_h, name)
        task[name] = dftable

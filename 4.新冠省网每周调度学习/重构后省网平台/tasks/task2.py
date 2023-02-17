# 每个task代表一个通报表格的从前到后,主要用于描述后处理过程
from src.tabular_and_post import Tabular
from src.utlis_fn import do_save


task_duty = {
    # 户籍类型占比统计表，不包含狂犬门诊，0-7岁儿童0-1、1-2、2-3...7-8岁
    # '8-1-1': {'cmodid': '29117', 'age': [0, 1, 2, 3, 4, 5, 6, 7]} 
    '8-1-1': Tabular(cmodid='29117', age=[0, 1, 2, 3, 4, 5, 6, 7]),
            }


def main(dd, requests_session, time_h):
    task = {}
    for name, tabular in task_duty.items():
        pst_table = tabular.get_device()(tabular, dd)
        dftable = pst_table.pst(requests_session, name)
        do_save(dftable, pst_table, time_h, name)
        task[name] = dftable

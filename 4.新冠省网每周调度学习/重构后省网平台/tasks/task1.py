# 每个task代表一个通报表格的从前到后,主要用于描述后处理过程
from src.posttable import pst_factory
from src.tabular import MappingClass, Tabular
from src.utlis_fn import do_save


task_duty = {
    # 新冠病毒疫苗分地区各剂次接种情况统计表，60-79岁，[11]列为当日加强接种数
    '7-1-1': {'cmodid': '1010011167', 'age': [60, 65, 70], 'mappingclass': MappingClass.ZHEN_JIE},
            }


def main(dd, requests_session, time_h):
    task = {}
    for name, param in task_duty.items():
        tabular = Tabular(**param, dd=dd)
        dftable = pst_factory(param['cmodid'])(tabular).pst(requests_session, name)
        do_save(dftable, tabular, time_h, name)
        task[name] = dftable
    # cpu逻辑
    df_0_1 = task['7-1-1'].copy()[[11]]
    df_0_1_sum = df_0_1.sum()
    df_0_1.loc['合计'] = df_0_1_sum
    df_0_1.index.name = '60-79接种数情况'
    df_0_1 = df_0_1.rename(columns={11: '当日接种数'})
    df_0_1 = df_0_1.reset_index()
    df_0_1.to_csv(
        f'./dfiles/{tabular.date}/{time_h}/{tabular.weekago} - {time_h} - result_tables00.csv',
        encoding='utf-8_sig',
        index=False)

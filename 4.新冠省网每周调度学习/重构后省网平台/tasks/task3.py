# 每个task代表一个通报表格的从前到后,主要用于描述后处理过程
import random
import time
from src.tabular_and_post import MappingClass, Tabular
from src.utlis_fn import do_save
import pandas as pd
from concurrent import futures

T0 = "2020-01-01"


def gen_duty(daterange):
    task_duty = {
        # 例： 新冠病毒疫苗分地区各剂次接种情况统计表，60-79岁，[11]列为当日加强接种数
        # '7-1-1': {'cmodid': '1010011167', 'age': [60, 65, 70], 'mappingclass': MappingClass.ZHEN_JIE},
        '1-1-1': Tabular(cmodid='1010011167', age=[3,6,12,15,18,50,55,60,65,70,80], mappingclass=MappingClass.ZHEN_JIE, dd=daterange),  # 周1234
        '1-2-1': Tabular(cmodid='1010011167', age=[3,6,12,15], mappingclass=MappingClass.ZHEN_JIE, dd=[T0, daterange[1]]),  # 累计
        '1-2-2': Tabular(cmodid='1010011167', age=[18,50,55], mappingclass=MappingClass.ZHEN_JIE, dd=[T0, daterange[1]]),  # 累计
        '1-2-3': Tabular(cmodid='1010011167', age=[60, 65, 70], mappingclass=MappingClass.ZHEN_JIE, dd=[T0, daterange[1]]),  # 累计
        '1-2-4': Tabular(cmodid='1010011167', age=[80], mappingclass=MappingClass.ZHEN_JIE, dd=[T0, daterange[1]]),  # 累计
        '1-3-1': Tabular(cmodid='1010011167', age=[3,6,12,15,18,50,55,60,65,70,80], mappingclass=MappingClass.ZHEN_JIE, dd=[T0, daterange[1]]),  # 累计4
                }
    return task_duty


def main(dd, requests_session, time_h):
    """
    用线程池做的多线程爬虫
    """
    task = {}
    executor = futures.ThreadPoolExecutor(max_workers=6)
    fs = []
    for name, tabular in gen_duty(dd).items():
        pst_table = tabular.get_device()(tabular, tabular.dd)
        # dftable, status_code, name = pst_table.pst(requests_session, name)
        f = executor.submit(pst_table.pst, requests_session, name)
        time.sleep(random.random() * 0.1)  # 增加一点点post请求延迟
        fs.append(f)
    futures.wait(fs)
    result = [f.result() for f in fs]
    for dftable, status_code, name in result:
        try:
            # 保存原始页面
            do_save(dftable, pst_table, time_h, name)
        except ValueError:
            print(f'检查一下post表单 : name = {name} , status_code={status_code} \n \
            检查一下处理后表单 : dftype = {type(dftable)}')
            continue
        dftable = pst_table.select_rows(dftable)
        task[name] = dftable
        do_save(dftable.reset_index(), pst_table, time_h, "_mapped_"+name)

    # 以下为后处理的cpu逻辑
    # 1. _0_1周接种剂次
    df_0_1 = task['1-1-1'].copy()[[1, 3, 6, 9]]
    df_0_1_sum = df_0_1.sum()
    df_0_1.loc['合计'] = df_0_1_sum
    df_0_1.index.name = '本周接种数情况'
    df_0_1 = df_0_1.rename(columns={1: '第一', 3: '二', 6: '三', 9: '四'})
    # df_0_1 = df_0_1.reset_index()
    # 2. _1_1 3-17岁组全程率、（加强率不需接种）
    df_1_1_quan = task['1-2-1'].copy()[[2, 3]]
    df_1_1_quan_sum = df_1_1_quan.sum()
    df_1_1_quan.loc['合计'] = df_1_1_quan_sum
    df_1_1_quan = (df_1_1_quan[3]/df_1_1_quan[2].round(2)).to_frame(name='3-17全程')
    df_1_1_jiaq = task['1-2-1'].copy()[[5, 6]]
    df_1_1_jiaq_sum = df_1_1_jiaq.sum()
    df_1_1_jiaq.loc['合计'] = df_1_1_jiaq_sum
    df_1_1_jiaq = (df_1_1_jiaq[6]/100).round(1).to_frame(name='3-17加强')
    df_1_1_jiaq[df_1_1_jiaq >= 0] = "-"
    # 3. _1_2 18-59岁组全程率、加强率
    df_1_2_quan = task['1-2-2'].copy()[[2, 3]]
    df_1_2_quan_sum = df_1_2_quan.sum()
    df_1_2_quan.loc['合计'] = df_1_2_quan_sum
    df_1_2_quan = (df_1_2_quan[3]/df_1_2_quan[2].round(2)).to_frame(name='18-59全程')
    df_1_2_jiaq = task['1-2-2'].copy()[[5, 6]]
    df_1_2_jiaq_sum = df_1_2_jiaq.sum()
    df_1_2_jiaq.loc['合计'] = df_1_2_jiaq_sum
    df_1_2_jiaq = (df_1_2_jiaq[6]/df_1_2_jiaq[5].round(2)).to_frame(name='18-59加强')
    # 4. _1_3 60-79岁组全程率、加强率
    df_1_3_quan = task['1-2-3'].copy()[[2, 3]]
    df_1_3_quan_sum = df_1_3_quan.sum()
    df_1_3_quan.loc['合计'] = df_1_3_quan_sum
    df_1_3_quan = (df_1_3_quan[3]/df_1_3_quan[2].round(2)).to_frame(name='60-79全程')
    df_1_3_jiaq = task['1-2-3'].copy()[[5, 6]]
    df_1_3_jiaq_sum = df_1_3_jiaq.sum()
    df_1_3_jiaq.loc['合计'] = df_1_3_jiaq_sum
    df_1_3_jiaq = (df_1_3_jiaq[6]/df_1_3_jiaq[5].round(2)).to_frame(name='60-79加强')        
    # 5. _1_4 80+岁组全程率、加强率
    df_1_4_quan = task['1-2-4'].copy()[[2, 3]]
    df_1_4_quan_sum = df_1_4_quan.sum()
    df_1_4_quan.loc['合计'] = df_1_4_quan_sum
    df_1_4_quan = (df_1_4_quan[3]/df_1_4_quan[2].round(2)).to_frame(name='80+全程')
    df_1_4_jiaq = task['1-2-4'].copy()[[5, 6]]
    df_1_4_jiaq_sum = df_1_4_jiaq.sum()
    df_1_4_jiaq.loc['合计'] = df_1_4_jiaq_sum
    df_1_4_jiaq = (df_1_4_jiaq[6]/df_1_4_jiaq[5].round(2)).to_frame(name='80+加强')
    # 6. _2_1第四剂次累计
    df_2_1 = task['1-3-1'].copy()[[9]]
    df_2_1_sum = df_2_1.sum()
    df_2_1.loc['合计'] = df_2_1_sum
    df_2_1 = df_2_1.rename(columns={9:'累计4剂次'})

    result_table1 = pd.concat([df_1_1_quan, df_1_1_jiaq, df_1_2_quan, df_1_2_jiaq, df_1_3_quan, df_1_3_jiaq, df_1_4_quan, df_1_4_jiaq], axis=1)
    print(result_table1)  # 打印调试
    result_table = pd.concat([df_0_1, result_table1, df_2_1], axis=1).reset_index()
    
    result_table.to_csv(
        f'./dfiles/{pst_table.date}/{time_h}/{pst_table.weekago} - {time_h} - result_tables03.csv',
        encoding='utf-8_sig',
        index=False)
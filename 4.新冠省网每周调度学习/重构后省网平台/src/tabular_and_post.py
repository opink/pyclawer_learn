# 根据Tabular的cmodid选择对应post表单并接收其余参数，返回需要的待处理表并保存在确认位置


from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import random
import time
from typing import Dict, List, Optional
import pandas as pd
from src.utlis_fn import half_year_ago, three_month_ago


class MappingClass(Enum):
    """代表posttable返回表单的mapping等级"""
    ZHEN_JIE = "镇街"
    MEN_ZHEN = "门诊"


@dataclass
class Tabular:
    cmodid: str
    fixeddaterange: Optional[List[str]] = None
    age: Optional[List[int]] = None
    mappingclass: Optional[MappingClass] = None

    def get_device(self) -> 'Cmodid':
        # 需定义接口类
        cmodid_to_pst: Dict[str, "Cmodid"] = {
                '1010011167': Cmodid1010011167,
                '29117': Cmodid29117
                }
        return cmodid_to_pst.get(self.cmodid, NotImplementedError)


class Cmodid(ABC):
    """代表网页接口"""
    date: str
    weekago: str
    a_month_ago: str
    three_month_ago: str
    half_year: str

    def __init__(self, tabular: Tabular, dd: str):
        if tabular.fixeddaterange:
            self.date = self.fixeddaterange[0]
            self.weekago = self.fixeddaterange[1]
        else:
            self.provide_datebean(dd)

    @abstractmethod
    def generate(self) -> Dict:
        """生成post请求的data表单"""

    def pst(self, requests_session, name) -> pd.DataFrame:
        """发送请求并获得返回原始数据表"""
        resp = requests_session.post(self.target_url, data=self.generate())
        time.sleep(random.randint(1, 2) * 0.2)
        resp.encoding = resp.apparent_encoding
        print(f'name = {name}, encoding = {resp.encoding}, status_code={resp.status_code}'
        )
        # print(resp.text)
        table = pd.read_html(resp.text, encoding='utf-8')[-1]
        # print(table) # 调试
        try:
            # 接着处理表格，转换对应镇街
            # print(f'响应表格 ---  \n  {table}')  # 调试
            table = self.select_rows(table)
            return table
        except ValueError:
            print(f'检查一下post表单 : name = {name} , status_code={resp.status_code} \n \
            检查一下处理后表单 : dftype = {type(table)}')

    @abstractmethod
    def select_rows(self, table: pd.DataFrame) -> pd.DataFrame:
        """从pst返回的原始数据表中选择需要的数据行"""
        """后转换为对应镇街或者对应门诊"""

    def provide_datebean(self, dd: str):
        """根据main函数提供的dd参数，制作需要的databean"""
        if dd == "Week":
            self.date = str(datetime.date(datetime.now()) - datetime.timedelta(1))  # 减一天
            self.weekago = str(datetime.date(datetime.now()) - timedelta(7))  # 减一周
            self.half_year = half_year_ago(
                datetime.date(datetime.now()) - timedelta(1))
        elif dd == "Today":
            self.date = str(datetime.date(datetime.now()))  # 今天
            self.weekago = str(datetime.date(datetime.now()))  # 今天
            self.a_month_ago = str(datetime.date(datetime.now()) - timedelta(22))  # 减21+1天
        elif dd == "Yesterday":
            self.date = str(datetime.date(datetime.now()) - timedelta(1))  # 减一天
            self.weekago = str(datetime.date(datetime.now()) - timedelta(1))  # 减一天
            self.a_month_ago = str(datetime.date(datetime.now()) - timedelta(22))  # 减21+1天
            self.three_month_ago = three_month_ago(
                                datetime.date(datetime.now()) - timedelta(1))
            self.half_year = half_year_ago(
                                datetime.date(datetime.now()) - timedelta(1))
        else:
            raise ValueError("dd = Week or Yesterday or Today")


class Cmodid29117(Cmodid):
    target_url = 'http://10.60.0.16:83/ShanDong/stat/regtypeGcb_query.action'  # 0-7岁儿童户籍类型占比统计表

    def __init__(self, tabular: Tabular, dd: str):
        super().__init__(tabular, dd)
        self.age: List[int] = tabular.age

    def generate(self):
        return {'cModId': '29117',  # 似乎没用，不过先留着吧。。
                'cOption': 4,
                'skipValue': 4,
                'areaCode':
                '371082010100,371082010200,371082010300,371082010400,371082010500,371082030100,371082030200,371082038100,371082038200,371082050100,371082050200,371082058100,371082058200,371082070100,371082078100,371082080100,371082088100,371082090100,371082098100,371082100100,371082108100,371082110100,371082118100,371082130100,371082138100,371082140100,371082148100,371082180100,371082180200,371082188100,371082188200,371082190100,371082190200,371082190300,371082190400,371082190500,371082250100,371082258100,371082270100,371082270200,371082278100,371082278200,371082280100,371082280400,371082288100,371082288200,371082298100,371082304100,371082308100,371082318100,371082328100,371082338100,371082340300,371082358100,371082368100,371082374100,371082378100,371082378200',
                'chkAge': True,
                '__checkbox_chkAge': True,
                'age': self.age,  # [0,1,2,3,4,5,6,7],  # 0-1，1-2，2-3，...，7-8
                # 'ageSel': [1,2,3,4,5,6,7],
                'isRabs': 0,   # [0,1]为包含狂犬门诊
                '__multiselect_isRabs': ''
                }

    def select_rows(self, table):
        table = table[~table[0].isin(['荣成市中医院成人预防接种门诊', '荣成市寻山街道卫生院接种点', '荣成市石岛人民医院接种点'])]
        return table


class Cmodid1010011167(Cmodid):
    target_url = 'http://10.60.0.16:83/ShanDong/gjdc/xgRptJzjcArea_query.action'  # 新冠病毒疫苗分地区各剂次接种情况统计表

    def __init__(self, tabular: Tabular, dd: str):
        super().__init__(tabular, dd)
        # self.date: str = tabular.date
        # self.weekago: str = tabular.weekago
        self.ageSel: List[int] = tabular.age
        self.mappingclass = tabular.mappingclass

    def generate(self):
        return {'cModId': '1010011167',
                'cOption': 4,
                'skipValue': 4,
                'areaCode':
                '371082010100,371082010200,371082010300,371082010400,371082010500,371082030100,371082030200,371082038100,371082038200,371082050100,371082050200,371082058100,371082058200,371082070100,371082078100,371082080100,371082088100,371082090100,371082098100,371082100100,371082108100,371082110100,371082118100,371082130100,371082138100,371082140100,371082148100,371082180100,371082180200,371082188100,371082188200,371082190100,371082190200,371082190300,371082190400,371082190500,371082250100,371082258100,371082270100,371082270200,371082278100,371082278200,371082280100,371082280400,371082288100,371082288200,371082298100,371082304100,371082308100,371082318100,371082328100,371082338100,371082340300,371082358100,371082368100,371082374100,371082378100,371082378200',
                'datebean.beginDate': self.date,
                'datebean.endDate': self.weekago,
                'chkAge': True,
                '__checkbox_chkAge': True,
                # 'age':[60,65,70],  # 不重要
                'ageSel': self.ageSel  # [60,65,70]
                }

    def select_rows(self, table):
        table = table.copy().iloc[1:59, 1:12].astype(float).astype(int)
        # print(f'astype后表格 ---  \n  {table}')
        table = table.reset_index(
                    drop=True)  # 重置index以便对应镇街Series的index
        # table = table.iloc[:, 1:]

        if self.mappingclass == MappingClass.ZHEN_JIE:
            table['zhenjie'] = pd.DataFrame(
                                zhenjie_mapping)['对应镇街']  # 添加对应合并列
            table = table.groupby(['zhenjie']).sum(0)  # 计算
        elif self.mappingclass == MappingClass.MEN_ZHEN:
            table['menzhen'] = pd.DataFrame(
                                zhenjie_mapping)['对应单位']  # 添加对应合并列
            table = table.groupby(['menzhen']).sum(0)  # 计算

        print(f'按合并登记归并后表格 ---  \n  {table}')
        return table


# mappingclass真正的对应
zhenjie_mapping = {
        '系统单位': {
            0: '崖头镇寻山卫生院预防接种门诊 3710820101',
            1: '崖头镇崂山卫生院预防接种门诊 3710820102',
            2: '中医院预防接种门诊       3710820103',
            3: '荣成市康宁医院预防接种门诊 3710820104',
            4: '荣成市人民医院预防接种门诊 3710828801',
            5: '俚岛中心卫生院预防接种门诊 3710820301',
            6: '俚岛镇马道卫生院接种门诊 3710820302',
            7: '荣成市俚岛镇马道卫生院狂犬病暴露处置门诊 3710820381',
            8: '荣成市俚岛中心卫生院狂犬病暴露处置门诊 3710820382',
            9: '第三人民医院预防接种门诊 3710820501',
            10: '成山镇龙须岛卫生院预防接种门诊 3710820502',
            11: '荣成市成山镇龙须岛卫生院狂犬病暴露处置门诊 3710820581',
            12: '荣成市第三人民医院狂犬病暴露处置门诊 3710820582',
            13: '埠柳中心卫生院预防接种门诊 3710820701',
            14: '荣成市埠柳中心卫生院狂犬病暴露处置门诊 3710820781',
            15: '港西镇卫生院预防接种门诊 3710820801',
            16: '荣成市港西镇卫生院狂犬病暴露处置门诊 3710820881',
            17: '整骨医院预防接种门诊 3710820901',
            18: '荣成市整骨医院狂犬病暴露处置门诊 3710820981',
            19: '夏庄卫生院预防接种门诊 3710821001',
            20: '荣成市夏庄镇卫生院狂犬病暴露处置门诊 3710821081',
            21: '荫子镇卫生院预防接种门诊 3710821101',
            22: '荣成市荫子镇卫生院狂犬病暴露处置门诊 3710821181',
            23: '大疃镇卫生院预防接种门诊 3710821301',
            24: '荣成市大疃镇卫生院狂犬病暴露处置门诊 3710821381',
            25: '上庄中心卫生院预防接种门诊 3710821401',
            26: '荣成市上庄中心卫生院狂犬病暴露处置门诊 3710821481',
            27: '人和中心卫生院预防接种门诊 3710821801',
            28: '人和镇靖海卫生院预防接种门诊 3710821802',
            29: '荣成市人和中心卫生院狂犬病暴露处置门诊 3710821881',
            30: '荣成市人和镇靖海卫生院狂犬病暴露处置门诊 3710821882',
            31: '荣成市石岛社区卫生服务中心接种门诊 3710821901',
            32: '王连卫生院预防接种门诊 3710823101',
            33: '宁津卫生院预防接种门诊 3710823201',
            34: '东山中心卫生院预防接种门诊 3710823301',
            35: '斥山卫生院预防接种门诊 3710823401',
            36: '滕家中心卫生院预防接种门诊 3710822501',
            37: '荣成市滕家中心卫生院狂犬病暴露处置门诊 3710822581',
            38: '虎山镇黄山卫生院预防接种门诊 3710822701',
            39: '虎山镇卫生院预防接种门诊 3710822702',
            40: '荣成市虎山镇黄山卫生院狂犬病暴露处置门诊 3710822781',
            41: '荣成市虎山镇卫生院狂犬病暴露处置门诊 3710822782',
            42: '东城区社区卫生服务中心预防接种门诊 3710822801',
            43: '荣成市中医院成人预防接种门诊 3710822804',
            44: '荣成市人民医院狂犬病暴露处置门诊 3710822881',
            45: '荣成市中医院狂犬病暴露处置门诊 3710822882',
            46: '荣成市康宁医院狂犬病暴露处置门诊 3710822981',
            47: '荣成市寻山街道卫生院接种点 3710823041',
            48: '荣成市寻山街道卫生院狂犬病暴露处置门诊 3710823081',
            49: '荣成市崂山街道卫生院狂犬病暴露处置门诊 3710823181',
            50: '荣成市宁津街道卫生院狂犬病暴露处置门诊 3710823281',
            51: '荣成市石岛社区卫生服务中心狂犬病暴露处置门诊 3710823381',
            52: '荣成市东山街道中心卫生院桃园预防接种门诊 3710823403',
            53: '荣成市王连街道卫生院狂犬病暴露处置门诊 3710823581',
            54: '荣成市东山街道中心卫生院狂犬病暴露处置门诊 3710823681',
            55: '荣成市石岛人民医院接种点 3710823741',
            56: '斥山街道卫生院狂犬病暴露处置门诊 3710823781',
            57: '荣成市石岛人民医院狂犬病暴露处置门诊 3710823782'
        },
        '对应单位': {
            0: '寻山',
            1: '崂山',
            2: '中医院',
            3: '康宁',
            4: '一院',
            5: '俚岛',
            6: '马道',
            7: '马道',
            8: '俚岛',
            9: '成山',
            10: '龙须',
            11: '龙须',
            12: '成山',
            13: '埠柳',
            14: '埠柳',
            15: '港西',
            16: '港西',
            17: '整骨',
            18: '整骨',
            19: '夏庄',
            20: '夏庄',
            21: '荫子',
            22: '荫子',
            23: '大疃',
            24: '大疃',
            25: '上庄',
            26: '上庄',
            27: '人和',
            28: '靖海',
            29: '人和',
            30: '靖海',
            31: '港湾',
            32: '王连',
            33: '宁津',
            34: '东山',
            35: '斥山',
            36: '滕家',
            37: '滕家',
            38: '黄山',
            39: '虎山',
            40: '黄山',
            41: '虎山',
            42: '东城',
            43: '中医院',
            44: '一院',
            45: '中医院',
            46: '康宁',
            47: '方舱',
            48: '寻山',
            49: '崂山',
            50: '宁津',
            51: '港湾',
            52: '桃园',
            53: '王连',
            54: '东山',
            55: '二院',
            56: '斥山',
            57: '二院'
        },
        '对应镇街': {
            0: '寻山街道',
            1: '崂山街道',
            2: '崖头街道',
            3: '城西街道',
            4: '崖头街道',
            5: '俚岛镇',
            6: '俚岛镇',
            7: '俚岛镇',
            8: '俚岛镇',
            9: '成山镇',
            10: '成山镇',
            11: '成山镇',
            12: '成山镇',
            13: '埠柳镇',
            14: '埠柳镇',
            15: '港西镇',
            16: '港西镇',
            17: '崖西镇',
            18: '崖西镇',
            19: '夏庄镇',
            20: '夏庄镇',
            21: '荫子镇',
            22: '荫子镇',
            23: '大疃镇',
            24: '大疃镇',
            25: '上庄镇',
            26: '上庄镇',
            27: '人和镇',
            28: '人和镇',
            29: '人和镇',
            30: '人和镇',
            31: '港湾街道',
            32: '王连街道',
            33: '宁津街道',
            34: '东山街道',
            35: '斥山街道',
            36: '滕家镇',
            37: '滕家镇',
            38: '虎山镇',
            39: '虎山镇',
            40: '虎山镇',
            41: '虎山镇',
            42: '崖头街道',
            43: '崖头街道',
            44: '崖头街道',
            45: '崖头街道',
            46: '城西街道',
            47: '崖头街道',
            48: '寻山街道',
            49: '崂山街道',
            50: '宁津街道',
            51: '港湾街道',
            52: '桃园街道',
            53: '王连街道',
            54: '东山街道',
            55: '斥山街道',
            56: '斥山街道',
            57: '斥山街道'
        }
    }

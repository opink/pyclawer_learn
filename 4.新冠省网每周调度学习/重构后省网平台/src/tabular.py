from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, timedelta
from enum import Enum

from src.utlis_fn import half_year_ago, three_month_ago


class MappingClass(Enum):
    """代表posttable返回表单的mapping等级"""
    ZHEN_JIE = "镇街"
    MEN_ZHEN = "门诊"


@dataclass
class Tabular:
    cmodid: str
    dd: str
    timerange: List[str] = None
    age: Optional[List[int]] = None
    mappingclass: MappingClass = None

    def __post_init__(self):
        if self.timerange:
            self.date = self.timerange[0]
            self.weekago = self.timerange[1]
        else:
            self.provide_datebean(dd=self.dd)

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
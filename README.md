# pyclawer_learn
 学习简单的python网页爬虫


1. 学习简单静态网页的Xpath；-- 包含文件 学习.ipynb , Xpath0.png , Xpath1.png
2. 自动化测试练习网页；-- 包含文件 理论考试自动化调试练手包括答案整理.ipynb , 2021年第四季度干部理论考试题库.docx ，答案.xlsx
3. 学习爬虫基本的内容；-- 包含文件 爬虫基本学习.ipynb
4. 新冠省网每周调度学习；-- 包含文件 省网每周新冠已经可用.ipynb
5. AKshareSDK接口重封装学习；-- 包含文件 netsFinding.ipynb , ./backups/｛DATE｝/*.xlsx , ./afiles(TODO)/


---
    '''python
    # 网页参数替换为字典形式

    (.*?): (.*)$ 和 
    '$1':'$2', 

    '''

    '''python
    pd.to_csv('',encoding='utf-8_sig')  # 编码带上sig，简中excel可以找到BOM

    '''

    """
    excel中 查重身份证 需要特别的公式才能扩展到15位以后→  =countif(A2:A,A2&"*")
    excel中 身份证vlookup 需要特别的公式才能扩展到15位以后→在前面加上 = vlookup("*"&A2,A:E,2,False)
    """

---

# 过程脚本代码重构成面向对象复用

【Software Design in Python】 https://www.bilibili.com/video/BV1Vd4y1k7dH/?p=14&share_source=copy_web&vd_source=11141d7b83e628e7a2f8baf703e55130
     恶臭代码，写作中必须避免：

     """
     1. 字符串类别，容易打错字；用变量维护 Enum类 & auto
     2. 代码重复，一处修改处处修改；只有一个box
     3. neety；列表生成式
     4. 变量命名尤其是不体现量纲的
     5. If isinstance子类，不应判断实例类型；消费者消费类的接口，面向消费者设计接口————所谓的“依赖倒置”处处都有，用类将行为和数据结合起来。
     6. 方法的目标是责任分离，但是看到通过传入一个布尔标识，让我们在两者之间做出选择，从而将两种责任合二为一；改回单一职责
     7.Exception但是不用，别的代码可能会接过去；用不到就不用
     """

---

     """
     1. strategypattern（依赖倒置的实现），面向消费者提供abc.ABC和abc.abstractmethod，实现开闭原则；
     2. factorypattern，可以用两个dataclass具体地维护（字符串、元组等）索引对象————（其实是最早的只有oop程序，只有一个__call__方法的类不如简单地直接传入函数）；
     3. 
     """

---

     """
     请补充
     vscode重构代码常用快捷键：删除、修改
     1. 直接删除光标所在当前行： ctrl + shift + K；
     2. 删除光标之后的该行所有内容： ctrl + shift + arrow（→）、delete；
     3. 多选相同内容，并可以在相同内容移动光标统一修改：ctrl+D；
     4. 重命名变量：f2；
     5. ctrl + I 提示输入提示；
     6. ctrl + shift + F 在文件中查找；
     7. alt + F12 速览定义；
     8. 
     """

---

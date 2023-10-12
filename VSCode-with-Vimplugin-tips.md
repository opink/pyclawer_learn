[TOC]
# vscvim
> 收集vscode使用vim种的常用操作

**markdown中所有一对尖括号，记得转义\\<>使用**


# 一、in normal mode
## 1. 单按键动作
- [norm] s : 删除当前字符并进入编辑模式
- [norm] x (X) : 删除当前字符 (删除光标处前一个字符)
- [norm] ~ : 切换当前字符大小写
- [norm] u : 撤销
    - [norm] \<C-r> : 重做
- [norm] % : 匹配括号
- [norm] * : 查找光标处单词
- [norm] / (?) : 向后查找(向前查找)
    - [norm] n (N) : 下一个(上一个)
    - [norm] \<C-n> : nohl 取消高亮
- [norm] I : 行首进插入
- [norm] A : 行尾进插入
- [norm] o : 另起一行进插入
- [norm] O : 新建光标的上面一行进插入

## 2. 移动
- [norm] {重复次数} hjkl : 移动光标
- [norm] gg : 移动到文件头
- [norm] G : 移动到文件尾
- [norm] 20gg : 移动到第20行
- [norm] % : 移动到配对的括号处

### 2.1 光标在文件内和不同文件间跳跃追踪/返回
- [norm] \<C-o> : 光标跳转至上次编辑位置
- [norm] \<C-i> : 光标跳转至上次跳转位置
- [norm] \<C-^> : 光标跳转至上次编辑文件

## 3. 多按键动作
- [norm] rx : 替换单个字符为x
- [norm] zc : 折叠代码
- [norm] zo : 打开折叠
- [norm] \<learder> \<learder> s : EASYMOTION - 快速搜索跳转
- [norm] fcrC : find c replace C

> 执行-重复.-回退u 工作流

### 3.1 动作+ {count} + 动作类型
- [norm] d2j : 删除当前行和下两行，共3行
- [norm] d2f' : 删除光标至本行第2个'处
- [norm] dt' : 删除光标至本行第1个'前
- [norm] d/hello : 删除光标至第一个hello之间的所有字符
- [norm] y2/foo[enter]p : 复制并粘贴从光标处到第2个发现的foo之间的内容
- [norm] c2w : 从光标处向后替换2个词并进入insert模式

### 3.2 动作+ {i or a} + 文本类型
> 文本类型:
- w : word
- s : sentence
- p : paragraph
- [vscvim] e : entire file
- [vscvim] q : 引号(单、双、反)
- [vscvim] a : 参数
- b | ( | ) : block surrounded by ( )
- B | { | } : block surrounded by { }
- \< | > : surrounded by \< >
- [ | ] : surrounded by [ ]
- " | ' : quoted text

#### 3.2.1 surrounding插件
- [norm] ds' : 删除包围的引号
- [norm] cs'" : 修改包围的单引号为双引号
- [norm] ysaptli> : 新建对段落包围的标签\<li> \</li>
- 

### 3.3 g trigger
- [norm] g~w : 切换当单词的大小写
- [norm] gUw : 转换当前单词为大写
- [norm] guw : 转换当前单词为小写
- [norm] gUU : 转换当前行所有字母为大写
- [norm] gi : 返回因意外离开insert model的最后修改的光标位置
- [norm] gb (gB) : 创建多光标所在单词的词尾(词首)进入view mode
- [norm] gd : 跳转到光标所在变量的定义处
- [norm] gf : 跳转到光标所在单词的文件


### 3.4 常用double click 的操作
- [norm] >> : 向右缩进光标
- [norm] \<\< : 向左缩进光标
- [norm] == : 格式化文本
- [norm] dd (D) : 删除当前行 (删除当前字符至行尾)
- [norm] ggdG : 返回到文件头，删除至文末

### 3.5 register
- [norm] "ayy : 复制当前行到a register

### 3.6 marco
- [norm] qa : 定义一个名为a的宏

### 3.7 command 
- [norm] :reg : 显示所有寄存器的内容
- [norm] :reg{register} : 显示指定寄存器的内容
- [norm] :[range]s/{pattern}/{substitute}/{flags} : 替换文本
    - 例 :%s/cucumber/\//g : 将当前文件中所有的cucumber替换为/
- [norm] :sp (:vsp) : 水平分割窗口(垂直分隔窗口)
    - [norm] \<C-w> hjkl : 光标跳至分隔的窗口
    - [norm] :only : 只保留当前窗口

### 3.8 vscode的窗口快捷键
- \<C-`> : 切换到vscode cmd 窗口
- \<C-2> : 新建/切换到vscode 2号窗口
    - \<C-w> : 在已打开2、3...窗口情况下，逐个关闭当前标签/窗口
- \<C-F4> : 关闭当前标签/窗口
- \<C-o> : 后台打开到上一个标签
- \<C-tab> : 切换标签

# 二、 in insert mode

## 1 删除修改
- \<C-w> : 删除最后输入的词
- \<C-u> : 删除最后键入的行

## 2 register
- \<C-r> " : pastes the contents of the unnamed register
- \<C-r> a : pastes the contents of the a register
- \<C-r> 0 : pastes the contents of the yank register

## 3 
- \<C-o> : 执行一个普通模式下的单个命令，然后返回插入模式

# 三、 in view mode

## 1 
- v : character-wise visual mode
- V : line-wise visual mode
- \<C-v> : block-wise rectangular mode

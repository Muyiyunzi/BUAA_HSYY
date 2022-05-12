"""
=============系号对应表===============
对应关系如有错误，请在repo中提issues指正，感谢！
32系 航发
35系 国际通用工程
36系 大飞机
39系 网安
41系 微电子（集成电路科学与工程）
42系 人工智能研究员
43系 前沿院
71系 传源
73系 士谔
74系 冯如
75系 士嘉
76系 守锷
77系 致真
79系 知行
"""

def school_trans(i: int) -> int:
    if 1 <= i <= 21:
        return i - 1
    elif 23 <= i <= 30:
        return i - 2
    else:
        encode = [32, 35, 36, 39, 41, 42, 43, 71, 73, 74, 75, 76, 77, 79]
        decode = [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]
        try:
            return decode[encode.index(i)]
        except ValueError as e:
            print("系号输入错误，如有疑惑请查阅school_trans.py中的系号对应表")
            raise e

if __name__ == '__main__':
    print(school_trans(72))



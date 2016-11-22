#!/usr/bin/env python
# -*- coding: utf-8 -*-

#print(),input()

#s = input('input some words:>>')
#print(s)
print(30)
print(30 + 200)
#print()无参数输出空行
print()
#逗号输出一个空格
print('100 + 200 =', 100 + 200)
#接受多个字符串
print('hello', 'world', 'by', 'python')

'''
数据类型和变量
'''
#八六进制0x
print(oct(100))
#二进制0b
print(bin(100))
#字符串换行
print('''line1
...line2
...line3''')
#python3中字符串编码格式为unicode，可以用中文作变量等
中国 = 'china'
print(中国)
# ord(str)查看字符的编码, chr(int)将编码转为字符并输出
print(ord('中'))
print(chr(25991))
print('\u4e2d\u6587')
#bytes字节类型
x = b'ABC'
print(x)
# unicode编码的str以encode()方法编码为指定bytes(ascii或utf-8)
print('ABC'.encode('ascii'))
print('中文'.encode('utf-8')) #超出ascii字符集的内容只能以utf-8编码方式
# decode()将bytes字节文本解码为ascii或utf-8编码文本
print(b'ABC'.decode('ascii'))
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))

# 函数；用尾递归优化方法实现汉诺塔的编码
'''
三个墩，ABC，A上有n个盘子，以B做为中转站将所有盘子转移到C上。
'''
def hanoi(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
        return
    else:
        hanoi(n-1, a, c, b) # 将上方n-1个盘子放到B上
        hanoi(1, a, b, c) # 将A上最后一盘子放到C上
        hanoi(n-1, b, a, c) # 将b上的盘子放到C上

hanoi(4, 'a', 'b', 'c')

#list-expression;列表生成式，包含if判断及预处理
L1 = ['HELLO', 'world', 18, 'Apple', None]
L2 = [ i.lower() for i in L1 if isinstance(i, str)]
print(L2)


# generator；生成器；列表生成器()；或yield语句
def triangles(n):
    l = [1]
    j = 1
    while j <= n:
        yield l
        l.append(0) # 每次循环前使列表长度增加1，末元素值为0
        l = [l[i-1] + l[i] for i in range(len(l))]
        j += 1

for n in triangles(5):
    print(n)

'''
迭代器：Iterator,拥有方法next()；当抛出StopIteration错误则迭代结束。
迭代器是惰性序列，需要主动调用next()才计算下一个值。
from collections import Iterator
isinstance(arg, Iterator)判断对象是否为Iterator对象
list, dict, str, set都是具有迭代性(Iterable)，但不是迭代器；需要借助iter()构建
'''

# map(func, *args)； reduce(func, *args)
from functools import reduce
def char2num(s):
    return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5':5, '6':6, '7': 7, '8':8, '9': 9}[s]

def chr2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))

print(chr2int('13579'))

s = ['adam', 'LiSa', 'bar']
def normalize(name):
    def low_cap(s):
        return s.lower().capitalize()

    return list(map(low_cap, name))

print(normalize(s))

# 求积
def prod(l):
    return reduce(lambda x, y: x * y, l)

print(prod([1, 2, 3]))

def str2float(s):
    l = s.split('.')
    point = len(l[1])
    if point > 0:
        s = l[0] + l[1]
    return chr2int(s) / (10 ** point)

print(str2float('123.456'))

#filter(func, *iterator)
print("filter()>>>")
#回数

def ishuishu(n):
    # 将n转为字符串，然后字符串反转并相比较，相等为回数
    if n <= 10:
        return 0
    if str(n) == str(n)[::-1]:
        return 1
    return 0

output = filter(ishuishu, range(1000, 10000))
print(list(output))

#sorted(*args, key=None, reverse=False)'key是个函数
d = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

L2 = sorted(d, key=lambda x:x[0].lower())
print(L2)

print(sorted(d, key=lambda x:x[1], reverse=True))

# 装饰器decorator
from functools import wraps

def log(text):
    def decorator(func):
        @wraps(func) # 使函数名保持一致
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log('excute')
def now():
    import time
    print(time.localtime())

now()
#相当于 now = log('excute)(now); log('excute)返回decorator函数;decorator(now)执行函数操作

'''
偏函数：将某函数的部分参数固定（非默认值）并返回该函数为基的新函数；相当于调整默认值
from functools import partial
'''
from functools import partial
def base_fun(x, y):
    return x + y

# 固定y值，构建新的函数
y2 = partial(base_fun, y=2)
print(y2(5)) # 5+2
print(y2(5, y=3)) # 5+3

'''
类和实例
'''
print("Class type>>>>>")
# 学生
class Student(object):
    __slots__ = ('name', 'age', '__score', '__papa') # 限制实例的属性可选范围;但对子类无效，即没有继承性
    student_number = 0 # 类属性是全局的

    def __init__(self, name):
        self.name = name
        self.__papa = None # 设置内部属性，限制外部访问

    def set_papa(self, papa):
        self.__papa = papa

    def get_papa(self):
        return self.__papa

    @property
    def score(self):
        return self.__score

    @score.setter #注意是setter，不能是其它的名称; 还有个属性是deleter, getter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer')
        if value < 0 or value > 100:
            raise ValueError('score must be between 0 ~ 100 !')
        self.__score = value

def register(name, **kw):
    s = Student(name)
    for k, v in kw.items():
        setattr(s, k, v)
    Student.student_number += 1
    return s

bob = register('Bob', score=90)
bob.set_papa('DHQ')
ta = register('Ta', age=25)

print(hasattr(bob, 'score'))
print(getattr(bob, 'score'))
print(getattr(ta, 'age'))
print(Student.student_number)
print(bob.get_papa())

# 属性装饰器@property可将类方法的调用过程隐藏并转为属性
ta.score = 60 # ta.score.setter(60)
print(ta.score) # ta.score.getter(60)

# 特殊方法
class Chain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        # getattr是动态调用的
        print(Chain('%s/%s' % (self._path, path)))
        return Chain('%s/%s' % (self._path, path))

    def __call__(self, param):
        # __call__直接调用实例本身（注意不是实例方法）
        print("----call-----")
        print(Chain('%s/%s' % (self._path, param)))
        return Chain('%s/%s' % (self._path, param))

    def __str__(self):
        return self._path

    __repr__ = __str__

print(Chain().status.user.timeline.list)
print(Chain().status.users('python').repos)

'''
枚举类：当有多个常量可归类时，可用Enum生成;常量的值默认从1开始
from enum import Enum
@unique装饰器可以去重
'''
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

print(Month.Jan)

for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

print(isinstance(Month.Jan, Month))
print(type(Month.Jan))
print(issubclass(Month, Enum))
print(type(Month))
print(Month.Feb.value)
print(Month.Feb.name)
print(type(1))

# 元类
# http://blog.csdn.net/weixin_35955795/article/details/52985170

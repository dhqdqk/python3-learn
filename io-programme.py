#!/usr/bin/env python
## -*- coding:utf-8 -*-

'''
#IO:read and write： 硬盘读写
stringIO bytesIO: 缓存读写
file and directory
json ：序列化
'''
import os

# atom-runner takes project-dir as cirdir then it work wrong
if 'pthon3-learn' not in os.path.abspath('.'):
    os.chdir(os.path.join(os.path.abspath('.'), 'python', 'python3-learn'))

# IO: read and write
with open(os.path.join(os.path.abspath('.'), 'test.py'), 'r') as f:
    for line in f.readlines():
        print(line.strip('\n')) # remove th tail '\n' of every line

# stringIO：在缓存读写字符串类型数据;读写不能并存于同一对象
from io import StringIO

f = StringIO()
f.write('hello')
f.write(' ')
f.write('world!')
print(f.getvalue())

f1 = StringIO('Hello!\nHI!\nGoodbye!')
for line in f1.readlines():
    print(line.strip('\n'))

# bytesIO: 在缓存中读写二进制数据
from io import BytesIO
b = BytesIO()
b.write('中文'.encode('utf-8'))
print(b.getvalue())
print(b.tell()) # 读取当前指针位置
b.seek(1) # 将指针位置设为1
print(b.tell())
print(b.read())
print(b.tell())

b1 = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(b1.read())

# file and dir
# os模块是文件和目录操作的API
import os
print(os.name) # os Type
if hasattr('uname', 'os'):
    # win中os没有uname方法
    print(os.uname()) # os的详细信息
print(os.environ.get('PATH'))

print(os.path.abspath('.'))
print(os.path.join(os.path.abspath('.'), 'test.py'))

print([x for x in os.listdir('.') if os.path.isfile(x)])

print(os.listdir('.'))
print(os.stat('.git'))

class FindFile(object):
    def __init__(self, searchdir='', searchstr=''):
        self.searchdir = self.check_searchdir(searchdir)
        self.searchstr = self.check_searchstr(searchstr)
        self.findtimes = 0

    def check_searchdir(self, searchdir):
        'check the searchdir is valid or not'
        if os.path.isdir(searchdir):
            return searchdir
        else:
            print ("'%s' is not vaild dir name." % searchdir)
            return ''

    def check_searchstr(self, searchstr):
        'the search content should be string'
        if isinstance(searchstr, str):
            return searchstr
        else:
            print ("'%s' is not valid string" % searchstr)
            return ''

    def findfile(self, path, word):
        for x in os.listdir(path):
            fp = os.path.join(path,x)
            if os.path.isdir(fp):
                self.findfile(fp,word)
            else:
                if word in os.path.splitext(x)[0]:
                    # 检查文件名是否包含指定字符串
                    print(os.path.abspath(fp))
        return

    def ls(self):
        if self.searchdir != '':
            self.findfile(self.searchdir, self.searchstr)

f = FindFile('.', 'ba')
f.ls()

# pickling
# pickle is python's own model
d = dict(name='python', version=3.5, pickle='pickle')
print(d)

import  pickle
pd = pickle.dumps(d)

with open('pdumps.txt', 'wb') as f:
    f.write(pickle.dumps(d))
# pickle translate d from dict to bytes by pickling
print(pd)

with open('pdump.txt', 'wb') as pf:
    pickle.dump(d, pf)

with open('pdump.txt', 'rb') as f:
    pl = pickle.load(f)
print(pl)

# JSON: universal standard
'''
JSON类型	    Python类型
{}            dict
[]	          list
"string"	  str
1234.56	      int或float
true/false	  True/False
null	      None
'''
import json
j = dict(name='python', version=3.5, pickle='json')

js = json.dumps(j)
print(js)
print(type(js))

with open('jdump.txt', 'w') as f:
    # dump(json-obj, file-obj)
    json.dump(js,f)

with open('jdumps.txt', 'w') as f:
    f.write(json.dumps(j))

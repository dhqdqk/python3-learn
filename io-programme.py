#!/usr/bin/env python
## -*- coding:utf-8 -*-

'''
#IO:read and write： 硬盘读写
stringIO bytesIO: 缓存读写
file and directory
json ：序列化
'''
'''
import os
# IO: read and write
with open(os.path.join(os.path.abspath('.'), 'test.py'), 'r') as f:
    for line in f.readlines():
        print(line.strip('\n')) # remove th tail '\n' of every line
'''

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
print(os.uname()) # os的详细信息
print(os.environ.get('PATH'))

print(os.path.abspath('.'))
print(os.path.join(os.path.abspath('.'), 'test.py'))

print([x for x in os.listdir('.') if os.path.isdir(x)])

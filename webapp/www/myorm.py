#!/usr/bin/env python3
# coding:utf-8

import logging
import asyncio
import aiomysql

logging.basicConfig(level=logging.INFO)

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

async def create_pool(loop, **kw):
    '创建连接到数据库的全局连接池'
    logging.info('create global database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3306),
        user = kw['user'],
        password = kw['password'],
        db = kw['db'],
        charset = kw.get('charset', 'utf8'),
        autocommit = kw.get('autocommit', True),
        # 最大连接数
        maxsize = kw.get('maxsize', 14),
        minsize = kw.get('minsize', 1),
        loop = loop
    )

async def destory_pool():
    '使用event_loop后要销毁连接池pool'
    global __pool
    if __pool is not None:
        __pool.close()
        await __pool.wait_closed()

async def select(sql, args, size=None):
    '从数据库查表的操作'
    log(sql, args)
    global __pool
    with (await __pool) as conn:
        cur = await conn.cursor(aiomysql.Dictcursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs

'''
封装insert, update, delete
语句操作参数一样，定义一个通用的执行函数
返回操作影响的行号
'''
async def execute(sql, args):
    'update, delete, set操作共用execute执行'
    log(sql)
    with (await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            await conn.commit()
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return affected

def create_args_string(num):
    '根据输入的参数生成占位符列表'
    l = []
    for n in range(num):
        l.append('?')
    # ','为分隔符，将列表合成字符串
    return (','.join(l))

class ModelMetaclass(type):
    '''
     -*-定义Model的元类

    # 所有的元类都继承自type
    # ModelMetaclass元类定义了所有Model基类(继承ModelMetaclass)的子类实现的操作

    # -*-ModelMetaclass的工作主要是为一个数据库表映射成一个封装的类做准备：
    # ***读取具体子类(user)的映射信息
    # 创造类的时候，排除对Model类的修改
    # 在当前类中查找所有的类属性(attrs)，如果找到Field属性，就将其保存到__mappings__的dict中，
        同时从类属性中删除Field(防止实例属性遮住类的同名属性)
    # 将数据库表名保存到__table__中

    # 完成这些工作就可以在Model中定义各种数据库的操作方法
    '''
    def __new__(cls, name, bases, attrs):
        '''
        #__new__控制__init__的执行，所以在其执行之前

        #在当前类中查找所有的类属性(attrs)，如果找到Field属性，就将其保存到__mappings__
            的dict中，同时从类属性中删除Field(防止实例属性遮住类的同名属性)
            将数据库表名保存到__table__中完成这些工作就可以在Model中定义各种数据库的操作方法
        # bases: 代表继承父类的集合
        # attrs: 类的方法集合
        '''
        # 排除Model类本身
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)

        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        # 获取所有Field和主键名
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 存在主键
                    if primaryKey:
                        # 设置过主键；重复
                        raise RuntimeError('Duplicate primary key for fields %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        # 保存属性和列的映射关系
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        # 主键属性名
        attrs['__primary_key__'] = primaryKey
        # 非主键的属性名
        attrs['__fields__'] = fields
        # 构造默认的SELECT, INSERT, UPDATE, DELETE语句
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey,
                                        ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
            tableName, ', '.join(escaped_fields),
            primaryKey, create_args_string(len(escaped_fields)+1)
            )
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName,
            '. '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)),
            primaryKey
            )
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no abbtribution %s." % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def find(cls, pk=None):
        # find object by primay key.
        rs = select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__),
                          [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        logging.info('save: %s' % args)
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)


class Field(object):
    'Field负责保存（数据库）表的字段名和字段类型'
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s: %s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, length=100):
        column_type = 'varchar(%s)' % len
        super().__init__(name, column_type, primary_key, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'Text', False, default)

class FloatField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'float', False, default)


if __name__ == '__main__':
    class User(Model):
        __table__ = 'users'
        id = IntegerField(primary_key=True)
        name = StringField()

    user = User(id=123, name='python')
    print(user.getValue('id'))

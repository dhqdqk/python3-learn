#!/usr/bin/env python
# coding:utf-8

import random
import os
from datetime import datetime
from PIL import Image, ImageFilter, ImageDraw, ImageFont

# 随机字母
def rndChar():
    return chr(random.randint(65, 90))

# 随机颜色
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

class PinChar(object):
    'create an pin picture with chars(a-zA-Z)'
    def __init__(self):
        self.width = 60 * 4
        self.height = 60
        self.__background()
        self.__addchar()
        self.__blur()

    def __background(self):
        '生成背景图'
        for x in range(width):
            for y in range(height):
                self.draw.point((x, y), fill=rndColor())

    def __addchar(self):
        '图像添加字母'
        self.charlist = []
        font = ImageFont.truetype('Arial.ttf', 36)
        for t in range(4):
            c = rndChar()
            self.charlist.append(c)
            draw.text((60 * t + 10, 10), c, font=font, fill = rndColor2())

    def __blur(self):
        '模糊处理'
        self.image = self.image.filter(ImageFilter.BLUR)

    def cname(self, salt=''):
        '生成文件名'
        t = datetime.utcnow()
        return str(t) + salt

    def save(self, path='.', f='jpeg'):
        if path == '.':
            os.chdir(os.path.join(os.path.abspath('.'), 'python', 'python3-learn'))
        else:
            os.chdir(path)
        self.image.save(self.name, f)

    def image(self):
        self.image = Image.new('RGB', (width, height), (255, 255, 255))
        self.draw = ImageDraw.Draw(image)
        self.__background()
        self.__addchar()
        self.__blur()
        self.name = self.cname()
        self.save()

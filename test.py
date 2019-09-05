#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: yinhaozheng
@software: PyCharm
@file: test.py
@time: 2019-09-05 15:55
"""
import os

__mtime__ = '2019-09-05'


if __name__=="__main__":
    for i in os.listdir("./"):
        print(i)
        # for filepath in files:
        #     print(filepath)
        # for sub in subdirs:
        #     print(sub)

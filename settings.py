# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 19:51:06 2019

@author: Administrator
"""

MAX_SCORE = 50
import logging

# 默认的配置
LOG_LEVEL = logging.INFO # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S' # 默认时间格式
LOG_FILENAME = 'log.log'

# 测试代理Ip的超时时间
TEST_TIMEOUT = 10 # 单位是s
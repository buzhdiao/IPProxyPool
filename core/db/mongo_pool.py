# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 19:51:06 2019

@author: Administrator
"""
'''
作用：用于对proxies集合进行数据库的相关操作
目标：实现对数据库增删改查等相关操作
步骤：
	1，在init中，建立数据了解，获取要操作的集合，在del方法中关闭数据库连接
	2，提供基础的增删改查功能
		2.1，实现插入功能
		2.2，实现修改功能；
		2.3，实现删除代理，根据代理中的IP删除代理
		2.4，查询所有代理IP的功能
	3，提供代理API的使用功能
		1），实现查询功能，根据条件进行查询，可以指定查询数量，先分数降序，速度升序排，保证优质的代理
		IP在上面
		2），实现根据歇息和要访问的网站的域名，获取代理IP请求；
		3），实现根据协议类型和要访问的域名，获取代理IP列表
		4），实现根据协议类型和要访问的完整域名，随机获取一个代理IP
		5），实现把指定域名添加得到指定IP的disable_domain列表中
'''

import pymongo
import random

from seetings import MONGO_URL,DEFAULT_SCORE
from domian import Proxy

class :
	def insert_one(self,proxy):
		'''2.1，实现插入功能'''
		count = self.proxies.count({'_id':proxy.ip})
		if count ==0:
			# 我们使用proxy.ip作为MongoDB中的数据的主键:_id
			dict = proxy.__dict__
			dic['_id'] = proxy.ip
			self.proxies.insert_one(dic)
			logger.info("插入新的代理：{}".format(proxy))
		else:
			logger.info("已经存在的代理：{}".format(proxy))

	def update_one(self,proxy):
		'''2.2，实现修改功能；'''
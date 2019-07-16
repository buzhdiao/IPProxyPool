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

from pymongo import MongoClient
import random
import pymongo 

from seetings import MONGO_URL,DEFAULT_SCORE
from utils.log import logger
from domian import Proxy

class MongoPool(object):

	def __init__(self):
		# 1.1 在init中，建立数据链接
		self.client = MongoClient(MONGO_URL)
		# 1.2 获取要操作的集合
		self.proxies = self.client['proxies_pool']['proxies']

	def __del__(self):
		# 1.3 关闭数据库链接
		self.client.close()
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
		self.proxies.update_one({"_id":proxy.ip},{"$set":proxy.__dict__})

	def delete_one(self,proxy):
		# 2.3，实现删除代理，根据代理中的IP删除代理
		self.proxies.delete_one({'_id':proxy.ip})
		logger.info("删除代理IP：{}".format(proxy))

	def find_all(self):
		# 2.4，查询所有代理IP的功能
		cursor = self.proxies.find()
		for item in cursor:
			# 删除_id这个key
			item.pop()
			proxy = Proxy(**item)
			yield proxy

	def find(sef,conditions={},count=0):
		# 1），实现查询功能，根据条件进行查询，可以指定查询数量，先分数降序，速度升序排，保证优质的代理
		# IP在上面
		cursor = self.proxies.find(conditions,limit = count).sort([
			('score',pymongo.DESCENDING),('speed',pymongo.ASCENDING)])
		proxy_list = []
		for item in cursor:
			item.pop('_id')
			proxy = Proxy(**item)
			proxy_list,append(proxy)

		return proxy_list
		# 2），实现根据协议和要访问的网站的域名，获取代理IP请求；
		conditions = {'nick_type':nick_type}

		if protocol is None:
			# 如果没有传入协议类型，返回支持http和https的协议的代理Ip
			conditions['protocol'] = 2
		elif protocol.lower()=='http':
			conditions['protocol'] = {'$in':[0,2]}
		else:
			conditions['protocol'] = {'$in':[1,2]}

		if domian:
			conditions['disable_dimains'] = {'$nin':[domian]}

		return self.find(conditions,count=count)
		# 3），实现根据协议类型和要访问的域名，获取代理IP列表
		# 4），实现根据协议类型和要访问的完整域名，随机获取一个代理IP
		# 5），实现把指定域名添加得到指定IP的disable_domain列表中

	def random_porxy(self,protocol=None,domian=None,nick_type=0):
		proxy_list = self.get_proxies(protocol=protocol,domian = domian,count = count,nick_type=nick_type)
		return random.choice(proxy_list)

	def disable_domian(self,ip,domian):
		# 把指定的域名添加到指定ip的disable_domain列表中
		if self.proxies.count({'_id':ip,'disable_domains':domian})==0:
			self.proxies.update_one({'_id':ip},{'$push':{'disable_domains':domian}})


if __name__ == '__main__':
	mongo = MongoPool()
	proxy = Proxy('202.104.113.35',port='53281')
	mongo.insert_one(proxy)
	proxy = Proxy('202.104.113.35',port='8888')
	mongo.update_one(proxy)
	proxy = Proxy('202.104.113.35',port='8888')
	mongo.delete_one(proxy)

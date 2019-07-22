# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:29:19 2019

@author: Administrator
"""
import time
import requests
import json

from settings import TEST_TIMEOUT
from utils.http import get_request_headers
from utils.log import logger
from domain import Proxy
# 实现代理池的校验模块
#目标：检查代理IP速度，匿名程度以及支持的协议类型

#步骤
#检查代理IP速度和匿名程度
#1，代理Io速：就是从发送请求到获取相应时间间隔
#2，匿名程度检查
#    1，对htyp://httpbin.org/get或者https://httpbin.org/get发送请求
#    2，对相应origin中有，分隔的两个Ip就是透明代理IP
#    3，如果响应的headers中包含proxy-connection，说明是匿名代理IP
#    4，否则就是高匿代理Ip
#    
#检查代理IP协议类型
#    如果http://httpbin.org/get发送请求可以成功，说明支持http协议
#    如果https://httpbin.org/get发送请求可以成功，说明支持https协议
def check_proxy(proxy):
    '''
    用于检查指定的proxy的响应速度，匿名程度，支持的协议类型
    '''
#    准备字典
    proxies = {'http':'http://{}:{}/'.format(proxy.ip,proxy.port),
               'https':'https://{}:{}/'.format(proxy.ip,proxy.port)}
    http,http_nick_type,http_speed = _check_http_proxies(proxies,is_http=True)
    https,https_nick_type,https_speed = _check_http_proxies(proxies,is_http=False)
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy
        
def _check_http_proxies(proxies,is_http=True):
#    匿名类型，
    nick_type = -1
#    响应速度，单位为s
    speed = -1
    if is_http:
        test_url = 'http://httpbin.org/get'
        proxy_url = {'http':proxies['http']}
    else:
        test_url = 'https://httpbin.org/get'
        proxy_url = {'https':proxies['https']}
#    获取开始时间
    start = time.time()
#    发送请求，获取相应数据
    try:
#        TEST_TIMEOUT
        
        response = requests.get(test_url,headers=get_request_headers(),timeout=TEST_TIMEOUT,proxies = proxy_url)
    
        if response.ok:
    #        计算响应速度
            speed = round(time.time()-start,2)
    #        匿名程度
    #       把相应的json字符串，转换为字典
            dic = json.loads(response.text)
            origin = dic['origin']
    #        1，对htyp://httpbin.org/get或者https://httpbin.org/get发送请求
            proxy_connection = dic['headers'].get('Proxy-Connection',None)
    #        2，对相应origin中有，分隔的两个Ip就是透明代理IP
            if ',' in origin:
                nick_type = 2
            elif proxy_connection:
            #    3，如果响应的headers中包含proxy-connection，说明是匿名代理IP
                nick_type = 1
            else:
                nick_type = 0 #高匿代理IP
            return True,nick_type,speed
        return False,nick_type,speed # -1代表
    except :
#        logger.exception(ex)
        return False,nick_type,speed


if __name__=='__main__':
#    125.110.64.117 9000
    proxy = Proxy('121.13.252.62',port = '41564')
    print(check_proxy(proxy))
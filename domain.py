# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 19:35:28 2019

@author: Administrator
"""

from settings import MAX_SCORE

class Proxy(object):
    
    def __init__(self,ip,port,protocol=-1,nick_type=-1,speed=-1,area=None,score=MAX_SCORE,
                 disable_domains=[]):
#        ip,代理的IP地址
        self.ip = ip
#        port,代理的port
        self.port = port
#        protocol，代理的协议，0代表http,1代表https,2代表http和https都有
        self.protocol = protocol
#       nick_type ：代理ip的匿名程度，高匿：0，匿名:1,透明:2
        self.nick_type = nick_type
#        speed,代理ip的相应速度，单位s
        self.speed = speed
#        area,代理IP所在地区
        self.area = area
#        score 代理ip的得分，用于衡量代理的可用性
        self.score = score
#       默认分值可以通过配置文件进行配置，在进行代理可用性检查的时候，每遇到一次请求失败就减1分，
#        减到0 的Ip就不可用
#        disable_domains:不可用域名列表，有些代理IP在某些域名不可用，但是在其他域名下可用
        self.disable_domains = disable_domains
        
#        提供__str__方法 ，返回数据字符串
    def __str__(self):
        return str(self.__dict__)
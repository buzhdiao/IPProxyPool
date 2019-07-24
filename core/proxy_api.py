'''
10.实现代理池的API模块
目标

为爬虫提供高可用代理IP的服务接管口

步骤：
实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
试下根据协议类型额域名，提供获取多个高可用代理IP的服务
实现给指定的IP上追加不可用域名的服务

实现：
1. 在proxy_api.py中，创建ProxyApi类
2。实现初始化方法
    2.1 初始化一个Flask的web服务
    2.2    实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
        可用通过protocol和domain参数对IP进行过滤
        protocol当前请求的协议类型
        domian 当前请求域名
    2.3 实现根据协议类型和域名，提供获取多个高可用代理IP的服务
        可用通过protocol和domain参数对IP进行过滤
        实现给指定的IP上追加不可用域名的服务
    2.4 如果在获取IP的时候，有指定域名参数，将不在获取该IP，从而进一步提高代理IP的可用性
3. 实现run方法，用于启动Flask的web服务
4. 实现start的类方法啊，用于通过类名，启动服务
'''
# 1. 在proxy_api.py中，创建ProxyApi类
from flask import Flask
from flask import request
import json
from core.db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT
class ProxyApi(object):

    def __init__(self):
        # 2.实现初始化方法
        # 2.1 初始化一个Flask的web服务
        self.app = Flask(__name__)
        # 创建mongoPool对象，用于操作数据库
        self.mongo_pool = MongoPool()


        @self.app.route('/random')
        def random():
            # 2.2    实现根据协议类型和域名，提供随机的获取高可用代理IP的服务
        # 可用通过protocol和domain参数对IP进行过滤
        # protocol当前请求的协议类型
        # domian 当前请求域名
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_porxy(protocol,domain,count=PROXIES_MAX_COUNT)
            if protocol:
                return  '{}://{}:{}'.format(protocol,proxy.ip,proxy.port)
            else:
                return '{}://{}:{}'.format(proxy.ip,proxy.port)


        @self.app.route('/proxies')
        def proxies():
            # 2.3 实现根据协议类型和域名，提供获取多个高可用代理IP的服务
        # 可用通过protocol和domain参数对IP进行过滤
        # 实现给指定的IP上追加不可用域名的服务
    #         获取协议，http/https
            protocol = request.args.get('protocol')
    #         域名
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol,domain,count=PROXIES_MAX_COUNT)
    #         proxies是一个proxy对象的列表，但是proxy对象不能进行json序列化，需要转换为字典列表
    #         转换为字典列表
            proxies = [proxy.__dict__ for proxy in proxies]
    #       返回json
            return  json.dumps(proxies)

        @self.app.route('/disable_domain')

        def disable_domain():
            # 2.4 如果在获取IP的时候，有指定域名参数，将不在获取该IP，从而进一步提高代理IP的可用性

            ip = request.args.get('ip')
            domain = request.args.get('domain')

            if ip is None:
                return '请求提供ip参数'
            if domain is None:
                return '请求提供域名domain参数'

            self.mongo_pool.disable_domain(ip,domain)
            return '{} 禁用 {} 成功'.format(ip,domain)
    def run(self):
        # 3. 实现run方法，用于启动Flask的web服务
        self.app.run('0.0.0.0',port=16888)

        
    @classmethod
    def start(cls):
#        4. 实现start的类方法啊，用于通过类名，启动服务
        proxy_api = cls()
        proxy_api.run()

if  __name__ == '__main__':
    # proxy_api = ProxyApi()
    # proxy_api.run()
    ProxyApi.start()
from settings import  PROXIES_SPIDERS
import importlib
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger

"""
实现爬虫运行模块：
目标：根据配置文件信息，加载爬虫，抓代理IP，进行校验，如果可用，写入数据库中

步骤：
1，在run_spiders.py中，创建Run_Spider类
2，提供一个运行爬虫的urn方法，作为运行爬虫的入口，实现核心的处理逻辑
    2.1根据配置文件信息，获取爬虫对象列表
    2.2遍历爬虫对象列表，获取爬虫对象，遍历爬虫对象的get_proxies方法，获取代理IP
    2.3检测代理Ip（代理Ip检测模块）
    2.4如果可用，写入数据库，（数据库模块）
    2.5处理异常，防止一个爬虫出错了，影响其他爬虫
"""

class RunSpiders(object):

    def __init__(self):
    #     创建mongo_pool对象
        self.mongo_pool = MongoPool

    def get_spider_from_settings(self):
         # 2.1根据配置文件信息，获取爬虫对象列表
    #         遍历配置文件中的爬虫信息，获取每个爬虫全类名
        for full_class_name in PROXIES_SPIDERS:
            # 'core.proxy_spider.proxy_spiders.Ip66Spider',
    #         获取模块名和类名
            module_name,class_name = full_class_name.rsplit('.',maxsplit=1)
    #         根据模块名和类名导入类
            module = importlib.import_module(module_name)
    #         根据类名，从模块中，获取类
            cls = getattr(module,class_name)
    #         创建爬虫对象
            spider = cls()
            yield  spider


    # 2.1根据配置文件信息，获取爬虫对象列表
    def run(self):
        spiders = self.get_spider_from_settings()
        # 2.2遍历爬虫对象列表，获取爬虫对象，遍历爬虫对象的get_proxies方法，获取代理IP
        for spider in spiders:
#             遍历爬虫对象的get_proxies方法，获取代理IP

            # 2.5处理异常，防止一个爬虫出错了，影响其他爬虫
            try:
                for proxy in spider.get_proxies():
                    # 2.3检测代理Ip（代理Ip检测模块）
                    proxy = check_proxy(proxy)
                    # 2.4如果可用，写入数据库，（数据库模块）
                    # 如果speed不是-1，就说明可用
                    if proxy.speed != -1:
                        self.mongo_pool.insert_one(proxy)
            except Exception as ex:
                logger.exception(ex)

if __name__=='__main__':
    rs = RunSpiders()
    rs.run()
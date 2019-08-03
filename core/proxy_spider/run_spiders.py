# 打猴子补丁
from gevent import monkey
monkey.patch_all()
# 导入协程池
from gevent.pool import Pool

from settings import  PROXIES_SPIDERS
import importlib
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
import schedule
import time
from settings import RUN_SPIDERS_INTERVAL


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
3,使用异步来执行每一个爬虫任务，以提高代理爬虫的计算效率
    3.1 在init方法中创建协程池对象
    3.2 把处理有一个代理爬虫的代码抽到一个方法
    3.3 使用异步执行这个方法
    3.4 调用协程的join方法，让当前线程等到协程任务的完成
4.使用schedule模块，实现每个一定的时间，执行一次爬虫任务
    4.1 定义一个start的类方法
    4.2 创建当前类的对象，调用run方法
    4.3 使用schedule模块，每个一定的时间，执行当前对象的run方法。
"""

class RunSpiders(object):

    def __init__(self):
    #     创建mongo_pool对象
        self.mongo_pool = MongoPool()
#        3.1 在init方法中创建协程池对象
        self.coroutine_pool = Pool()

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
#            3.3 使用异步执行这个方法
            self.coroutine_pool.apply_async(self._execute_one_spider_task,args=(spider,))
#        3.4 调用协程的join方法，让当前线程等到协程任务的完成
        self.coroutine_pool.join()
    def _execute_one_spider_task(self,spider):
            # 2.5处理异常，防止一个爬虫出错了，影响其他爬虫
            try:
                for proxy in spider.get_proxies():
                    # self.mongo_pool.insert_one(proxy = proxy)
                    # 2.3检测代理Ip（代理Ip检测模块）
                    proxy = check_proxy(proxy)
                    # 2.4如果可用，写入数据库，（数据库模块）
                    # 如果speed不是-1，就说明可用
                    logger.info('{}:{}的速度是{}'.format(proxy.ip,proxy.port,proxy.speed))
                    if proxy.speed != -1:
                        self.mongo_pool.insert_one(proxy = proxy)
            except Exception as ex:
                logger.exception(ex)

    @classmethod
    def start(cls):
    # 4.使用schedule模块，实现每个一定的时间，执行一次爬虫任务
    # 4.1 定义一个start的类方法
    # 4.2 创建当前类的对象，调用run方法
        rs = RunSpiders()
        rs.run()
    # 4.3 使用schedule模块，每个一定的时间，执行当前对象的run方法。
        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(rs.run)
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__=='__main__':
    RunSpiders.start()
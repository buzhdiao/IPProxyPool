import requests
import time
from lxml import etree
from utils.log import logger

from domain import Proxy
from utils.http import get_request_headers

"""
8.3 实现通用爬虫
目标：实现可以指定不同URL列表，分组的XPATH和详情的XPATH，从不同页面上提取代理的IP，端口号和区域的通用爬虫
步骤：
1.在base-spider.py文件中，定义一个BaseSpider类，集成自Object
2，提供三个类成员变量
    urls：代理Ip网址的URL列表
    group_xpath:分组xpath,获取包含代理IP信息标签列表的XPATH
    detail_xpath：组内xpath,获取代理Ip详情的信息xpath,格式是{'ip':'xx','port':'xx','area':'xx'}
3. 提供初始方法，传入爬虫URL列表，分组Xpath，详情（组内）Xpath，
4. 对外提供一个获取代理Ip的方法

"""
class BaseSpider(object):

    # 2，提供三个类成员变量
    # urls：代理Ip网址的URL列表
    urls =[]
    # group_xpath:分组xpath,获取包含代理IP信息标签列表的XPATH
    group_xpath=''
    # detail_xpath：组内xpath,获取代理Ip详情的信息xpath,格式是{'ip':'xx','port':'xx','area':'xx'}
    detail_xpath = {}


    # 3.提供初始方法，传入爬虫URL列表，分组Xpath，详情（组内）Xpath，
    def __init__(self,urls=[],group_xpath='',detail_xpath={}):
        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self,url):
        ''''根据URL，发送请求，获取页面数据'''
#        time.sleep(5)
        headers = get_request_headers()
#        print(headers)
        response = requests.get(url,headers=headers)
        if response.status_code !=200:
#        charset_ = response.encoding
            print(response.status_code)
            logger.info("爬取{}网页时出现{}错误".format(url,response.status_code))
        logger.info("爬取{}网页成功。".format(url))
        return response.content

    def get_first_from_list(self,lis):
    #     如果列表中有元素就返回第一个，否则返回空串
        return lis[0] if len(lis)!=0  else ''

    def get_proxies_from_page(self,page):
        '''解析页面，提取数据，封装为Proxy对象'''
        element = etree.HTML(page)
    #     获取包含代理IP信息的标签列表
        trs = element.xpath(self.group_xpath)
    #     遍历trs,获取代理Ip相关信息
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip,port,area=area)
            yield proxy

    def get_proxies(self):
        # 4. 对外提供一个获取代理Ip的方法
        # 4.1 遍历URL列表，获取URL
        for url in self.urls:
            try:
                # 4.2 根据发送请求，获取页面数据
                page = self.get_page_from_url(url)
                # 4.3 解析页面，提取数据，封装为Proxy对象
                proxies = self.get_proxies_from_page(page)
                # 4.4 返回Proxy对象列表
                yield from proxies
            except :
                logger.info("{}爬取出现错误。".format(url))

if __name__=='__main__':

    # 西刺代理的测试
    '''
    config = {
       'urls': ['http://www.xicidaili.com/{}/{}/'.format(types,i) for types in ['nn','nt','wn','wt'] for i in range(1, 11)],
       'group_xpath':'//*[@id="list"]/table/tbody/tr',
       'detail_xpath':{
           'ip':'td[1]/text()',
           'port':'td[2]/text()',
           'area':'td[5]/text()',
       }
    }
    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)
    '''

     # ip3366代理
    '''
    config = {
        'urls':['http://www.ip3366.net/free/?stype={}&page={}'.format(j,i) for j in range(1,5) for i in range(1,8)],
        'group_xpath':'//*[@id="list"]/table/tbody/tr',
        'detail_xpath':{
            'ip':'td[1]/text()',
            'port':'td[2]/text()',
            'area':'td[5]/a/text()',
        }
        }
    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)
    '''

#     快代理
    config = {
        'urls':['http://www.kuaidaili.com/free/{}/{}/'.format(types,i) for types in ['inha','intr'] for i in range(1, 30)],
        'group_xpath':'//*[@id="list"]/table/tbody/tr',
        'detail_xpath':{
            'ip':'td[1]/text()',
            'port':'td[2]/text()',
            'area':'td[5]/text()',
        }
        }
    count =0
    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        count = count +1
        print(proxy)
    print(count)



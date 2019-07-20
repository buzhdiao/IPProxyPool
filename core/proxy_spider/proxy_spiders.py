from core.proxy_spider.base_spider import  BaseSpider
import time
import random
import re
import js2py
"""
实现西刺代理爬虫，http://www.xicidaili.com
定义一个类，继承通用爬虫类（basespider)
提供urls,group-xpath和detail_xpath
"""

class XiciSpider(BaseSpider):

    # 准备URL列表
    urls = ['http://www.xicidaili.com/nn/{}'.format(i) for i in range(1,11)]

    # 分组xpath，用于获取包含代理Ip信息的标签列表
    # //*[@id="ip_list"]/tbody
    group_xpath = '//*[@id="ip_list"]/tbody/tr[position()>1]'
    # 组内的XPath,用于提取ip,port,area
    # //*[@id="ip_list"]/tbody/tr[2]/td[2]
    # //*[@id="ip_list"]/tbody/tr[3]/td[2]
    # //*[@id="ip_list"]/tbody/tr[3]/td[3]
    detail_xpath = {
        'ip':'td[2]/text()',
        'port':'td[3]/text()',
        'area':'td[4]/a/text()'
    }


"""
实现IP3366代理爬虫，http://www.ip3366.net
定义一个类，继承通用爬虫类（basespider)
提供urls,group-xpath和detail_xpath
"""
class Ip3366Spider(BaseSpider):

    # 准备URL列表
    urls = ['http://www.ip3366.net/free/style={}&page={}'.format(i,j) for i in range(1,4,2) for j in range(1,8)]

    # 分组xpath，用于获取包含代理Ip信息的标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的XPath,用于提取ip,port,area
    detail_xpath = {
        'ip':'td[1]/text()',
        'port':'td[2]/text()',
        'area':'td[4]/text()'
    }

"""
实现快代理代理爬虫，http://www.kuaidaili.com/free/inha/1/
定义一个类，继承通用爬虫类（basespider)
提供urls,group-xpath和detail_xpath
"""
class KuaiSpider(BaseSpider):

    # 准备URL列表
    urls = ['http://www.kuaidaili.com/free/ihna/{}'.format(i) for i in range(1,6,2)]

    # 分组xpath，用于获取包含代理Ip信息的标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # 组内的XPath,用于提取ip,port,area
    detail_xpath = {
        'ip':'td[1]/text()',
        'port':'td[2]/text()',
        'area':'td[4]/text()'
    }

"""
实现Proxylistplus代理爬虫，http:/list.proxylistplus.com/Fresh-Http-Proxy-List-{}
定义一个类，继承通用爬虫类（basespider)
提供urls,group-xpath和detail_xpath
"""
class ProxylistplusSpider(BaseSpider):

    # 准备URL列表
    urls = ['http:/list.proxylistplus.com/Fresh-Http-Proxy-List-{}'.format(i) for i in range(1,4)]

    # 分组xpath，用于获取包含代理Ip信息的标签列表
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    # 组内的XPath,用于提取ip,port,area
    detail_xpath = {
        'ip':'td[2]/text()',
        'port':'td[3]/text()',
        'area':'td[5]/text()'
    }

    def get_page_from_url(self,url):
        time.sleep(random.uniform(1,3))
        # 调用父类方法，发送请求，获取数据
        return super().get_page_from_url(url)

if __name__=='__main__':
    spider = XiciSpider()
    for proxy in spider.get_proxies():
        print(proxy.ip)
    # print(Ip3366Spider.urls)


    url = 'http://www.66ip.cn/html'
    headers ={
        ''
    }
    response = requests.get(url,headers = headers)
    print(response.status_code)
    print(response.content.decode('GBK'))

    result = re.findadd('windows.onload=setTimeout\("(.+?)",200\);\s*(.+?)\s*<script>',text)
    print(result)
    # 希望执行js的时候，返回真正要执行的js
    # 把'eval("qo=eval;qo(po)'替换为return po
    func_str =  result[0][1]
    func_str = func_str.replace('eval("qo=eval;qo(po);','return po')
    print(func_str)
    # 获取执行js的环境
    context = js2py.EvalJS()
    # 加载执行func_str
    context.execute(func_str)
    # 执行这个函数，生产需要的js
    # code=gv(50)
    context.execute('code={}'.format(result[0][0]))
    # 打印生成的代码
    print(context.code)

    cookie_str =re.findall()
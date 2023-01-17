from bdpycmd.cmd.factory import base
from crontaber.tasks import spider_webdriver


class Command(base.BaseCommand,spider_webdriver.spider_webdriver):
    def __init__(self):
        super().__init__(name=self.__class__.__module__,alias='爬虫测试',description='爬取51Job的工作列表\n运行该爬虫需要下载安装chrome浏览器及chromedriver')
        super(base.BaseCommand,self).__init__()
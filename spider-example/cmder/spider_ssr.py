from bdpycmd.cmd.factory import base
from crontaber.tasks import spider_ssr


class Command(base.BaseCommand,spider_ssr.spider_ssr):
    def __init__(self):
        super().__init__(name=self.__class__.__module__,alias='爬虫测试',description='爬取电影数据网站电影目录')
        super(base.BaseCommand,self).__init__()
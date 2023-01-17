from bdpycmd.cmd.factory import base
from crontaber.tasks import spider_ajax


class Command(base.BaseCommand,spider_ajax.spider_ajax):
    def __init__(self):
        super().__init__(name=self.__class__.__module__,alias='爬虫测试',description='爬取小说列表描述信息')
        super(base.BaseCommand,self).__init__()
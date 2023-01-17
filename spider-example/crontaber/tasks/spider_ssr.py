import threading,os,requests,random,traceback,time
from pyquery import PyQuery as pq
from bdpycmd.cmd.factory import base

class spider_ssr:
    """
    爬虫，服务端渲染html练习
    获取电影列表
    """
    def __init__(self):
        #线程锁
        self.__lock = threading.RLock()
        #视频列表首页地址
        self.__video_page_index_url = 'https://ssr1.scrape.center/page/%s'
        #当前页数
        self.__current_page = 0
        #是否结束
        self.__is_over = False
        #爬取内容缓存
        self.__current_content = []
        #内容存储路径
        self.__video_content_save_path = '../../storage/out/spider_ssr.txt'
        #成功码
        self.__success_code = [200,302,304]
        #最大页码
        self.__max_page = 100
        #是否是第一次写入
        self.__first_write = True
    
    def __save(self):
        """
        保存已经爬取到的内容
        :param first: bool 是否是第一次写入
        :return:
        """
        more_rows = True
        while more_rows:
            #是否是最后一次存储
            if self.__is_over:
                more_rows = False
            
            #当数据拉取结束，或者内容大于20行的时候进行存储
            if self.__is_over or len(self.__current_content) >= 20:
                #判断写入模式
                if self.__first_write:
                    mode = 'w'
                    self.__first_write = False
                else:
                    mode = 'a'
                
                print('mode >>',mode)

                #当前内容加锁
                self.__lock.acquire()
                
                #处理内容写入
                with open(self.__video_content_save_path,mode=mode,encoding='utf-8') as f:
                    for content in self.__current_content:
                        content_fmt = """
                        名称:{name}
                        类型:{type}
                        地区:{area}
                        时间:{tm}
                        """.format(
                            name = content['name'],
                            type = content['type'],
                            area = content['area'],
                            tm = content['area']
                        )
                        print('write >>',content_fmt)
                        f.write(content_fmt)
                
                #解锁
                self.__lock.release()
                f.close()
             
            #等待一会
            time.sleep(0.1)
    
    def __random_header(self):
        """
        获取合适的header头
        :return: dict 
        """
        ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        ]
        headers = {
            'user-agent':random.choice(ua)
        }
        return headers
    
    def __get_page(self):
        """
        分配页码
        :return: int 页码
        """
        self.__lock.acquire()
        self.__current_page += 1
        page = self.__current_page
        if self.__current_page >= self.__max_page:
            self.__is_over = True
        self.__lock.release()
        return page

    def __rand_sleep(self,base:int,rad:float):
        """
        随机随
        :param base: int 基础秒数
        :param rad: float 随机秒数
        :return:
        """
        ts = base + random.random() * rad
        time.sleep(ts)
    
    def __get_content(self):
        """
        内容拉取
        :return:
        """
        while not self.__is_over:
            #获取页码
            page = self.__get_page()
            print('page >',page)
            print('over >',self.__is_over)
            #格式化url
            url = self.__video_page_index_url % str(page)
            #随机睡眠
            self.__rand_sleep(0.5, 1)
            
            #获取内容页
            try:
                resp = requests.get(url=url,headers=self.__random_header(),timeout=20)
                if resp.status_code not in self.__success_code:
                    self.__is_over = True
                else:
                    #提取视频信息列表
                    dom = pq(resp.content)
                    video_list = dom('#index > div:nth-child(1) > div:nth-child(1)').children('div.el-card.item').items()
                    
                    #遍历提取内容
                    content_list = []
                    for video in video_list:
                        video_content = video('div.el-card__body > div.el-row > div:nth-child(2)')
                        tmp = {
                            'name':video_content.children('a.name').text().strip(),
                            'type':video_content.children('div.categories').text().strip(),
                            'area':video_content.children('div.m-v-sm.info').eq(0).text().strip(),
                            'tm':video_content.children('div.m-v-sm.info').eq(1).text().strip()
                        }
                        content_list.append(tmp)
                    
                    #更新到当前内容中
                    if len(content_list) > 0:
                        self.__lock.acquire()
                        self.__current_content.extend(content_list)
                        print('__current_content len >>',len(self.__current_content))
                        self.__lock.release()
            except:
                print(traceback.format_exc())
                self.__is_over = True
    
    @base.BaseCommand.as_cmder
    def run(self,num:int=4):
        """
        调起爬虫
        :param num: int 启动线程数
        :return:
        """
        thread_s = []
        
        #添加爬取线程
        for i in range(int(num)):
            thread_s.append(threading.Thread(target=self.__get_content))
        
        #添加存储线程
        thread_s.append(threading.Thread(target=self.__save))
        
        #线程开启
        for thd in thread_s:
            thd.setDaemon(True)
            thd.start()
        
        #主线程阻塞
        for thd in thread_s:
            thd.join()
        
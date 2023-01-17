import threading,requests,asyncio,aiohttp,json,traceback,random,time
from bdpycmd.cmd.factory import base

class spider_ajax:
    """
    爬虫，客户端渲染html练习，异步io
    获取小说内容介绍
    """
    def __init__(self):
        #线程锁
        self.__lock = threading.RLock()
        #封面列表接口
        self.__book_list_api = 'https://spa5.scrape.center/api/book/'
        #当前封面列表页码
        self.__current_page = 0
        #书本总数
        self.__book_count = 0
        #分页行数
        self.__book_per_page = 20
        #封面列表是否拉取完毕
        self.__is_book_list_over = False
        #书本ID集合
        self.__current_book_ids = []
        #内容介绍接口
        self.__book_describe_api = 'https://spa5.scrape.center/api/book/%s'
        #当前已获取书本信息
        self.__current_books = {}
        #信息获取是否结束
        self.__is_done = False
        #成功码
        self.__success_code = [200,302,304]
    
    def __random_header(self):
        """
        获取合适的header头
        :return: dict 
        """
        ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        ]
        headers = {
            'user-agent':random.choice(ua),
            'accept':'application/json'
        }
        return headers

    def __rand_sleep(self,base:int,rad:float):
        """
        随机随
        :param base: int 基础秒数
        :param rad: float 随机秒数
        :return:
        """
        ts = base + random.random() * rad
        time.sleep(ts)
    
    def __get_page(self):
        """
        分配页码
        :return: int 页码
        """
        self.__lock.acquire()
        if self.__is_book_list_over:
            return self.__current_page
        else:
            self.__current_page += 1
            page = self.__current_page
        self.__lock.release()
        return page
    
    def __get_book_list(self):
        """
        获取书本列表
        :return:
        """
        while not self.__is_book_list_over:
            #分页
            page = self.__get_page()
            print('page >',page)
            print('book_count >',self.__book_count)
            
            #参数准备
            params = {
                'offset':page - 1,
                'limit':self.__book_per_page
            }
            self.__rand_sleep(0.4, 1)
            
            #书本列表获取
            try:
                resp = requests.get(url=self.__book_list_api,params=params,headers=self.__random_header(),timeout=20)
                #状态码不对标记结束
                if resp.status_code not in self.__success_code:
                    self.__is_book_list_over = True
                    break
                
                #解析数据
                res = resp.json()
                
                book_ids = []
                for book in res['results']:
                    book_ids.append(book['id'])
                
                #数据更新
                self.__lock.acquire()
                #更新当前书本ID列表
                self.__current_book_ids.extend(book_ids);
                #更新书本总数目
                if self.__book_count <= 0:
                    self.__book_count = res['count']
                #判断是否结束
                if self.__current_page * self.__book_per_page >= self.__book_count:
                    self.__is_book_list_over = True
                self.__lock.release()
            except Exception as e:
                #异常标记结束
                self.__is_book_list_over = True
                print('书本列表拉取异常 >>',str(e))
    
    def __get_book_conetnts(self):
        """
        获取书本内容
        :return:
        """
        #开启携程获取内容
        asyncio.run(self.__aio_http_get_books())
    
    async def __aio_http_get_books(self):
        """
        异步获取书本内容
        :return:
        """
        more_book = True
        while more_book:
            #退出循环条件
            if self.__is_book_list_over:
                more_book = False

            #取出10条ID来查询信息
            self.__lock.acquire()
            book_len = len(self.__current_book_ids)
            if book_len >= 10:
                book_ids = self.__current_book_ids[-10:]
                self.__current_book_ids = self.__current_book_ids[0:book_len-10]
            else:
                book_ids = self.__current_book_ids
                self.__current_book_ids = []
            
            print('获取前书本ID数目 >>',book_len)
            print('获取后书本数目 >>',len(self.__current_book_ids))
            self.__lock.release()
            
            #异步http获取书本信息
            tasks = []
            for book_id in book_ids:
                tasks.append(asyncio.create_task(self.__get_book(book_id)))
            
            #等待完成
            for task in tasks:
                await task

            #等待下次循环
            time.sleep(0.01)
    
    async def __get_book(self,book_id:str):
        """
        异步获取书本内容
        :param book_ids: list 书本ID列表
        :return:
        """
        try:
            url = self.__book_describe_api % str(book_id)
            async with aiohttp.request('GET',url=url,headers=self.__random_header()) as resp:
                await asyncio.sleep(0.3 + random.random() * 0.5)
                book = await resp.json()
                book_content = """
                名称:{name}
                简介:{introduce}
                类型:{type}
                作者:{author}
                评论:{comments}
                """.format(
                    name=book['name'],
                    introduce = book['introduction'],
                    type=' '.join(book['tags']),
                    author= ' '.join(book['authors']),
                    comments = self.__mk_comments(book['comments'])
                )
                print('book content >>',book_content)
        except Exception as e:
            print("内容拉取异常 >>",str(e))
            
    
    def __mk_comments(self,comments:list):
        """
        评论列表转字符串
        :comments comments: list 评论列表
        :return: str
        """
        if not comments:
            return ''
        
        coms = []
        for comment in comments:
            coms.append(comment['content'])
        
        return '\n'.join(coms)
    
    @base.BaseCommand.as_cmder
    def run(self,num:int):
        """
        运行入口
        :param num: int 列表爬取进程数
        :return:
        """
        thread_s = []
        
        #添加信息获取
        thread_s.append(threading.Thread(target=self.__get_book_conetnts))
        
        #添加爬取线程
        for i in range(int(num)):
            thread_s.append(threading.Thread(target=self.__get_book_list))
        
        #线程开启
        for thd in thread_s:
            thd.setDaemon(True)
            thd.start()
        
        #主线程阻塞
        for thd in thread_s:
            thd.join()
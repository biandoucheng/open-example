import random,time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Expd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from cmder.factory.base import BaseCommand
from bdpycmd.cmd.factory import base

class spider_webdriver:
    """
    爬虫，浏览器驱动练习，解决js无法反解析的情况，在接口中及html文档中发现不了数据的情况
    爬取51Job工作信息
    运行该爬虫需要下载安装chrome浏览器及chromedriver
    chromedriver 需要根据你的chrome版本选择正确的安装版本
    chromedriver 地址:http://npm.taobao.org/mirrors/chromedriver/
    """
    def __init__(self):
        #浏览器驱动
        self.__driver = None
        
        #设置浏览器选项
        self.__driver_opts = webdriver.ChromeOptions()
        self.__driver_opts.add_argument('user-agent=' + self.__random_ua())
        self.__driver_opts.add_argument('--ignore-certificate-errors')
        self.__driver_opts.add_argument('--ignore-ssl-errors')
        self.__driver_opts.add_argument('--log-level=3')
        # self.__driver_opts.add_argument('--headless')
        # self.__driver_opts.add_argument('--no-sandbox')
        # self.__driver_opts.add_argument('--disable-gpu')
        
        #51官网地址
        self.__index_url = 'https://www.51job.com/'
        
        #窗口适配
        self.__window_size = (1850,1080)
        
        #停止执行
        self.__stop = False

    def __start_webdriver(self):
        """
        启动web浏览器
        :retun:
        """
        self.__driver = webdriver.Chrome(chrome_options=self.__driver_opts)
        self.__driver.implicitly_wait(10)
    
    def __random_ua(self):
        """
        获取UA
        :return: str
        """
        ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        ]
        return random.choice(ua)
    
    def __open_index_page(self):
        """
        打开首页，并配置窗口合适
        :return:
        """
        #打开首页
        self.__driver.get(self.__index_url)
        #重置窗口宽高
        self.__driver.set_window_size(width=self.__window_size[0], height=self.__window_size[1])
        #调整窗口坐标原点 非必须，保证窗口正常填充就行
        self.__driver.set_window_position(x=-5,y=0)
        #等待确认打开完成 <搜索按钮出现并可点击>
        WebDriverWait(self.__driver, 10).until(Expd.element_to_be_clickable((By.CSS_SELECTOR,'body > div.content > div > div.fltr.radius_5 > div > button')))
    
    def __enter_position_page(self):
        """
        进入职位搜索页
        :return:
        """
        #捕获 <职位搜索> 标题
        search_position_title = self.__driver.find_element(By.CSS_SELECTOR,'#topIndex > div > p > a:nth-child(2)')
        
        #点击进入
        search_position_title.click()
        
        #等待新页面出现 <搜索按钮出现并可点击>
        WebDriverWait(self.__driver, 10).until(Expd.element_to_be_clickable((By.CSS_SELECTOR,'#search_btn')))
    
    def __range_city_index(self):
        """
        获取城市列表
        :return:
        """
        #滑动到页面顶部
        self.__to_top()
        
        #获取城市列表
        city_list_s = self.__driver.find_elements(By.CSS_SELECTOR,'body > div:nth-child(4) > div.j_filter > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div.region > div.clist.gray > a')
       
        #删除 <全部|热门>选项 这里只是为了展示遍历点击的情况，实际操作中有全部的话没必要一个个点
        if len(city_list_s) > 0:
            del city_list_s[0:2]
        
        #返回城市索引
        for index in range(len(city_list_s)):
            yield index + 2
    
    def __city_click(self,index:int):
        """
        点击城市按钮
        :param index: int 城市索引
        :return:
        """
        #滑动到页面顶部
        self.__to_top()
        
        #计算城市的nth-child索引
        nth_index = str(index + 1)
        target_city_css = 'body > div:nth-child(4) > div.j_filter > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div.region > div.clist.gray > a:nth-child(%s)' % nth_index
        
        #捕捉并点击城市
        city = self.__driver.find_element(By.CSS_SELECTOR,target_city_css)
        city.click()
        
        #等待点击结果
        time.sleep(1)
        
        #确定点击结果正确
        times = 5
        while times > 0:
            #检测目标城市是否被选中
            n_city = self.__driver.find_element(By.CSS_SELECTOR,target_city_css)
            n_city_class = n_city.get_attribute('class')
            if 'on' in n_city_class or 'mk' in n_city_class:
                return True
            #延时等待完全加载
            time.sleep(0.5)
            times -= 1
        else:
            return False
    
    def __to_top(self):
        """
        滑动到页面顶部
        :return:
        """
        print("滑动到页面顶部 >>>")
        js_scripts = 'var q=document.documentElement.scrollTop=0'
        self.__driver.execute_script(js_scripts)
        time.sleep(0.5)
    
    def __analysis_page_content(self):
        """
        解析当前页面内容
        :return:
        """
        #获取工作列表
        index = 0
        work_lists = self.__driver.find_elements(By.CSS_SELECTOR,'body > div:nth-child(4) > div.j_result > div > div.leftbox > div:nth-child(4) > div.j_joblist > div.e')
        for work in work_lists:
            index += 1
            left_content = work.find_element(By.CSS_SELECTOR,'a.el')
            right_content = work.find_element(By.CSS_SELECTOR,'div.er')
            
            content_fmt = """
            行数:{index}
            城市:{city}
            公司:{company}
            类型:{type}
            产品:{product}
            岗位:{position}
            薪资:{salary}
            """.format(
                index = str(index),
                city = left_content.find_element(By.CSS_SELECTOR,'p.info').find_element(By.XPATH,'span[2]').text.split('|')[0],
                company = right_content.find_element(By.CSS_SELECTOR,'a.cname.at').text,
                type = right_content.find_element(By.CSS_SELECTOR,'p.dc.at').text,
                product = right_content.find_element(By.CSS_SELECTOR,'p.int.at').text,
                position = left_content.find_element(By.CSS_SELECTOR,'p.t').text.replace('\n',' '),
                salary = left_content.find_element(By.CSS_SELECTOR,'p.info').text.replace('\n',' ')
            )
            print(content_fmt)
    
    def __to_bottom(self):
        """
        滑动到页面底部
        :return:
        """
        print("滑动到页面底部 >>")
        js_scripts = 'var q=document.documentElement.scrollTop=10000'
        self.__driver.execute_script(js_scripts)
        time.sleep(0.3)
    
    def __range_page(self):
        """
        遍历页码
        :return: bool 是否遍历成功
        """
        #滑动页面到底部
        self.__to_bottom()
        
        #查找分页按钮
        next_s = self.__driver.find_elements(By.CSS_SELECTOR,'div.p_in > ul > li.next')
        if len(next_s) <= 0:
            return False
        
        #判断是否分页结束
        next = next_s[0]
        if 'bk' in next.get_attribute('class'):
            return False
        
        #点击分页按钮
        next.click()
        
        #判断点击完成
        time.sleep(0.5)
        WebDriverWait(self.__driver, 10).until(Expd.element_to_be_clickable((By.CSS_SELECTOR,'#search_btn')))
        return True
    
     @base.BaseCommand.as_cmder
    def range_51_jobs(self):
        """
        遍历51job 工作内容
        :return:
        """
        #初始化浏览器
        self.__start_webdriver()
        
        #进入51Job主页
        self.__open_index_page()
        
        #进入工作页面
        self.__enter_position_page()
        
        #开始获取工作列表
        for city_index in self.__range_city_index():
            ok = self.__city_click(city_index)
            if not ok:
                print('城市选择失败 >>',city_index)
                break
            more_page = True
            while more_page:
                self.__analysis_page_content()
                more_page = self.__range_page()



def run():
    """
    任务调度入口
    """
    spider_webdriver().range_51_jobs()
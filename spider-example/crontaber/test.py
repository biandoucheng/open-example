import requests

sess = requests.session()
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
resp = sess.get(url='https://www.baidu.com')
# text = resp.content.decode('gbk')
# resp.encoding = 'gbk'
print('encoding >>',resp.encoding)
print('text >>',str(resp.content,encoding='gbk'))
print('over >>')
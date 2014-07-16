'''
Created on Jul 17, 2014

@author: zsy
'''
import urllib.request

url = "http://www.youku.com"
'''
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
}
'''
headers = {'User-agent':'Mozilla/5.0',
           'cache-control':'no-cache',
           'accept':'*/*'
           }


req = urllib.request.Request(url);
#req.add_header('User-agent', 'Mozilla/5.0')
#req.add_header('cache-control', 'no-cache')
#req.add_header('accept', '*/*')
for k, v in headers.items():
    print(k, v)
    req.add_header(k, v)
r = urllib.request.urlopen(req)
data = r.read()


'''
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
data = opener.open(url).read()
'''
print(data)
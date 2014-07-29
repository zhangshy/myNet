'''
使用urllib接口获取网页，将图片保存
Created on Jul 17, 2014

@author: zsy
'''
import urllib.request
import time
import os
from html.parser import HTMLParser
import argparse
import re
import json
import random


filePath = "/home/zsy/lqbz/pictures/"

'''
像jpg、png等都是3个字节，将tag是img，开头为http，倒数第四个字节为'.'的当作图片
'''
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global index
        global filePath
        if tag=="img":            
            if attrs[0][0]=="src" or attrs[0][0]=="r_src":
                url = attrs[0][1]
                if (url.startswith("http")):
                    if url[-4:-3]=='.':
                        fileNameindex = url.rfind("/")
                        fileName = url[fileNameindex:]
                        fileName = filePath + fileName
                        urllib.request.urlretrieve(url, fileName)
                        print(".", end=" ")
                

##根据charset=选项确定编码方式
def getEncodeType(context):
    str = ""
    for i in context[0:200]:
        str += chr(i)
    print(str)
    target = "charset="
    decodeType="UTF-8"
    index1 = str.find(target)
    if index1!=-1:
        index2 = str.find("\"", index1)
        if index2!=-1:
            decodeType = str[index1+len(target): index2]
            print(decodeType)
            if decodeType=="gb2312":
                decodeType = "gbk"  #GB2312是中国规定的汉字编码，也可以说是简体中文的字符集编码;
                                    #GBK 是 GB2312的扩展 ,除了兼容GB2312外，它还能显示繁体中文，还有日文的假名
    return decodeType

'''
创建文件保存路径
'''
def creatOutPath():
    global filePath
    localDir = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime()) #获取当前时间
    filePath = filePath + localDir;
    if not os.access(filePath, os.R_OK):
        print("目录不存在")
        os.mkdir(filePath, mode=0o777)        
'''
获取url内容
'''
def getUrlContext(url):
    headers = {
               #'Accept-Encoding': 'gzip',
               'Accept-Charset': 'ISO-8859-1,utf-8',
               'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection': "keep-alive",
               'Accept-Language': 'en-US',
               'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B146 Safari/8536.25'
               }
    req = urllib.request.Request(url)
    for k, v in headers.items():
        #print(k, v)
        req.add_header(k, v)
    r = urllib.request.urlopen(req)
    context = r.read()
    decodeType=getEncodeType(context)
    data = context.decode(decodeType)   #使用gbk还是utf-8看具体内容。youku使用decode("UTF-8")
    return data

##获取youku视频链接信息
def getVideoInfo(url):  
    ruleTitle=re.compile('<title>(.*)</title>')  
    ruleId=re.compile('http://v.youku.com/v_show/id_(.*).html')  
    videoTitle=ruleTitle.findall(urllib.request.urlopen(url).read().decode('utf8'))  
    videoId=ruleId.findall(url)  
    return videoTitle[0],videoId[0]

def getTrueLink(videoid):  
    data=urllib.request.urlopen('http://v.youku.com/player/getPlayList/VideoIDS/'+videoid)  
    info=json.loads(data.read().decode('utf8'))  
  
    segs=info['data'][0]['segs']  
    types=segs.keys()  
  
    seed=info['data'][0]['seed']  
    source=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890")  
    mixed=''  
    while source:  
        seed=(seed*211+30031)&0xFFFF  
        index=seed*len(source)>>16  
        c=source.pop(index)  
        mixed+=c  
  
    ids=info['data'][0]['streamfileids']['flv'].split('*')[:-1]  
    vid=''.join(mixed[int(i)] for i in ids)  
  
    sid='%s%s%s'%(int(time.time()*1000),random.randint(1000,1999),random.randint(1000,9999))  
  
    urls=[]  
    for s in segs['flv']:  
        no='%02x'%int(s['no'])  
        url='http://f.youku.com/player/getFlvPath/sid/%s_%s/st/flv/fileid/%s%s%s?K=%s&ts=%s'%(sid,no,vid[:8],no.upper(),vid[10:],s['k'],s['seconds'])  
        urls.append(url)  
    return urls  
  
def down2file(urls,filename):  
    f=open(filename,'wb')  
    fileNum=len(urls)  
    count=0  
    for url in urls:  
        count+=1  
        print('downloading file %d/%d'%(count,fileNum))  
        req=urllib.request.Request(url,headers={'Referer':'http://www.youku.com'})  
        data=urllib.request.urlopen(req).read()  
        f.write(data)  
    f.close()  
    print('download '+filename+' OK!')
    
'''
参考网络代码：http://blog.csdn.net/littlethunder/article/details/18230859
'''    
def youkuDown(link):  
    videotitle,videoid=getVideoInfo(link)
    print(videoid, videotitle)  
    urls=getTrueLink(videoid)  
    for url in urls:
        print(url)
#    down2file(urls,videotitle+'.flv')    ###未成功，暂时不下载。
    
if __name__=="__main__":  
    url = "http://news.baidu.com/"
    #url = "http://www.youku.com/"
    global filePath
    ##命令行参数解析
    parser = argparse.ArgumentParser(description="处理网页内容")
    parser.add_argument('-u', '--url', dest="url", help="要访问的网页url")
    parser.add_argument('-o', '--output', dest="filePath", help="文件要保存的路径")
    parser.add_argument('--image', action='store_true', help="使用保存图片操作")
    parser.add_argument('--youku', action='store_true', help="保存youku视频")
    argRet = parser.parse_args()
    print(argRet)
    #使用命令行中的参数
    url = argRet.url if argRet.url!=None else url   
    filePath = argRet.filePath if argRet.filePath!=None else filePath
    print(url, filePath)
    
    if argRet.youku:
        youkuDown(url)
    
    if argRet.image:
        data = getUrlContext(url)
        creatOutPath()
        parser = MyHTMLParser()
        parser.feed(data)
        
    print("fun end")
    

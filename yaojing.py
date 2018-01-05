#coding:utf-8
import requests
import re
from lxml import etree
import os
import time
#使用多线程
import threading
#随机数
import random

#使用进程
# from multiprocessing import Process

import chardet

#网址 http://manhua.fzdm.com/27/
#漫画http://manhua.fzdm.com/27/509/
#翻页http://manhua.fzdm.com/27/509/index_0.html

#链接//*[@id="content"]/li[5]/a/@href
#名字//*[@id="content"]/li[5]/a/

class bookListFZDM(object):
    def __init__(self):
        self.headers = [
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 "},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50"},
            {"User-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET "},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) "},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"},
        ]

    def findList(self):
        # http://manhua.fzdm.com/在线漫画
        #爬取所有链接
        #爬取所有可看漫画名字
        response = requests.get("http://manhua.fzdm.com/", headers=self.headers[random.randint(0,9)])
        selector = etree.HTML(response.text)
        #获取所有漫画链接
        bookLinks = selector.xpath('//*[@id="mhmain"]/ul/div/li/a/@href')
        #获取所有漫画名字
        bookNames = selector.xpath('//*[@id="mhmain"]/ul/div/li/a/@title')
        bookFindName = raw_input("请输入你要下载的动漫名称(格式：“xxxx漫画”，例如：火影忍者漫画)：")
        #返回的两值
        reNameEncode = ""
        reLinkEncode = ""
        #设一个标签，判断是否已经找到漫画
        findFlag = 0
        for link, name in zip(bookLinks, bookNames):
            nameEncode = name.encode('utf-8')
            linkEncode = link.encode('utf-8')
            if bookFindName == nameEncode:
                print "已找到漫画",linkEncode, nameEncode
                reNameEncode = nameEncode
                reLinkEncode = linkEncode
                # 找到漫画设标签为1
                findFlag = 1
                break

        # 如果没有找到漫画，则打印出来
        if findFlag == 0:
            print "未找到漫画"
        return reLinkEncode,reNameEncode


class downloadFZDM(object):
    def __init__(self,bookName,bookLink):
        self.headers = [
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 "},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50"},
            {"User-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36"},
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET "},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) "},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36"},
            {"User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0"},
        ]
        self.bookName = bookName
        self.bookLink = bookLink

    #查找需要下载的所有链接
    def findUrls(self):
        # 更换链接即可爬取风之动漫网的任意漫画 http://manhua.fzdm.com/27/
        # 一拳超人http://manhua.fzdm.com/132/
        response = requests.get("http://manhua.fzdm.com/" + self.bookLink, headers=self.headers[random.randint(0,9)])
        selector = etree.HTML(response.text)
        #获取链接
        links = selector.xpath('//*[@id="content"]/li/a/@href')
        #获取章节名称
        linkName = selector.xpath('//*[@id="content"]/li/a')
        for link,name in zip(links,linkName):
            #使用多线程进行下载
            openUrlThreads = threading.Thread(target=self.openUrl,args=(link,name.text))
            #开启线程
            openUrlThreads.start()

            # 使用进程占用资源太多（电脑卡成狗）
            # #使用进程
            # openUrlProcess = Process(target=openUrl,args=(link,name.text))
            # #开启进程
            # openUrlProcess.start()

            #未使用进程(速度慢如狗)
            # openUrl(link,name.text)
            #爬取一话停5秒，防止封ip
            # time.sleep(5)

    #单独访问链接
    #图片xpath //*[@id="mhpic"]/@src
    def openUrl(self,link,fileName):
        #观察发现图片链接经过特殊处理
        # http://183.91.33.78/p1.xiaoshidi.net/2017/07/15011730573263.jpg
        # http://183.91.33.78/p1.xiaoshidi.net/2017/07/15011730573264.jpg
        # 只需要匹配提取出 2017/07/15011730573262.jpg
        # pattern = re.compile(r'\d+\/\d+\/\d+\.jpg')

        #匹配正则表达式
        pattern = re.compile(r'\d+\/\d+\/\d+\.jpg')
        #循环读取图片链接(由于没有超过100页的页面，所以直接设定为100页)
        for i in range(100):
            openLink = "http://manhua.fzdm.com/"+self.bookLink+link+"index_"+str(i)+".html"
            print "\n",openLink
            try:
                response2 = requests.get(openLink, headers=self.headers[random.randint(0,9)])
                #使用正则匹配图片链接
                imagelink = pattern.findall(response2.text)
                if len(imagelink) != 0:
                    # print imagelink[0]
                    #下载图片
                    self.downloadImages(i, fileName, imagelink[0])
            except:
                pass

    #下载链接内图片
    def downloadImages(self,i,fileName,link):
        print "\n", "正在下载:", link
        #拼接地址
        # addr = "images/" + self.bookName + "/" + fileName.encode("utf-8")
        # print "\n", "正在下载:", link," 地址：",addr
        #判断文件夹是否存在
        # isExists = os.path.exists(addr.decode('utf-8'))
        isExists = os.path.exists("images/"+fileName)
        if not isExists:
            # 如果不存在则创建目录
            # os.makedirs(addr.decode('utf-8'))
            os.makedirs("images/"+fileName)
            # print "\n",addr,":文件夹创建成功"
            print "\n",fileName, ":文件夹创建成功"
            #"http://183.91.33.78/p1.xiaoshidi.net/"
        response = requests.get("http://183.91.33.7"+str(random.randint(0,9))+"/p1.xiaoshidi.net/"+link, headers=self.headers[random.randint(0,9)])
        # 保存图片
        with open("images/"+fileName+"/"+str(i)+".png","wb") as f:
            f.write(response.content)
        print "\n",link,"下载完毕"

    #主函数
    def downloadMain(self):
        self.findUrls()

if __name__ == "__main__":
    bF = bookListFZDM()
    link, name = bF.findList()
    print link, name
    download = downloadFZDM(name,link)
    download.downloadMain()

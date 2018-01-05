#coding:utf-8
import requests
import re
from lxml import etree
import os
import time

#网址 http://manhua.fzdm.com/27/
#漫画http://manhua.fzdm.com/27/509/
#翻页http://manhua.fzdm.com/27/509/index_0.html

#链接//*[@id="content"]/li[5]/a/@href
#名字//*[@id="content"]/li[5]/a/

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"
}

#查找所有链接
def findUrls():
    #更换链接即可爬取风之动漫网的任意漫画 http://manhua.fzdm.com/27/
    response = requests.get("http://manhua.fzdm.com/27/", headers=headers)
    selector = etree.HTML(response.text)
    links = selector.xpath('//*[@id="content"]/li/a/@href')
    linkName = selector.xpath('//*[@id="content"]/li/a')
    for link,name in zip(links,linkName):
        openUrl(link,name.text)
        #爬取一话停5秒，防止封ip
        time.sleep(5)


#单独访问链接
#图片xpath //*[@id="mhpic"]/@src
def openUrl(link,fileName):
    #观察发现图片链接经过特殊处理
    # http://183.91.33.78/p1.xiaoshidi.net/2017/07/15011730573263.jpg
    # http://183.91.33.78/p1.xiaoshidi.net/2017/07/15011730573264.jpg
    # 只需要匹配提取出 2017/07/15011730573262.jpg
    # pattern = re.compile(r'\d+\/\d+\/\d+\.jpg')

    #匹配正则表达式
    pattern = re.compile(r'\d+\/\d+\/\d+\.jpg')
    #循环读取图片链接(由于没有超过100页的页面，所以直接设定为100页)
    for i in range(100):
        openLink = "http://manhua.fzdm.com/27/"+link+"index_"+str(i)+".html"
        print openLink
        try:
            response2 = requests.get(openLink, headers=headers)
            #使用正则匹配图片链接
            imagelink = pattern.findall(response2.text)
            if len(imagelink) != 0:
                print imagelink[0]
                #下载图片
                downloadImages(i, fileName, imagelink[0])
        except:
            pass

#下载链接内图片
def downloadImages(i,fileName,link):
    print "正在下载:",link
    #判断文件夹是否存在
    isExists = os.path.exists("images/"+fileName)
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs("images/"+fileName)
        print fileName,":文件夹创建成功"
        #"http://183.91.33.78/p1.xiaoshidi.net/"
    response = requests.get("http://183.91.33.78/p1.xiaoshidi.net/"+link, headers=headers)
    # 保存图片
    with open("images/"+fileName+"/"+str(i)+".png","wb") as f:
        f.write(response.content)
    print link,"下载完毕"

#主函数
def main():
    findUrls()

if __name__ == "__main__":
    main()

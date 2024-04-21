import sys
from bs4 import BeautifulSoup
import re
import urllib.request
import time
#得到页面全部内容
def askURL(url):
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
    request = urllib.request.Request(url,headers=headers)#发送请求
    try:
        response = urllib.request.urlopen(request)#取得响应
        html= response.read()#获取网页内容
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print (e.code)
        if hasattr(e,"reason"):
            print (e.reason)
    return html
    
def getData(baseurl,page):
    findname=re.compile(r'<h2 class="title-h2"><.*>(.*)</a>')#诗名
    findauthor=re.compile(r'<p class="list-zuozhe">(.*)</p>')#朝代及作者
    findtext1=re.compile(r'</div></a>((.)*)</div></mip-showmore>',re.S)#诗内容,格式1
    findtext2=re.compile(r'</p>((.)*)</div></mip-showmore>',re.S)#诗内容，格式2
    remove=re.compile(r'<br/>|\n|\r|<p>|</p>|<br>|</br>|<span>|</span>|题注：.*|注：.*|①|②|③|\(.*?\)|\（.*?\）|《|》',re.S)#去掉无关内容
    
    for i in range(page,page+10):
        
        datalist=[]
        url=baseurl+str(i)
        html=askURL(url)
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_='content-box box-border padding-a scpt-y'):#找到每一首诗
            data=[]
            item=str(item)#转化成字符串
            name=re.findall(findname,item)
            data.append(name)
            author=re.findall(findauthor,item)
            data.append(author)
            try:
                text=re.findall(findtext1,item)[0][0]
                #print(type(text))
                #print(text.strip())
            except:
                text=re.findall(findtext2,item)[0][0]
            text=re.sub(remove,'',text)
            s1=re.sub(u"，|。|？|！"," ",text)
            s1=s1.split()
            try:
                flag=len(s1[0])
                for k in range(len(s1)):
                    if (len(s1[k])!=flag):
                        flag=0
                if((flag==5)or(flag==7)) and (len(s1)%4==0)and (len(s1)>=4):
                    data.append(text)
                    print(data)
                    datalist.append(data)
                else:
                    continue
            except:
                continue
        print(i)
    return datalist


#保存datalist的内容到指定路径savepath
def saveData(datalist,savepath):
    f=open(savepath,"a+",encoding='utf-8')
    for i in range(0,len(datalist)):
        data=datalist[i]
        for j in range(0,2):
            f.write(""+data[j][0]+"\t")
        f.write(""+data[2])
        f.write("\n")
    
def main():
    print("开始爬取……")
    baseurl="https://shicixuexi.com/13/p"
    page=1
    page_all=1633
    start=time.time()
    #每十页保存一次
    while page+10<=page_all:
        datalist=getData(baseurl,page)
        savepath="唐.txt"
        saveData(datalist,savepath)
        page=page+10
    end=time.time()
    print(end-start)
    
main()
               
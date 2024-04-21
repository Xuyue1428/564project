import re
import os

openfile="new_all.txt"
f=open(openfile,"r",encoding="utf-8")
txt=f.readlines()
lens=len(txt)
f.close()

dir="data"
#将长诗分割为每四句一首的诗,并按5言或7言分类
for i in range(0,lens):
    line=txt[i]
    list1=line.split('\t')
    poem=list1[2].strip()
    s1=re.sub(u"，|。|？|！|；"," ",poem)
    s=s1.split()
    length_shi=len(s)
    j=0
    if len(s[0])==5:
        file=dir+"/5/quan.txt"
    else:
        file=dir+"/7/quan.txt"
    f_write=open(file,"a+",encoding="utf-8")
    while j+3<=length_shi:
        temp=""
        tou=""
        wei=""
        temp+=s[j]+"，"+s[j+1]+"。"+s[j+2]+"，"+s[j+3]+"。\n"
        f_write.write(temp)
        j=j+4
import re

#读取文件
def read_file(openfile):
    f=open(openfile,"r",encoding="utf-8")
    txt=f.readlines()
    lens=len(txt)
    f.close()
    return txt,lens

#判断诗歌的每句的长度是否相等，且为5或7
def check_num_of_words(poem):
    lens=len(poem[0])
    for temp in poem:
        if len(temp)==lens and (lens==5 or lens==7):
            continue
        else:
            return False
    return True

#判断诗歌长度大于4，且是4的倍数。
def check_num_of_line(poem):
    s1=re.sub(u"，|。|？|！|；"," ",poem)
    s=s1.split()
    if len(s)%4==0 and len(s)>=4 and check_num_of_words(s):
        return True
    return False

#判断诗歌中均为中文，或标点    
def check_chinese(poem):
    for word in poem:
        if '\u4e00'<=  word and word<= '\u9fff' or word=="，" or word=="。" or word=="！" or word=="？" or word=="；":
            continue
        else:
            return False
    return True

openfile="all.txt"
savefile="all_1.txt"    
f=open(savefile,"w",encoding="utf-8")    
txt,lens=read_file(openfile)  
  
for i in range(0,lens):
    line=txt[i]
    list1=line.split('\t')
    title=list1[0].strip()
    poem=list1[2].strip()
    if ("生查子" in title) or ("木兰花" in title) or ("玉楼春" in title) or ("浣溪沙" in title) or ("瑞鹧鸪" in title) or check_num_of_line(poem)==False or check_chinese(poem)==False:
        #if ("生查子" in title) or ("木兰花" in title) or ("玉楼春" in title) or ("浣溪沙" in title) or ("瑞鹧鸪" in title):
        #    print(title)
        continue
    else:
        f.write(line)

        
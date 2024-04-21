import re
import Levenshtein as ls

#读文件
def read_file(openfile):
    f=open(openfile,"r",encoding="utf-8")
    txt=f.readlines()
    lens=len(txt)
    f.close()
    return txt,lens

#计算当前诗与列表中诗歌的最高相似度，并返回相似诗歌和相似率    
def to_rate(list,line):
    rate=0
    po=""
    for temp in list:
        ra=ls.ratio(temp,line)
        if ra>rate:
            rate=ra
            po=temp
    return rate,po
    
list_poem=[]     
 
openfile="all_1.txt"
savefile="new_all.txt"
profile="pro_all.txt"       
#profile保存相似度超过0.8的诗歌，以及与它最相似的诗歌

#由于文件较大，且循环判断需求时间长，中间有中断
#读取已经处理完的部分，并继续处理
f=open(savefile,"r+",encoding="utf-8")
txt_save=f.readlines()
for line in txt_save:
    s1=line.split('\t')
    try:
        list_poem.append(s1[2].strip())
    except:
        print(line)
        pass
#print(list_poem)

f_pro=open(profile,"a+",encoding="utf-8")
txt,lens=read_file(openfile)

for i in range(0,lens):
    if i%100==0:
        print(i)
    line=txt[i]
    s1=line.split('\t')
    poem=s1[2].strip()
    rate,po=to_rate(list_poem,poem)
    if rate<=0.8:
        list_poem.append(poem)
        f.write(line)
    else:
        f_pro.write(line)
        f_pro.write(po+"\n")
    

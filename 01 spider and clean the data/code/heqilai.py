import re

#将唐、五代、宋、金、辽、元、明、清、近现代、当代诗合在一个文件中

openfile1="1/dangdai.txt"
openfile2="1/all.txt"

pro="pro_all.txt"

f=open(openfile1,encoding="utf-8")
txt1=f.readlines()
len1=len(txt1)
f.close()
f=open(openfile2,"r+",encoding="utf-8")
txt2=f.readlines()
len2=len(txt2)


f1=open(pro,"a+",encoding='utf-8')
list=[]

#去无用符号，并判断是否为中文字符
def check_zh(temp):
    remove=re.compile(r'<br/>|\n|\r|<p>|</p>|<br>|</br>|<span>|</span>|题注：.*|注：.*|①|②|③|\(.*?\)|\（.*?\）|《|》',re.S)#去掉无关内容
    temp=re.sub(remove,'',temp)
    s1=re.sub(u"，|。|？|！|；"," ",temp)
    s=s1.split()
    #print(s)
    for ju in s:
        for zi in ju:
            if not '\u4e00' <= zi <= '\u9fa5':
                return False
    return True
#将内容写入文件    
def write_in(lens,txt):
    for i in range(0,lens):
        line=txt[i]
        list1=line.split('\t')
        poem=list1[2].strip()    
        if check_zh(poem)==False:
            #print(t3)
            f1.write(line)
            continue    
        if poem not in list:
            list.append(poem)
            f.write(line)
        else:
            continue
#载入已经保存的内容            
def reload(lens,txt):
    for i in range(0,lens):
        line=txt[i]
        list1=line.split('\t')
        poem=list1[2].strip()
        if poem not in list:
            list.append(poem)
        else:
            continue
reload(len2,txt2)  
write_in(len1,txt1) 
         
from pypinyin import pinyin,Style
import re
import Levenshtein as ls
import math
def is_rusheng(zi):#判断一个字是否为入声
    style=Style.TONE3
    temp=pinyin(zi,style=style)
    temp=temp[0][0]
    sheng=temp[-1]
    pin=temp[:-1]
    if len(pin)>=2 and (pin[-2:]=="ng" or pin[-1]=="n"):
        return False
    elif len(pin)>=2 and (pin[0]=="b" or pin[0]=="d" or pin[0]=="g" or pin[0]=="j" or pin[0]=="z" or pin[:2]=="zh") and sheng=="2":
        return True
    elif len(pin)>=3 and (pin[0]=="k" or pin[0]=="r" or pin[:2]=="zh" or pin[:2]=="ch" or pin[:2]=="sh") and pin[-2:]=="uo":
        return True
    elif len(pin)>=2 and(pin[0]=="d" or pin[0]=="t" or pin[0]=="l" or pin[0]=="z" or pin[0]=="c" or pin[0]=="s") and  pin[1]=="e":
        return True
    elif len(pin)>=2 and pin[0]=="f" and (pin[1]=="a" or pin[1]=="o"):
        return True
    elif len(pin)>=3 and (pin[0]=="d" or pin[0]=="g" or pin[0]=="h" or pin[0]=="z" or pin[0]=="s") and pin[-2:]=="ei":
        return True
    elif len(pin)>=3 and (pin[0]=="b" or pin[0]=="p" or pin[0]=="m" or pin[0]=="d" or pin[0]=="t" or pin[0]=="n" or pin[0]=="l") and pin[-2:]=="ie" and zi!="爹":
        return True
    elif len(pin)>=3 and pin[-2:]=="ue" and zi!="嗟" and zi!="瘸" and zi!="靴":
        return True
    else: 
        return False

def ping_or_ze(zi):#判断一个字的平仄
#0表示平，1表示仄
    style=Style.TONE3
    temp=pinyin(zi,style=style)
    sheng=temp[0][0][-1]
    if is_rusheng(zi):
        return "1"
    elif sheng=='1' or sheng=='2':  
        return "0"
    else:
        return "1"

def rhyme(zi1,zi2):#判断两个字是否押韵
    style=Style.FINALS 
    Finals0=pinyin(zi1,style=style,heteronym=True)[0]
    Finals1=pinyin(zi2,style=style,heteronym=True)[0]
    #print(Finals0,Finals1)
    for i in range(len(Finals0)):
        Fi0=Finals0[i]
        for j in range(len(Finals1)):
            Fi1=Finals1[j]
            if Fi1[-1]=="u" or Fi1[-1]=="v":
                if Fi0[-1]=="u" or Fi0[-1]=="v":
                    return 1
                
            if Fi0[-1]==Fi1[-1]:
                return 1
           # print(Fi0,Fi1)
            '''
            if len(Fi0)==1 or len(Fi1)==1:
                if Fi0[-1]==Fi1[-1]:
                    return 1
            elif Fi0[-2:]==Fi1[-2:]:
                return 1
            '''
    if is_rusheng(zi1) and is_rusheng(zi2):
        return 3        
    return 0  
    
list_5=[["00110，11100。11001，00110。"],["01100，00110。10011，11100。"],["00011，11100。11001，00110。"],["11001，00110。00011，11100。"]]
list_7=[["001110，1100110。1100011，0011100。"],["1100110，0011100。0011001，1100110。"],["0011001，1100110。1100011，0011100。"],["1100011，0011100。0011001，1100110。"]]

def quan_ping_ze(yan,res):#将一首诗转化为它对应的平仄向量形式
    quan=""
    for i in range(len(res)):
        line=res[i]
        for zi in line:
            quan+=ping_or_ze(zi)
        if i%2==0:
            quan+="，"
        else:
            quan+="。"
    return quan
    
def to_rate(list,line):#给出字符串相似度
    rate=0
    for temp in list:
        ra=ls.ratio(temp[0],line)
        if ra>rate:
            rate=ra
    return rate    
    
def score_pingze(res,type):#根据平仄给分
    yan=len(res[0])
    if yan==5:
        list=list_5
    else:
        list=list_7
   # print(yan,list)
    quan=quan_ping_ze(yan,res)
    #print(quan)
    score=to_rate(list,quan)*10
    #print(score)
    return score
    
def score_rhyme(res):#根据押韵情况给分    
    score=0
    type=0
    type1=rhyme(res[1][-1],res[3][-1])
    #print(type1)
    if type1!=0 and res[1][-1]!=res[3][-1]:
        type+=type1
        score+=8
        type2=rhyme(res[0][-1],res[3][-1])
        if type2!=0 and res[0][-1]!=res[3][-1] and res[0][-1]!=res[1][-1]:
            score+=2
            type+=type2
            return score,type
        return score,type
    else:
        return score,type  
            
def check_quality(res):#判断诗歌分数
    
    s1=re.sub(u"，|。"," ",res)
    s1=s1.split()
    '''
    print(fluence(s1))
    return True
    '''
    score1,type=score_rhyme(s1)
    score2=score_pingze(s1,type)
    score_all=score1*1.0+score2*1.0
    #print(res)
    #print("押韵得分：\t",score1)
    #print("平仄得分：\t",score2)
    #print("总得分：\t",score_all)
    return score_all
    
       

        
     
#['uang', 'u'] ['ai', 'u', 'uan']    
'''    
res="刻骨酸辛藕断丝，国门归棹恰当时。九州无限抛雏恨，唱彻千秋堕泪词。"
print(check_quality(res))
'''

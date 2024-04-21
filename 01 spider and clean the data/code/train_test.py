import random

source="C:/code/564/sqx_NLP_generate/02藏头诗训练及生成/代码和数据/data/7/quan.txt"
test_num=10000


def rand_nums(limits,number):    #limits是范围，随机数在(0，limits)内;number是随机数个数
    list=[]
    for i in range(0,number):
        num=random.randint(0,limits)
        while num in list:
            num=random.randint(0,limits)
        list.append(num)
    return list
    
def divide(source,test_num):       #划分测试集10000，训练集其他
    with open(source,encoding='utf-8') as f:
        all_source=f.readlines()    
    all_num=len(all_source)
    test=[]
    test=rand_nums(all_num,test_num)
    #print(test)

    with open("C:/code/564/sqx_NLP_generate/02藏头诗训练及生成/代码和数据/data/7/test.txt","w",encoding='utf-8') as f:
        for i in test:
            f.write(all_source[i])  
   

    with open("C:/code/564/sqx_NLP_generate/02藏头诗训练及生成/代码和数据/data/7/train.txt","w",encoding='utf-8') as f:
        for i in range(0,all_num):
            if  i not in test :
                f.write(all_source[i])



divide(source,test_num)
    
            
        
    
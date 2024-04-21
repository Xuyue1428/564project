import os

dir='E:/work/python/2019.12/按主题/2'

def read_file(openfile):
    f=open(openfile,"r",encoding='utf-8')
    txt=f.readlines()
    lens=len(txt)
    f.close()
    return txt,lens

f_train=open("data/trainData.tsv","w",encoding='utf-8')
f_dev=open("data/devData.tsv","w",encoding='utf-8')
f_test=open("data/testData.tsv","w",encoding='utf-8')

dict={"山水":1,"思念":2,"思乡":3,"悼亡":4,"爱国":5,"田园":6,"读书":7,"送别":8}

for (root, dirs, files) in os.walk(dir):
    for file in files:
        openfile=dir+"/"+file
        txt,lens=read_file(openfile)
        label=dict[file.split('.')[0]]
        for i in range(0,int(lens*0.05)):
            line=txt[i]
            f_dev.write(line.strip()+"\t"+str(label)+"\n")
        for i in range(int(lens*0.05),int(lens*0.1)):
            line=txt[i]
            f_test.write(line.strip()+"\t"+str(label)+"\n")
        for i in range(int(lens*0.1),lens):
            line=txt[i]
            f_train.write(line.strip()+"\t"+str(label)+"\n")
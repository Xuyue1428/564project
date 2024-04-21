import collections
import numpy as np
import _pickle as cPickle
import os
from arg import Param
import re
        
class data():
    def __init__(self,args):
        if not (os.path.exists(args.test_file) and os.path.exists(args.tensor_test)):
            #print("运行prepare")
            self.prepare(args,args.input_file, args.vocab_file)
            self.train_test_data(args,args.train_file,args.tensor_train)
            self.train_test_data(args,args.test_file,args.tensor_test)
            self.load_prepare(args.vocab_file, args.tensor_train,args.tensor_test)
        else:
            #print("运行load_prepare")
            self.load_prepare(args.vocab_file, args.tensor_train,args.tensor_test)
        args.vocab_size=len(self.words)
        args.train_pointer=0
        args.test_pointer=0
        self.train_batch(args.batch_size)
        self.test_batch(args.batch_size)
        #print(self.test_x)
    def pre_read(self,args,input_file):
        poetrys = []    
        f=open(input_file,encoding='utf-8')
        txt=f.readlines()    
        for line in txt:
            try:
                line1=line.strip('\n')
                if args.tou_or_wei=="WEI":
                    line=line1[::-1]
                else:
                    line=line1
                new=""               
                new=new+args.BEGIN_CHAR+line+args.END_CHAR
                poetrys.append(new)
            except:
                pass
        # 按诗的字数排序
        poetrys = sorted(poetrys, key = lambda line: len(line))
        return poetrys
    def prepare(self,args,input_file, vocab_file):
        poetrys = self.pre_read(args,input_file)
        print('唐诗总数: ', len(poetrys))
        # 统计每个字出现次数
        all_words = []
        for poetry in poetrys:
            all_words += [word for word in poetry]
        counter = collections.Counter(all_words)
        count_pairs = sorted(counter.items(), key=lambda x: -x[1])
        words, _ = zip(*count_pairs)
        # 取前多少个常用字
        self.words = words[:len(words)] + (' ',)
        # 每个字映射为一个数字ID
        self.vocab=dict(zip(self.words,range(len(self.words))))           
        #保存vocab_file
        f=open(vocab_file,'wb')
        cPickle.dump(self.words,f)

    def train_test_data(self,args,input_file,tensor_file):#将训练集和测试集的内容转化为诗向量，并保存
        poetrys = self.pre_read(args,input_file)
        print('总数: ', len(poetrys)) 
        to_num = lambda word: self.vocab.get(word, len(self.words))
        tensor = [ list(map(to_num, poetry)) for poetry in poetrys]
        f=open(tensor_file,'wb')
        cPickle.dump(tensor,f) 
    
    def load_prepare(self,vocab_file, tensor_train,tensor_test):#将保存好的内容载入
        f=open(vocab_file,'rb')
        self.words=cPickle.load(f)
        f=open(tensor_train,'rb')
        self.tensor_train=cPickle.load(f) 
        f=open(tensor_test,'rb')
        self.tensor_test=cPickle.load(f)         
        # 每个字映射为一个数字ID
        self.vocab=dict(zip(self.words,range(len(self.words))))

    def batch(self,num_batches,tensor_batch,batch_size):#将数据分batch
        unknow_char_int=self.vocab[' ']
        batch_x=[]
        batch_y=[]
        for i in range(0,num_batches):
            start=i*batch_size
            end=start+batch_size
            batches=tensor_batch[start:end]
            seq_length = max(map(len,batches))        
            xdata = np.full((batch_size, seq_length), unknow_char_int, np.int32)
            for line in range(0,batch_size):
                xdata[line,:len(batches[line])]=batches[line]
            ydata=np.copy(xdata)
            ydata[:,:-1] = xdata[:,1:]
            batch_x.append(xdata)
            batch_y.append(ydata)
        return batch_x,batch_y
    def train_batch(self,batch_size):
        self.num_batches=int(len(self.tensor_train)/batch_size)
        self.tensor_train=self.tensor_train[:self.num_batches*batch_size]
        
        self.train_x,self.train_y=self.batch(self.num_batches,self.tensor_train,batch_size)
            
    def test_batch(self,batch_size):
        self.test_num_batches=int(len(self.tensor_test)/batch_size)
        self.tensor_test=self.tensor_test[:self.test_num_batches*batch_size]
        self.test_x,self.test_y=self.batch(self.test_num_batches,self.tensor_test,batch_size)

    def next_batch(self,args):
        xdata=self.train_x[args.train_pointer]
        ydata=self.train_y[args.train_pointer]
        args.train_pointer+=1
        return xdata,ydata
        
    def test_next_batch(self,args):
        xdata=self.test_x[args.test_pointer]
        ydata=self.test_y[args.test_pointer]
        args.test_pointer+=1
        return xdata,ydata


def main():
    args=Param(7,"TOU")
    pre=data(args)
    args=Param(5,"TOU")
    pre=data(args)

if __name__ == "__main__":
    main()
  

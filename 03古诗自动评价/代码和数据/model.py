import numpy as np
import tensorflow as tf
import tensorflow.contrib.rnn as rnn
import math
from score import *

class Poetry_Model():
    def __init__(self,args,infer=False):#定义模型
        self.graph = tf.Graph()
        with self.graph.as_default():
            self.n_epoch=args.n_epoch
            self.model_file=args.model_file
            self.batch_size=args.batch_size
            self.args=args
            if infer:
                self.batch_size=1
            
            with tf.name_scope('inputs'):
                self.input_data = tf.placeholder(
                    tf.int32, [self.batch_size, None])
                self.targets = tf.placeholder(
                    tf.int32, [self.batch_size, None])
        
            with tf.name_scope('model'):    
                cell_fun = rnn.BasicLSTMCell
                cell=cell_fun(args.rnn_size,state_is_tuple=False)
                cell=rnn.MultiRNNCell([cell]*args.num_layers,state_is_tuple=False)
                self.cell=cell        
                self.initial_state = cell.zero_state(self.batch_size, tf.float32)               
                with tf.variable_scope('rnnlm'):
                #tf.variable_scope可以让变量有相同的命名，包括tf.get_variable得到的变量，还有tf.Variable的变量
                    softmax_w = tf.get_variable("softmax_w", [args.rnn_size, args.vocab_size])
                    softmax_b = tf.get_variable("softmax_b", [args.vocab_size])
                    with tf.device("/cpu:0"):
                        embedding = tf.get_variable("embedding", [args.vocab_size, args.rnn_size])
                        inputs = tf.nn.embedding_lookup(embedding, self.input_data)#选取一个张量里面索引对应的元素            
                outputs, last_state = tf.nn.dynamic_rnn(cell, inputs, initial_state = self.initial_state, scope = 'rnnlm')
       
            with tf.name_scope('loss'):
                output=tf.reshape(outputs,[-1,args.rnn_size])
                self.logits=tf.matmul(output,softmax_w)+softmax_b
                self.probs=tf.nn.softmax(self.logits)
                self.last_state=last_state
                targets=tf.reshape(self.targets, [-1])
                loss=tf.contrib.legacy_seq2seq.sequence_loss_by_example([self.logits],[targets],[tf.ones_like(targets,dtype=tf.float32)],args.vocab_size)
                self.cost=tf.reduce_mean(loss)
                tf.summary.scalar('loss', self.cost)#画loss
        
            with tf.name_scope('optimize'):   
                self.learning_rate = tf.Variable(0.0, trainable = False)
                tf.summary.scalar('learning_rate', self.learning_rate)            
                     
                train_vars = tf.trainable_variables()#可以查看可训练的变量
                grads=tf.gradients(self.cost, train_vars)#tf.gradients(ys,xs,其他参数)实现ys对xs求导
                for g in grads:
                    tf.summary.histogram(g.name, g)#显示训练过程中变量的分布情况            
                grads, _ = tf.clip_by_global_norm(grads, args.clip_norm)
                # clip_by_global_norm将x的L2范数与clip_norm比较如果比clip_norm大则对x进行处理使x的L2范数小于等于clip_norm
                #optimizer = tf.train.GradientDescentOptimizer(learning_rate)#梯度
                optimizer = tf.train.AdamOptimizer(self.learning_rate)#数据稀疏，Adam好  
                self.train_op = optimizer.apply_gradients(zip(grads, train_vars))
                self.merged_op = tf.summary.merge_all()#merge_all 将所有summary全部保存到磁盘，以便tensorboard显示。
              
    def load(self,sess,saver):
        latest=tf.train.latest_checkpoint(self.model_file)
        if latest:
            saver.restore(sess,latest)
            return int(latest.split('-')[1])
        else:
            sess.run(tf.global_variables_initializer())
            return -1
      
    def fluent(self,sess,words,vocab,poem,len_ju):#计算诗歌生成概率
        def word_to_weight(word,weights):
            num=vocab[word]
            return weights[num]
        fluence=1
        res=""+self.args.BEGIN_CHAR
        for i in range(4):
            res+=poem[i][0]
            for j in range(1,len_ju):
                x = np.array([list(map(vocab.get,res))])
                state = self.cell.zero_state(1, tf.float32).eval()
                [probs,state] = sess.run([self.probs,self.last_state],{self.input_data: x,self.initial_state: state})
                fluence=fluence*word_to_weight(poem[i],probs[-1])*pow(10,4)
                res+=poem[i]
            if i%2==0:
                res+="，"
            else:
                res+="。" 
        #print(fluence)
        
        return fluence
                    
                    
    def gen(self,sess,words,vocab,keywords,len_ju,cang):#由给定关键词和要求生成诗歌
        def check_reuse(key):
        #检查藏头词或藏尾词是否有字重复
            lis=[]
            for word in key:
                if word not in lis:
                    lis.append(word)
            if len(lis)<len(key):
                return True
            else:
                return False
        
        
        def is_Chinese(words):
            for word in words:
                if '\u4e00' > word or word> '\u9fff' or word=="]" or word=="[" or word=="，" or word=="。":
                    return False
            return True
            
        def nums_to_word(weights):
            t = np.cumsum(weights)#cumsum计算一个数组各行的累加值
            s = np.sum(weights)
            sample = words[int(np.searchsorted(t, np.random.rand(1)*s))]#np.searchsorted在t中检索s所处的位置
            return sample
         
        if len(keywords)<4:
            flag=3
            while flag>0:
                flag_ci=False
                while not flag_ci:
                    key=keywords
                    for i in range(len(key),4):
                        x = np.array([list(map(vocab.get,key))])
                        state = self.cell.zero_state(1, tf.float32).eval()
                        [probs,state] = sess.run([self.probs,self.last_state],{self.input_data: x,self.initial_state: state})
                        next=nums_to_word(probs[-1])
                        key+=next 
                    if is_Chinese(key)==True:
                        flag_ci=True
                        
                    #print(key)
                if cang=="WEI":
                    #print(flag)
                    #print(key)
                    if rhyme(key[1],key[3])==0 or(check_reuse(key)==True and check_reuse(keywords)==False):
                        flag-=1
                    else:
                        flag=0
                elif check_reuse(key)==True and check_reuse(keywords)==False :
                    flag-=1
                else:   
                    flag=0
            keywords=key
       # print(keywords)
        Flag=5
        temp=["",0]
        while Flag>0:
            if cang=="TOU":
                res=""+self.args.BEGIN_CHAR
            else:
                res=""+self.args.BEGIN_CHAR+"。"
                keyword=keywords[::-1]
                keywords=keyword
            for word in keywords:
                flag=True
                while flag:
                    sentence=word
                    x = np.array([list(map(vocab.get,res+sentence))])
                    state = self.cell.zero_state(1, tf.float32).eval()
                    [probs,state] = sess.run([self.probs,self.last_state],{self.input_data: x,self.initial_state: state})
                    next=nums_to_word(probs[-1])
                
                    while next!='，' and next!='。'and next!= self.args.END_CHAR:
                        sentence+=next
                        x = np.zeros((1,1))
                        x[0,0] = vocab[next]
                        [probs,state] = sess.run([self.probs,self.last_state],{self.input_data: x,self.initial_state: state})
                        #print(probs[-1])
                        next=nums_to_word(probs[-1])
                    sentence+=next
                    if len(sentence)==1+len_ju:
                        res+=sentence
                        flag=False
            #print(res[1:])
            if cang=="TOU":
                res=res[1:]
                scores=check_quality(res)
                if scores<8:
                    Flag-=1
                    if scores>temp[1]:
                        temp[1]=scores
                        temp[0]=res
                    
                else:
                    Flag=-1
            else:
                res1=res[::-1]
                res=res1[1:-1]
                Flag=-1
            if Flag==0 and temp[0]=="":
                Flag=5
        if Flag==0:
            res=temp[0]
            
        return res

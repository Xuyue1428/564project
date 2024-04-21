#python train.py -y 7 -c "TOU"

from __future__ import unicode_literals
import codecs
import argparse 
import numpy as np
import tensorflow as tf
from arg import Param
from prepare_data import *
from model import Poetry_Model
import time
import os,sys
import math
import _pickle as cPickle
from tensorflow.contrib.tensorboard.plugins import projector
from io import open

argparse.open = open
#命令行参数
def create_parser(subparsers=None):
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="generate poems")
    parser.add_argument(
        '--yan', '-y', type=int, default="7",
        help="输入五言或七言")
    parser.add_argument(
        '--cang', '-c', type=str, default="WEI",
        help="输入藏头或藏尾")    
    return parser
    
def train(args):
    data_loader=data(args)
    model=Poetry_Model(args)

    Session_config = tf.ConfigProto(allow_soft_placement = True)
    Session_config.gpu_options.allow_growth = True

    with tf.Session(config=Session_config,graph=model.graph) as sess:
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver(tf.global_variables())
        last_epoch=model.load(sess,saver)
        #载入已有模型（如果有）
        writer = tf.summary.FileWriter(args.log_dir, sess.graph)
        config = projector.ProjectorConfig()
        embed = config.embeddings.add()
        embed.tensor_name = 'rnnlm/embedding:0'
        embed.metadata_path = args.metadata
        projector.visualize_embeddings(writer, config)
       

        print("start training")
        losses=[]
        
        for i in range(last_epoch+1,model.n_epoch):
            start=time.time()
            print("n_epoch：",i)
            trainloss=[]
            sess.run(tf.assign(model.learning_rate, args.learning_rate * (args.decay_rate ** i)))
            args.train_pointer=0
           
            all_loss=0.0
            #分batch进行训练
            for j in range(0,data_loader.num_batches):
                xdata,ydata=data_loader.next_batch(args)
                feed_dict={model.input_data:xdata, model.targets:ydata}
                train_loss, _, _, _ = sess.run([model.cost,model.merged_op, model.last_state, model.train_op],feed_dict)
                all_loss = all_loss + train_loss
                trainloss.append(train_loss)
                end = time.time()
                if j%100==0:
                    print("batch:",j,"loss:",train_loss,"time:",end-start)
                
                
            total_loss = 0.0
            args.test_pointer=0
            for k in range(data_loader.test_num_batches):
                xdata,ydata=data_loader.test_next_batch(args)
                feed_dict = {model.input_data:xdata, model.targets:ydata}
                train_loss,summary, _, _ = sess.run([model.cost,model.merged_op, model.last_state, model.train_op],feed_dict)
        
                total_loss+= train_loss   
                test_loss=total_loss / data_loader.test_num_batches
                
            losses.append(test_loss)
            ave_loss=all_loss * 1.0/data_loader.num_batches
            writer.add_summary(summary, global_step=i*data_loader.test_num_batches)
            checkpoint_path = os.path.join(args.model_file, 'model.ckpt')
            saver.save(sess,checkpoint_path,global_step=i)#保存模型
           
            print("epoch:",i,"train_Loss:",ave_loss,"time:",end-start)
            print("epoch:",i,"test_Loss:",test_loss)#输出loss值
            with open(os.path.join(args.save_dir,"train_losses-"+str(i)+".pkl"),'wb') as f1:
                cPickle.dump(trainloss,f1)
            
        with open(os.path.join(args.save_dir,"test_losses"+".pkl"),'wb') as f2:
            cPickle.dump(losses,f2)
            print("ok")

def main():
    if sys.version_info < (3, 0):
        sys.stderr = codecs.getwriter('UTF-8')(sys.stderr)
        sys.stdout = codecs.getwriter('UTF-8')(sys.stdout)
        sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
    else:
        sys.stderr = codecs.getwriter('UTF-8')(sys.stderr.buffer)
        sys.stdout = codecs.getwriter('UTF-8')(sys.stdout.buffer)
        sys.stdin = codecs.getreader('UTF-8')(sys.stdin.buffer)
    
    parser = create_parser()
    args = parser.parse_args()
    arg=Param(args.yan,args.cang)
    train(arg)

if __name__=='__main__':
    main()



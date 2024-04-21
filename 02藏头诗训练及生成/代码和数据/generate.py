#python generate.py -k "江南好" -y "七言" -c "藏头"

from __future__ import unicode_literals
import sys
import codecs
import argparse 
import numpy as np
import tensorflow as tf
from model import Poetry_Model
from arg import Param
import os
from prepare_data import data
import time
from pypinyin import pinyin,Style
from io import open

argparse.open = open
#命令行参数
def create_parser(subparsers=None):
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="generate poems")
    parser.add_argument(
        '--key', '-k', type=str, default="香港理工大学",
        help="输入关键词.")

    parser.add_argument(
        '--yan', '-y', type=str, default="七言",
        help="输入五言或七言")
    parser.add_argument(
        '--cang', '-c', type=str, default="藏头",
        help="输入藏头或藏尾")    
    return parser
    
#将输入要求转化
def pre(yan,cang):
    if yan=="五言":
        len_ju=5
    elif yan=="七言":
        len_ju=7
    else:
        print("句子长度需为5或7！")
        return
    if cang=="藏头":
        type="TOU"
    elif cang=="藏尾":
        type="WEI"
    else:
        print("关键字需指定藏头或藏尾！")
        return 
    return  len_ju, type  

#拼音转汉字，返回10个候选项    
def pinyin_2_hanzi(pinyinList):
    from Pinyin2Hanzi import DefaultDagParams
    from Pinyin2Hanzi import dag
    dagParams = DefaultDagParams()
    result = dag(dagParams, pinyinList, path_num=10, log=True)#10代表侯选值个数
    return result

#生成诗歌函数
def generate_poem(key_words,yan,cang):
    start=time.time()
    len_ju,type=pre(yan,cang)
    args=Param(len_ju,type)
    data_loader=data(args)
    words=data_loader.words
    vocab=data_loader.vocab
    model=Poetry_Model(args,infer=True)
    with tf.Session(graph=model.graph) as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.model_file)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            p1 = model.gen(sess,words,vocab,key_words,len_ju,type)
            p2 = model.gen(sess,words,vocab,key_words,len_ju,type)
    end =time.time()
    #print(end-start)
    return p1, p2

#预处理函数
def handle_poem(key_words,yan,cang):
    key_words=key_words.replace(" ","")
    start=time.time()
    len_ju,type=pre(yan,cang)
    args=Param(len_ju,type)
    data_loader=data(args)
    words=data_loader.words
    def in_words(word):
        temp=""
        for ch in word:
            if ch not in words:
                style=Style.TONE3
                pinyinList=pinyin(ch,style=style)
                #print(pinyinList)
                res=pinyin_2_hanzi(pinyinList[0])
                for item in res:
                    if item.path[0] in words:
                        temp+=item.path[0]
                        break
            else:
                temp+=ch
        #print(temp)
        return temp
    def is_Chinese(word):
        for ch in word:
            if '\u4e00' > ch or ch> '\u9fff':
                return False
        return True
    if len(key_words)<1:
        return 1,1        
    elif is_Chinese(key_words)==False:
        return 2,2

    else:
        if len(key_words)>4:
            key_words=key_words[:4]
        key_words=in_words(key_words)
        if len(key_words)==0:
            return 3,3
        p1,p2=generate_poem(key_words,yan,cang)
        end=time.time()
        print(end-start)
        return p1,p2   

#主函数
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
    p1, p2 = generate_poem(args.key,args.yan,args.cang)
    print(p1)
    print(p2)

if __name__ == '__main__':
    main()  
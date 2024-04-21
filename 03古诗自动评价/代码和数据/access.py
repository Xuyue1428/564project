#python access.py -i data/评价/access.txt -o data/评价/res.txt

from __future__ import unicode_literals

import tensorflow as tf
import sys
import codecs
import argparse 
from model import Poetry_Model
from prepare_data import data
from arg import Param
from score import *
from pypinyin import pinyin,Style
import re
import math
from jieba import analyse 
import os
import operator
import time
textrank = analyse.textrank
extract_tags=analyse.extract_tags
from io import open
argparse.open = open

dict_dir="data/label"
file_stopwords="data/stopwords.txt"

#命令行参数
def create_parser(subparsers=None):
    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="access quality of poems")
    parser.add_argument(
        '--input', '-i', type=argparse.FileType('r'), default=sys.stdin,
        metavar='PATH',
        help="Input text (default: standard input).")

    parser.add_argument(
        '--output', '-o', type=argparse.FileType('w'), default=sys.stdout,
        metavar='PATH',
        help="Output file for BPE codes (default: standard output)")
    return parser


#读取文件内容
def readfile(input_file):
    f=open(input_file,"r",encoding="utf-8")
    txt=f.readlines()
    f.close()
    return txt
#根据诗歌生成概率给分
def score_fluence(res,len_ju):
    args=Param(len_ju,"TOU")
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
            flu=model.fluent(sess,words,vocab,res,len_ju)
            flu=pow(flu,1/4)
            if flu>=10:
                flu=10
            elif flu<=1:
                flu=1
            return flu

#用两种算法提取关键词
def get_keywords(poem):
    analyse.set_stop_words(file_stopwords)
    key1 = textrank(poem) 
    key2=extract_tags(poem)
    keys=sorted(list(set(key1+key2)))
    return keys

#通过预测诗歌主题，前二可能性最大标签的概率值
def poem_topic(poem,dict):
    keys=get_keywords(poem)
    P={}
    for label in dict:
        dict_label=dict[label]
        P[label]=0
        for key in keys:
            if key in dict_label:
                P[label]+=dict_label[key]
    P=sorted(P.items(),key=operator.itemgetter(1))
    temp1=P[-1]
    temp2=P[-2]
    if P[-1][1]!=0:
        p=0
        for temp in P:
            p+=temp[1]
        temp1=(P[-1][0],P[-1][1]/p)
        temp2=(P[-2][0],P[-2][1]/p)
    return temp1,temp2
#载入主题关键词字典    
def topic_dict(dict_dir):
    dict={}
    for (root, dirs, files) in os.walk(dict_dir):
        for file in files:
            dict_file={}
            openfile=dict_dir+"/"+file
            txt=readfile(openfile)
            label=file.split('.')[0]
            for line in txt:
                s1=line.split('\t')
                dict_file[s1[0]]=float(s1[2].strip())
            dict[label]=dict_file
        return dict    
#根据关键词打分
def score_keywords(poem):
    keys=get_keywords(poem)
    lens=len(keys)
    if lens>10:
        return 10
    else:
        return lens
#前二可能性最大标签的概率值之和，作为主题鲜明度的判断依据
def score_topic(poem):
    dict=topic_dict(dict_dir)
    temp1,temp2=poem_topic(poem,dict)
    return (temp1[1]+temp2[1])*10
        
#各项分数经加权求和得总分
def access_quality(res):
    res=re.sub(u"\n|\t","",res)
    s1=re.sub(u"，|。"," ",res)
    s1=s1.split()
    score1,type=score_rhyme(s1)
    score2=score_pingze(s1,type)
    score3=score_fluence(res,len(s1[0]))
    score4=score_keywords(res)
    score5=score_topic(res)
    pro=[0.22024896541577815,0.43827599093017017,0.20811311577544914,0.07227329762835814,0.061088630250244406]
    score_all=pro[0]*score1+pro[1]*score2+pro[2]*score3+pro[3]*score4+pro[4]*score5

    score=[score1,score2,score3,score4,score5,score_all]
    return score
     
def access_all(fobj,outfile):    
    start=time.time()
    num=0
    all=[0,0,0,0,0,0]
    for i, line in enumerate(fobj):
        num+=1
        poem=line.strip()
        score=access_quality(poem)
        for j in range(6):
            all[j]+=score[j]
        outfile.write(poem+"\n")
        outfile.write("押韵："+'%.2f' % score[0]+"\t平仄："+'%.2f' % score[1]+"\t流畅度："+'%.2f' % score[2]+"\t内容丰富度："+'%.2f' % score[3]+"\t主题鲜明度："+'%.2f' % score[4]+"\t总分："+'%.2f' % score[5]+"\n")
    end=time.time()
    print("共用时：",end-start)
    print("平均每首诗用时：",(end-start)*1.0/num)
    outfile.write("押韵："+'%.2f' % all[0]+"\t平仄："+'%.2f' % all[1]+"\t流畅度："+'%.2f' % all[2]+"\t内容丰富度："+'%.2f' % all[3]+"\t主题鲜明度："+'%.2f' % all[4]+"\t总分："+'%.2f' % all[5]+"\n")
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
    if args.input.name != '<stdin>':
        args.input = codecs.open(args.input.name, encoding='utf-8')
    if args.output.name != '<stdout>':
        args.output = codecs.open(args.output.name, 'w', encoding='utf-8')
    access_all(args.input,args.output)

if __name__ == '__main__':
    main() 


from tornado import web
import os
from generate import * 

poetry1="藏闲不管探明儿，头上经和细细忙。诗就尉锄林石伴，记随茆屋稻田香。"
poetry2="藏畋便欲索风淳，头角文章亦始悭。诗律赫方从北去，许风嘶领下江干。"
import re 
def add_enter(poetry):
    sen=[]
    temp=""
    s1=re.sub(u"，","， ",poetry)
    s1=re.sub(u"。","。 ",s1)
    s1=s1.split()
     
    return s1
ori_sen1=add_enter(poetry1)
ori_sen2=add_enter(poetry2)
      
class IndexHandler(web.RequestHandler):
    """主路由处理类"""
    ##对于不同的请求方式，我们用不同的方法
    def get(self,*args,**kwargs):
        """对应http的get请求方式"""
        
        self.render("index.html",
        key_words="藏头诗",
        poetry1=ori_sen1,
        poetry2=ori_sen2)
        
    
    def post(self):
        yan=self.get_body_argument("yan")   
        cang=self.get_body_argument("cang")
        key_words=self.get_body_argument("key_words")
        key_words=key_words.replace(" ","")
        p1,p2=handle_poem(key_words,yan,cang)
        if p1==1:
            self.render("index.html",key_words="藏头词在1-4字",poetry1=["","","",""],poetry2=["","","",""])
        elif p1==2:
            self.render("index.html",key_words="藏头词为中文",poetry1=["","","",""],poetry2=["","","",""])
        elif p1==3:
            self.render("index.html",key_words="未找到同音替换",poetry1=["","","",""],poetry2=["","","",""])
        else:
            p1=add_enter(p1)
            p2=add_enter(p2)
            self.render("index.html",
            key_words=key_words,
            poetry1=p1,
            poetry2=p2)
        




		




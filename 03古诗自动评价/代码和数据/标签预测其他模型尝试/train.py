import kashgari
from kashgari.embeddings import WordEmbedding
'''
embedding = WordEmbedding('<embedding-file-path>',
                           task=kashgari.CLASSIFICATION,
                           sequence_length=600)

# 初始化 BERT embedding
from kashgari.embeddings import BERTEmbedding
embedding = BERTEmbedding('bert-base-chinese',
                          task=kashgari.CLASSIFICATION,
                          sequence_length=600)
'''
# 使用 embedding 初始化模型
from kashgari.tasks.classification import BiLSTM_Model
#model = CNN_Model(embedding)
model = BiLSTM_Model()
#KMax_CNN_Model 0.3587 n=5
#BiGRU_Model 0.3667 n=3
#BiLSTM_Model 0.3772 n=3
import logging
logging.basicConfig(level='DEBUG')

kashgari.config.use_cudnn_cell = True


def to_list(poem):
    list=[]
    for zi in poem:
        list.append(zi)
    return list

def input_x_y(file):
    f=open(file,"r",encoding="utf-8")
    txt=f.readlines()
    x=[]
    y=[]
    for line in txt:
        s1=line.split('\t')
        poem=s1[0].rstrip()
        label=s1[1].rstrip()
        x.append(to_list(poem))
        y.append(label)
    return x,y
        
data_dir="E:/work/python/2019.12/按主题/data"
train_x, train_y=input_x_y(data_dir+"/trainData.tsv")
valid_x, valid_y=input_x_y(data_dir+"/devData.tsv")
test_x, test_y=input_x_y(data_dir+"/testData.tsv")

model.fit(train_x, train_y, valid_x, valid_y,epochs=3)

# 验证模型，此方法将打印出详细的验证报告
model.evaluate(test_x, test_y)

# 保存模型到 `saved_ner_model` 目录下
model.save('saved_classification_model')

# 加载保存模型
loaded_model = kashgari.utils.load_model('saved_classification_model')

# 使用模型进行预测
loaded_model.predict(test_x[:10])

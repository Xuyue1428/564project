import os


class Param():
    def __init__(self,yan5or7,tou_or_wei):
        self.batch_size=64
        self.n_epoch=100
        self.rnn_size=128
        self.num_layers=6
        self.vocab_size=11828
        self.clip_norm=5.
        self.yan5or7=yan5or7
        self.tou_or_wei=tou_or_wei
        self.save_dir="../../02藏头诗训练及生成/代码和数据/save/"+tou_or_wei+"/"+str(yan5or7)
        self.model_file="../../02藏头诗训练及生成/代码和数据/model/"+tou_or_wei+"/"+str(yan5or7)
        self.data_dir='../../02藏头诗训练及生成/代码和数据/data/'+str(yan5or7)
        self.log_dir='../../02藏头诗训练及生成/代码和数据/logs/'+tou_or_wei+"/"+str(yan5or7)
        self.metadata = 'metadata.tsv'
        self.train_pointer=0
        self.test_pointer=0
        self.learning_rate=0.002
        self.decay_steps = 1000
        self.decay_rate = 0.97
        self.BEGIN_CHAR='['
        self.END_CHAR=']'
        self.train_file = os.path.join(self.data_dir, "train.txt")
        self.test_file=os.path.join(self.data_dir, "test.txt")
        self.input_file=os.path.join(self.data_dir, "quan.txt")
        self.vocab_file = os.path.join(self.data_dir, "vocab.pkl")
        self.tensor_train = os.path.join(self.data_dir, "train.npy")
        self.tensor_test = os.path.join(self.data_dir, "test.npy")
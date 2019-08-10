'''
Created on 2019年8月2日

@author: stanis
'''
from gensim.models import word2vec
import logging,os
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)
cut_result='D:/zhwiki/zhwiki-20190720-pages-articles-multistream_xml/text/result_cut_word/'
 
class mycorpus(object):
    def  __init__(self,dir):
        self.dir=dir
    def __iter__(self):
        for filename in os.listdir(self.dir):
            for file in open(os.path.join(self.dir,filename),'r',encoding='utf-8'):
                yield file.split()

articles=mycorpus(cut_result)

#use word2vec训练分完词的数据，并存储模型          
article=word2vec.LineSentence(cut_result+'wiki_{:0>2d}'.format(0))
model=word2vec.Word2Vec(articles)
model.save('wiki-training.model')

#加载存储的模型
model=word2vec.Word2Vec.load('wiki-training.model')

print([key for key in model.most_similar('唐',topn=10)])
#输出结果：[('宋', 0.7449533343315125), ('魏', 0.6562801003456116), ('翟', 0.6480683088302612), ('裴', 0.647372305393219), ('邢', 0.6467240452766418), ('殷', 0.6460856795310974), ('宋初', 0.6406868696212769), ('娄', 0.6392995715141296), ('崔', 0.6378682255744934), ('马融', 0.6353722810745239)]
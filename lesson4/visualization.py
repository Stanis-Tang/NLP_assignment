'''
Created on 2019年8月2日

@author: stanis
'''
from gensim.models import word2vec

from sklearn.manifold import TSNE

import numpy as np
import matplotlib.pyplot as plt

#利用TSNE可视化模型结果，选取前200个词显示结果，结果见文件visualization.jpg
def tsne_plot(model):
    '''create and TSNE model and plots it'''
    lables=[]
    tokens=[]
    
    for word in model.wv.vocab:
        tokens.append(model[word])
        lables.append(word)
        
    tsne_model=TSNE(perplexity=40,n_components=2,verbose=1,init='pca',n_iter=2500,random_state=23)
    new_values=tsne_model.fit_transform(np.array(tokens[0:200])) #信息量过大，仅取前200
    
    x=[]
    y=[]
    for value in new_values:
        x.append(value[0])
        y.append(value[1])
    plt.figure(figsize=(16,16))
    for i in range(len(x)):
        plt.scatter(x[i],y[i])
        plt.annotate(lables[i],xy=(x[i],y[i]),xytext=(5,2),textcoords='offset points',ha='right',va='bottom')
    plt.show()


 
model=word2vec.Word2Vec.load('wiki-training.model')

tsne_plot(model)      
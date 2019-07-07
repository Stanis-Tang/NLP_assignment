'''
Created on 2019年7月1日

@author: stanis
'''
# 
# if __name__ == '__main__':
#     pass
import random
from collections import Counter
import pandas as pd
import jieba
import re
from _operator import add
from functools import reduce

human = """
human = 自己 寻找 活动
自己 = 我 | 俺 | 我们 
寻找 = 看看 | 找找 | 想找点
活动 = 乐子 | 玩的
"""

host = """
host = 寒暄 报数 询问 业务相关 结尾 
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = 耍一耍 | 玩一玩
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？"""

#如何通过grammar=host，取得target=‘host’？？
#返回句子
def generate(grammar=host,target='host',split_mark=' = '):
    return create_sentence(grammar_dict(grammar,split_mark),target)
  
def grammar_dict(grammar,split_mark):
    return {line.split(split_mark)[0]:[choice for choice in line.split(split_mark)[1].split(' | ')] for line in grammar.split('\n') if line!= '' }  

def create_sentence(grammar,target):
    if not target in grammar:
        return target;
    return ''.join([create_sentence(grammar, word) for word in random.choice(grammar[target]).split(' ')])
        


def token(string):
    return re.findall('\w+', string)

#training 
def corpus_train_1(filename='C:\\Users\\stanis\\Desktop\\course\\lesson_1\\train.txt'):
    #read txt，此处pandas的read_csv出错，没有使用。
    f=open(filename, 'r',encoding='utf-8')
    string=''.join([i for i in f.read()])
    f.close()
    #split into lines, delete marks
    article_list=[''.join(token(line.split(' ++$++ ')[2])) for line in string.split('\n') if line != '']
    #cut words using jieba
    cut_result=[]
    cut_result_2=[]
    for line in article_list:
        line_cut=list(jieba.cut(line))
        cut_result+=line_cut
        for  i in range(len(line_cut)-1):
            cut_result_2+=[line_cut[i]+line_cut[i+1]] #此处不加[]，会出错
        
    #calculate frequency of single word, and save
    fre_dict=dict(Counter(cut_result))
    #2-gram frequency
    fre_dict_2=dict(Counter(cut_result_2))

    return fre_dict,fre_dict_2

def corpus_train_2(filename='C:\\Users\\stanis\\Desktop\\course\\lesson_1\\movie_comments.csv'):
    #read txt，此处pandas的read_csv出错，没有使用。
    f=pd.read_csv(filename,encoding='utf-8',dtype={'id':str,"link":str,'name':str,'comment':str,'star':str})
    #cut words using jieba
    cut_result=[]
    cut_result_2=[]
    for line in enumerate(f['comment']):
         #此处按理而言，line应该就是str了，但是实际过程中发现第49355次循环，出现line不为str，结果为nan。 由于暂未想到解决方法，因此暂时先强制转化为str处理。
        line_cut=list(jieba.cut(''.join(token(str(line))))) 
        cut_result+=line_cut
        for  i in range(len(line_cut)-1):
            cut_result_2+=[line_cut[i]+line_cut[i+1]]
         
    #calculate frequency of single word, and save
    fre_dict=dict(Counter(cut_result))
    #2-gram frequency
    fre_dict_2=dict(Counter(cut_result_2))

    return fre_dict,fre_dict_2

#得到全局可使用的语料训练结果
word_dict,word_dict_2=corpus_train_1()

#calculate the probability 
def pro_2(word_dict,word):
    if not word in word_dict: return 0.5/reduce(add,[amount for amount in word_dict.values()])
    return word_dict[word]/reduce(add,[amount for amount in word_dict.values()])

def pro_sentence(sentence):
    word=list(jieba.cut(sentence))
    pro=1
    for i in range(len(word)-1):
        pro*=pro_2(word_dict_2, ''.join(word[i:i+2]))
    return pro
    

def generate_n(n=20):
    return [generate() for i in range(n)]

def generate_best():
#according to the pro_2 function's result, get the most probability of the sentence by 2-gram methods
    result=[]
    for i in generate_n():
        result.append([i,pro_sentence(i)])
    return sorted(result,key=lambda x:x[1],reverse=True)
#     return sorted(generate_n(),key=lambda x: pro_sentence(x))


for line in generate_best():
    print(line)










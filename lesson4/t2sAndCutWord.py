'''
Created on 2019年8月1日

@author: stanis
'''

from opencc import OpenCC
import jieba

read_dir='D:/zhwiki/zhwiki-20190720-pages-articles-multistream_xml/text/AA/'
cut_result='D:/zhwiki/zhwiki-20190720-pages-articles-multistream_xml/text/result_cut_word/'

#t2s（繁体转简体） jieba分词

cc=OpenCC('t2s')
for i in range(72):
    k='wiki_{:0>2d}'.format(i)
    file_read=open(read_dir+k,'r',encoding='utf-8')
    file_write=open(cut_result+k,'w',encoding='utf-8')
    for line in file_read:
        file_write.write(" ".join(jieba.cut(cc.convert(line)))+'\n') #保证分完词之后还是分行的，genism有分行要求
    file_read.close()
    file_write.close()
    print(k,'is finished')
  





'''
Created on 2019年7月11日

@author: stanis
'''

# if __name__ == '__main__':
#     pass

import requests,re
from bs4 import BeautifulSoup as bs
kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}

#得到所有地铁线的url
def data_crawler(url='https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485'):
    response=requests.get(url,headers=kv)
    #<a target=_blank href="/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%811%E5%8F%B7%E7%BA%BF">北京地铁1号线</a>   
    want_token=r'<a\s+target=_blank\s+href="(/item/\S+)">(北京地铁\S+线)</a>'
    pattern=re.compile(want_token)
    subway_lines=set(pattern.findall(response.content.decode('utf-8')))
    line_links={i[1]:'https://baike.baidu.com'+i[0] for i in subway_lines}
    sorted_links=sorted(line_links.items(),key=lambda x:x[0])
    return sorted_links
#大兴线为4号线延长线

#由于网页表格中包含站点信息，因此利用网页中的表格减少匹配错误和匹配量
def station_tables(string):
    response=requests.get(string,headers=kv)
    html_content=response.content.decode('utf-8')
    soup=bs(html_content,'lxml')
    tables=soup.find_all('table')
    return str(tables)

#根据每条线网页的特点使用不同的pattern得到站点信息
def station_names(tables):
    want_token_1=r'<td\s+align="center"\s+colspan="1"\s+rowspan="1"\s+valign="middle">(\S+)</td>' #1号线--6
    want_token_2=r'<th>(\S+)</th><td align="middle" valign="center" width="72">'#2号线--7
    want_token_3=r''#3号线未通
    want_token_4=r'</tr><tr><td align="center" colspan="1" rowspan="1" valign="middle">(\D+)</td><td align="center"'#4号线--8
    want_token_5=r'<a .*href="/item/\S+" target="_blank">(\S+站)</a></div>'#5号线--9
    want_token_6=r'</tr><tr><th>([\u4E00-\u9FA5]*)</th><td>'#6号线--10 #\u4E00-\u9FA5代表所有汉字在utf-8中的编码范围
    want_token_7=r'</td></tr><tr><th>([\u4E00-\u9FA5]*)</th><td'#7号线--11
    want_token_8=r''#8号线--12
    want_token_9=r''#9号线--13
    want_token_s1=r''#s1号线--14
    want_token_10=r''#10号线--1
    want_token_13=r''#13号线--2
    want_token_14=r''#10号线--3
    want_token_15=r''#10号线--4
    want_token_16=r''#10号线--5
    pattern=re.compile(want_token_6)
    return pattern.findall(tables)        
        
            

tables=station_tables(data_crawler()[9][1])
station=station_names(tables)
print(station)

#以6号线为例，print结果如下：
#['金安桥', '苹果园', '杨庄', '西黄村', '廖公庄', '田村', '海淀五路居', '慈寿寺', '花园桥', '白石桥南', '车公庄西', '车公庄', '平安里', '北海北', '南锣鼓巷', '东四', '朝阳门', '东大桥', '呼家楼', '金台路', '十里堡', '青年路', '褡裢坡', '黄渠', '常营', '草房', '物资学院路', '通州北关', '通运门', '北运河西', '北运河东', '郝家府', '东夏园', '潞城']





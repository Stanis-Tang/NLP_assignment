'''
Created on 2019年8月4日

@author: stanis
'''
####################由于数据问题，暂做1，2，4，5，6五条线的数据
import requests,json,re
from _collections import defaultdict
kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0"}

#非环线
line_1=['苹果园', '古城', '八角游乐园', '八宝山', '玉泉路', '五棵松', '万寿路', '公主坟', '军事博物馆', '木樨地', '南礼士路', '复兴门', '西单', '天安门西', '天安门东', '王府井', '东单', '建国门', '永安里', '国贸', '大望路', '四惠', '四惠东'] 
line_4=['安河桥北', '北宫门', '西苑', '圆明园', '北京大学东门', '中关村', '海淀黄庄', '人民大学', '魏公村', '国家图书馆', '动物园', '西直门', '新街口', '平安里', '西四', '灵境胡同', '西单', '宣武门', '菜市口', '陶然亭', '北京南站', '马家堡', '角门西', '公益西桥'] 
line_5=['宋家庄站', '刘家窑站', '蒲黄榆站', '天坛东门站', '磁器口站', '崇文门站', '东单站', '灯市口站', '东四站', '张自忠路站', '北新桥站', '雍和宫站', '和平里北街站', '和平西桥站', '惠新西街南口站', '惠新西街北口站', '大屯路东站', '北苑路北站', '立水桥南站', '立水桥站', '天通苑南站', '天通苑站', '天通苑北站'] 
line_6=['金安桥', '苹果园', '杨庄', '西黄村', '廖公庄', '田村', '海淀五路居', '慈寿寺', '花园桥', '白石桥南', '车公庄西', '车公庄', '平安里', '北海北', '南锣鼓巷', '东四', '朝阳门', '东大桥', '呼家楼', '金台路', '十里堡', '青年路', '褡裢坡', '黄渠', '常营', '草房', '物资学院路', '通州北关', '通运门', '北运河西', '北运河东', '郝家府', '东夏园', '潞城'] 
#环线
line_2=['西直门', '积水潭', '鼓楼大街', '安定门', '雍和宫', '东直门', '东四十条', '朝阳门', '建国门', '北京站', '崇文门', '前门', '和平门', '宣武门', '长椿街', '复兴门', '阜成门', '车公庄'] 


line_1=[i+'站' for i in line_1]
line_2=[i+'站' for i in line_2]
line_4=[i+'站' for i in line_4]
line_6=[i+'站' for i in line_6]
lines=[line_1,line_2,line_4,line_5,line_6]

#利用百度地图得到经纬度，不准改成高德地图
#baidu map_AK=M466kekczhrtp3GT0eC1vRUGp7p4aIcy
#http://api.map.baidu.com/geocoding/v3/?address=北京市海淀区上地十街10号&output=json&ak=您的ak&callback=showLocation
#https://restapi.amap.com/v3/geocode/geo?key=311ca8c7ef2248251b9a42c77fe950ca&address=地名    --高德api
def get_geocode(line):
    station_geocode=defaultdict()
#     want_token_lng='<lng>(\d+)</lng>'
#     want_token_lat='<lat>(\d+)</lat>'
    want_token_location='(\d+.\d+),(\d+.\d+)'
    for station_name in line:
        url='https://restapi.amap.com/v3/geocode/geo?key=311ca8c7ef2248251b9a42c77fe950ca&city=beijing&address=北京市'+station_name[0:-1]+'地铁站'
        response=requests.get(url,headers=kv)
        json_result=json.loads(response.content.decode('utf-8'))
        location=re.findall(want_token_location,json_result['geocodes'][0]['location'])
        station_geocode[station_name]=[float(location[0][0]),float(location[0][1])]
    return station_geocode

#得到每个站的经纬度
# stations_geocode=defaultdict()
# for line in lines:
#     stations_geocode.update(get_geocode(line))

#对每条线经纬度相差过大的站进行调整
# #line1    
# stations_geocode['苹果园站']=[116.177388,39.926727]
# stations_geocode['南礼士路站']=[116.354471,39.902138]
# #line2
# stations_geocode['前门站']=[116.397937,39.900192]
# #line6
# stations_geocode['郝家府站']=[116.717826,39.903195]
# stations_geocode['杨庄站']=[116.187004,39.92785]
# stations_geocode['花园桥站']=[116.310683,39.93234]
# stations_geocode['白石桥南站']=[116.32568,39.933022]
# #line5
# stations_geocode['天通苑北站']=[116.412888,40.083668]

# #将如下格式的字典存入文件station_geocode中
# #foramt: '潞城站':(116.4133836971231,39.910924547299565)
# with open('station_geocode','w') as f:
#     f.write(json.dumps(stations_geocode))
#     f.close()



#得到所有站的上下站
station_connection=defaultdict(list)
for line in lines:
    for i,station_name in enumerate(line):
        if i==0:
            station_connection[station_name].append(line[i+1])
        elif i==len(line)-1:
            station_connection[station_name].append(line[i-1])
        else:
            station_connection[station_name].append(line[i-1])
            station_connection[station_name].append(line[i+1])

#2号线为环线，对首尾站单独处理
station_connection[line_2[0]]+=[line_2[-1]]
station_connection[line_2[-1]]+=[line_2[0]]

#networkx,use station_connection & station_geocode
import math
import networkx as nx
import matplotlib.pyplot as plt
#load 站点经纬度
with open('station_geocode','r') as f:
    station_geocode=json.loads(f.read())
    f.close()
station_geocode_nx=station_geocode

#计算站点距离
def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = station_geocode[origin]
    lat2, lon2 = station_geocode[destination]
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d

# #显示站点分布，结果见文件station_location.png
# station_graph=nx.Graph()
# station_graph.add_nodes_from(list(station_geocode.keys()))
# nx.draw(station_graph,station_geocode_nx,with_labels=True,node_size=5)
# plt.show()

# #显示线路图，结果见文件lines.png
# station_con_graph=nx.Graph(station_connection)
# nx.draw(station_con_graph,station_geocode_nx,with_labels=True,node_size=5)
# plt.show()


#搜索路线
def search(station_connection,start,destination,sorted_methods):
    pathes=[[start]]
    seen=set()
    while pathes:
        path=pathes.pop(0)
        frontier=path[-1]
        if frontier in seen: continue
        for next in station_connection[frontier]:
            if next in path: continue
            new_path=path+[next]
            if next == destination: return new_path
            pathes.append(new_path)
        seen.add(frontier)
        pathes=sorted(pathes, key=sorted_methods)  

#按最少站    
def station_number(path):
    return len(path)

#按最短距离
def station_distance(path):
    distance=0
    lens=len(path)
    if lens==0: return distance
    for i in range(lens-1):
        distance+=geo_distance(path[i], path[i+1])
    return distance

print(search(station_connection,'南礼士路站','东大桥站',station_number))  
 
#最少站输出结果：['南礼士路站', '复兴门站', '西单站', '天安门西站', '天安门东站', '王府井站', '东单站', '建国门站', '朝阳门站', '东大桥站']   
#最短距离输出结果：['南礼士路站', '复兴门站', '西单站', '天安门西站', '天安门东站', '王府井站', '东单站', '建国门站', '朝阳门站', '东大桥站']



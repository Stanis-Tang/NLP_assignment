'''
Created on 2019年8月7日

@author: stanis
'''
from _collections import defaultdict
from functools import wraps


price=[2, 5, 8, 9, 10, 17, 17, 20, 24, 30, 31]

price_dict=defaultdict(int)

def memo(f):
    '''memos'''
    memo_cache={}
    @wraps(f)
    def wrappers(n):
        '''wrappers'''
        if n in memo_cache: return memo_cache[n]
        memo_cache[n]=f(n)
        return memo_cache[n]
    return wrappers
    
for i,p in enumerate(price):
    price_dict[i]=p

global called_time
called_time=defaultdict(int)
def get_call_time(f):
    '''calculate called times'''
    def wrapper(n):
        '''wrapper'''
        called_time[n]+=1
        return f(n)
    return wrapper

global solutions
solutions=defaultdict(list)

def parse_solution(length,solutions):
    left_len,right_len=solutions[length]
    if left_len==0:return [right_len]
    return parse_solution(left_len, solutions)+parse_solution(right_len, solutions)    
    
@get_call_time
@memo 
def r(n):
    """find the max"""
    max_price=max([(price_dict[n-1],0)]+[(r(i)[0]+r(n-i)[0],i) for i in range(1,n)],key=lambda x:x[0])
    solutions[n]=[max_price[1],n-max_price[1]]
    return max_price
                
# print(r(201)[0],parse_solution(201, solutions))
# print(called_time)
# print(solutions)


##########################################
#edit-distance
def editDistance(string1,string2,solution):
    '''calculate the difference of two strings'''

    if len(string1)==0: 
        k=[len(string2),'add {} '.format(string2)]
        return k
    if len(string2)==0: 
        k=[len(string1),'del {} '.format(string1)]
        return k
    tail1=string1[-1]
    tail2=string2[-1]
    print(string1[-1],string2[-1])
    if tail1==tail2:
        k=min([editDistance(string1[0:-1], string2,solution)[0]+1,'del {} '.format(string1[-1])+editDistance(string1[0:-1], string2,solution)[1]],[editDistance(string1, string2[0:-1],solution)[0]+1,'add {} '.format(string2[-1])+editDistance(string1, string2[0:-1],solution)[1]],[editDistance(string1[0:-1], string2[0:-1],solution)[0]+1,'sub {} by {} '.format(string1[-1],string2[-1])+editDistance(string1[0:-1], string2[0:-1],solution)[1]],key=lambda x:x[0])
        print(k)
        return k
    else:
        k=min([editDistance(string1[0:-1], string2,solution)[0]+1,'del {} '.format(string1[-1])+editDistance(string1[0:-1], string2,solution)[1]],[editDistance(string1, string2[0:-1],solution)[0]+1,'add {} '.format(string2[-1])+editDistance(string1, string2[0:-1],solution)[1]],[editDistance(string1[0:-1], string2[0:-1],solution)[0],editDistance(string1[0:-1], string2[0:-1],solution)[1]],key=lambda x:x[0])    
        print(k)
        return k
print(editDistance('1', '12',''))
###distance is right, solution is wrong

# def test():
#     assert editDistance('123456', '123')==3
#     assert editDistance('1253567998', '124356798')==2
#     print('No mistake')
# 
# test()
    




 
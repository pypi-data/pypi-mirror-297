from typing import List


##Arithmetic Progression
def arithprog( n: int, d: float, st: float = 0.0) -> List[float]:
    ret_list = []
    for i in range(1, n+1):
        num = st + (i - 1)*d
        ret_list.append(num)
    return ret_list



##Geometric Progression
def geomprog( n: int, r: float, st: float = 1.0) -> List[float]:
    ret_list = []
    for i in range(1, n+1):
        num = st*( r**(i - 1) )
        ret_list.append(num)
    return ret_list

#is numeric
def is_numeric(lst):
    return all(isinstance(k, (int, float)) for k in lst)


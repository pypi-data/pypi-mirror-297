from typing import List


##Arithmetic Progression
def arithprog( n: int, d: float, st: float = 0.0) -> List[float]:
    """
    This function generates a list of numbers following an arithmetic progression.

    :param int n: Length of the sequence.
    :param float d: Separation between the (k+1)th and kth term for any k.
    :param float st: Starting value of the sequence.
    :return: A list of numbers representing the arithmetic progression.
    :rtype: list[float]
    """
    ret_list = []
    for i in range(1, n+1):
        num = st + (i - 1)*d
        ret_list.append(num)
    return ret_list







##Geometric Progression
def geomprog( n: int, r: float, st: float = 1.0) -> List[float]:
    """
    This function generates a list of numbers following a geometric progression.

    :param int n: Length of the sequence.
    :param float d: Ratio of the (k+1)th to kth term for any k.
    :param float st: Starting value of the sequence.
    :return: A list of numbers representing the geometric progression.
    :rtype: list[float]
    """
    ret_list = []
    for i in range(1, n+1):
        num = st*( r**(i - 1) )
        ret_list.append(num)
    return ret_list

#is numeric
def is_numeric(lst):
    """
    This function returns True if all entries are numeric(int or float)

    :param list lst: A python list
    :return: A boolean bit specifying whether all members are numeric
    :rtype: list[float]
    """
    return all(isinstance(k, (int, float)) for k in lst)


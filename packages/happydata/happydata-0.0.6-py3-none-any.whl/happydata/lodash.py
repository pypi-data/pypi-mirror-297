from typing import List, Dict, Iterable, Generator, Callable,Any
import datetime,random

def groupby(l: Iterable, key: str| Callable) -> Dict:
    """group a list by key
    @param l: list of dict
    @param key: key to group by
    @return: dict of key -> list of item
    """
    if not l:
        return l
    if key and callable(key):
        d = {}
        for item in l:
            k = key(item)
            if k not in d:
                d[k] = []
            d[k].append(item)
        return d
    d = {}
    for item in l:
        k = item[key]
        if k not in d:
            d[k] = []
        d[k].append(item)
    return d

def indexby(l: Iterable, key: str| Callable) -> Dict:
    """index a list by key, keep the last one if duplicated
    @param l: list of dict
    @param key: key to index by
    @return: dict of key -> item
    """
    if not l:
        return l
    if key and callable(key):
        d = {}
        for item in l:
            d[key(item)] = item
        return d
    d = {}
    for item in l:
        d[item[key]] = item
    return d

def unique(l:List, fn:Callable=None) -> List:
    """unique list and keep order"""
    if not l:
        return l
    if fn and callable(fn):
        seen = set()
        return [x for x in l if not (fn(x) in seen or seen.add(fn(x)))]
    seen = set()
    return [x for x in l if not (x in seen or seen.add(x))]


def partition(l: Iterable,partition_size:int) -> Generator[List, None, None]:
    """Partition a list into partitions of size partition_size"""
    if l is None:
        return
    cur = []
    i = 0
    for v in l:
        cur.append(v)
        i += 1
        if i == partition_size:
            yield cur
            cur = []
            i = 0
    if cur:
        yield cur


def divide(l: List, num_partitions:int) -> List[List]:
    """Partition a list into num_partitions partitions"""
    if not l:
        return l
    partition_size = len(l)//num_partitions
    if partition_size == 0:
        partition_size = 1
    elif len(l) % num_partitions != 0:
        partition_size += 1
    return [l[i*partition_size : (i+1) * partition_size] for i in range (num_partitions)]

def flattern(l:List)->List:
    """flattern a list
    [1,[2,3],[4],[[2]]] -> [1,2,3,4 ,[2]]
    """
    if not l:
        return l
    return [x for i in l for x in (i if isinstance(i, list) or isinstance(i ,set) else [i])]

def flattern_deep(l:List)->List:
    """flattern a list deeply
    [1,[2,3],[4],[[2]]] -> [1,2,3,4 ,2]
    """
    if not l:
        return l
    return [x for i in l for x in (flattern_deep(i) if isinstance(i, list) or isinstance(i ,set) else [i])]

def index_of(l:List, v:Any|Callable)->int:
    """return the index of the first element , -1 not found """
    if callable(v):
        for i, e in enumerate(l):
            if v(e):
                return i
        return -1
    else:
        for i, e in enumerate(l):
            if e == v:
                return i
        return -1

def last_index_of(l:List, v:Any|Callable)->int:
    """return the index of the last element , -1 not found """
    if callable(v):
        for i, e in enumerate(reversed(l)):
            if v(e):
                return len(l) - i - 1
        return -1
    else:
        for i, e in enumerate(reversed(l)):
            if e == v:
                return len(l) - i - 1
        return -1


def now()->int:
    """return current time in seconds"""
    return int(datetime.datetime.now().timestamp())

def pick(d:Dict, keys:List)->Dict:
    """pick keys from a dict"""
    if not d or not keys:
        return d
    return {k: d[k] for k in keys if k in d}

def omit(d:Dict, keys:List)->Dict:
    """omit keys from a dict"""
    if not d or not keys:
        return d
    return {k: d[k] for k in d if k not in keys}

def compact(l:List)->List:
    """remove None, False, 0 from a list"""
    if not l:
        return l
    return [x for x in l if x]

def shuffle(l:List)->List:
    """shuffle a list"""
    l = [v for v in l]
    random.shuffle(l)
    return l

def sample(l:List, n:int)->List:
    """sample n elements from a list"""
    return random.sample(l, n)

def randstr(n:int, az=True,AZ=True, digits = True)->str:
    """generate a random string with length n"""
    s = ''
    if az:
        s += 'abcdefghijklmnopqrstuvwxyz'
    if AZ:
        s += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if digits:
        s += '0123456789'
    return ''.join(random.choices(s, k=n))


def union(*args:List)->List:
    """union multiple lists"""
    return list(set(flattern(args)))

def intersection(*args:List)->List:
    """intersection multiple lists"""
    return list(set.intersection(*map(set, args)))

def difference(a:List, b:List)->List:
    """difference of two lists"""
    return list(set(a) - set(b))

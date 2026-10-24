def sieve_list(n):
    if n<2:return []
    values=list(range(2,n+1));i=0
    while i<len(values) and values[i]**2<=n:
        p=values[i];j=i
        while j<len(values) and p*values[j]<=n:
            product=p*values[j]
            while product<=n:
                values.remove(product);product*=p
            j+=1
        i+=1
    return values
print(sieve_list(50))

def sieve_set(n):
    values=list(range(2,n+1));i=0
    while i<len(values) and values[i]**2<=n:
        remaining=set(values);p=values[i]
        for v in values[i:]:
            if p*v>n:break
            remaining.remove(p*v)
        values=sorted(remaining);i+=1
    return values
print(sieve_set(50))

from math import isqrt
from timeit import timeit
def trial(n):
    return [x for x in range(2,n+1) if all(x%d for d in range(2,isqrt(x)+1))]
for limit in range(0,101):assert sieve_list(limit)==sieve_set(limit)==trial(limit)
for size in (500,2000,5000):
    print(size, 'list:',timeit(lambda:sieve_list(size),number=1),
          'set:',timeit(lambda:sieve_set(size),number=1))
print('list.remove要查找并移动；set删除平均O(1)，但重建与排序仍有成本。')
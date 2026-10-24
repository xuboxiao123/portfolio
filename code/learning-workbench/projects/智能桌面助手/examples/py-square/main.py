def chars(number,seen):
    text=str(number);digits=set(text)
    return seen|digits if len(digits)==len(text) and not seen&digits else None
print(chars(784,set('025')),chars(676,set('025')))

def digits(number,seen):
    seen=set(seen)
    while number:
        number,d=divmod(number,10)
        if d in seen:return None
        seen.add(d)
    return seen
original={0,2,5}
print(digits(784,original),digits(841,original));print('原集合:',original)
assert original=={0,2,5}

def mask(number,seen=1):
    while number:
        number,d=divmod(number,10);bit=1<<d
        if seen&bit:return None
        seen|=bit
    return seen
from math import isqrt
answer=[i*i for i in range(isqrt(100)+1,isqrt(999)+1) if mask(i*i) is not None]
print(answer)
for number in range(100,1000):
    a=chars(number,{'0'});b=digits(number,{0});c=mask(number)
    assert (a is None)==(b is None)==(c is None)
print('三种表示对小变式逐项核对通过')
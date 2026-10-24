from random import Random
rng=Random(1);deck=list(range(8))
cut=sum(rng.randrange(2) for _ in deck)
left,right=deck[:cut],deck[cut:]
print('两堆:',left,right)

i=j=0;shuffled=[]
while i<len(left) and j<len(right):
    a=len(left)-i;b=len(right)-j
    if rng.randrange(a+b)<a:
        shuffled.append(left[i]);i+=1
    else:
        shuffled.append(right[j]);j+=1
    print(shuffled)
shuffled.extend(left[i:]);shuffled.extend(right[j:])
print('结果:',shuffled)
assert sorted(shuffled)==deck
assert [v for v in shuffled if v in left]==left
assert [v for v in shuffled if v in right]==right

import sys
import matplotlib.pyplot as plt
lengths=[];sizes=[];items=[]
for n in range(1,81):
    items.append(None);lengths.append(n);sizes.append(sys.getsizeof(items))
plt.plot(lengths,sizes);plt.xlabel('length');plt.ylabel('list bytes');plt.title('Capacity grows in steps')
print('此测量只含列表本身，不含它引用的元素。')
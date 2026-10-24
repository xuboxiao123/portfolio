devices={'d1','d2','d3'};rooms={'A','B','C'}
mapping={'d1':'A','d2':'A','d3':'B'}
assert set(mapping)==devices and set(mapping.values())<=rooms
injective=len(set(mapping.values()))==len(devices)
surjective=set(mapping.values())==rooms
print('单射:',injective,'满射:',surjective)

inverse={room:{d for d,r in mapping.items() if r==room} for room in rooms}
print(inverse)
assert inverse['A']=={'d1','d2'} and inverse['C']==set()
mapping={'d1':'A','d2':'B','d3':'C'}
assert len(set(mapping.values()))==len(devices) and set(mapping.values())==rooms
print('改成双射后可构造单值逆函数:',{r:d for d,r in mapping.items()})
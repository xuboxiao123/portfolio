eggs=2;moves=0;coverage=[0]*(eggs+1)
target=100

while coverage[eggs]<target:
    moves+=1
    for e in range(eggs,0,-1):coverage[e]=coverage[e]+coverage[e-1]+1
print(moves,coverage)

assert coverage[2]==moves*(moves+1)//2
print('两颗球下覆盖数为三角数；100层需最坏14次。')
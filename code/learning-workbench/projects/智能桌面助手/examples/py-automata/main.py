rule=110
outputs=[(rule>>i)&1 for i in range(8)]
print(dict(zip(range(8),outputs)))

width=41
row=[0]*width;row[width//2]=1
history=[row[:]]
for _ in range(20):
    padded=[0]+row+[0]
    row=[outputs[4*padded[i]+2*padded[i+1]+padded[i+2]] for i in range(width)]
    history.append(row[:])
for row in history:print(''.join('■' if b else ' ' for b in row))

import matplotlib.pyplot as plt
plt.figure(figsize=(8,4));plt.imshow(history,cmap='binary',interpolation='nearest')
plt.title('Rule '+str(rule));plt.xlabel('position');plt.ylabel('step')
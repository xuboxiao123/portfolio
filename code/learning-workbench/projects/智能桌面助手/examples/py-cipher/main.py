def transform(text,key,decode=False):
    if not key or not all('A'<=c<='Z' for c in key.upper()):raise ValueError('key应为英文字母')
    shifts=[ord(c)-65 for c in key.upper()];out=[];j=0
    for c in text:
        if 'A'<=c.upper()<='Z':
            base=65 if c.isupper() else 97
            delta=shifts[j%len(shifts)]*(-1 if decode else 1)
            out.append(chr(base+(ord(c)-base+delta)%26));j+=1
        else:out.append(c)
    return ''.join(out)

message='Design a smart product!';key='CODE'
cipher=transform(message,key)
print(cipher);print(transform(cipher,key,True))

assert transform(transform(message,key),key,True)==message
print('字符表、模26与逆向操作联系到9020的Z26。')

from string import printable
alphabet=printable[:-3];index={c:i for i,c in enumerate(alphabet)}
def table_cipher(text,key,sign=1):
    if not key or any(c not in index for c in key+text):raise ValueError('字符超出课堂字符表')
    return ''.join(alphabet[(index[c]+sign*index[key[i%len(key)]])%len(alphabet)] for i,c in enumerate(text))
plain='Sensor: 28.5 C!';key='Study!'
coded=table_cipher(plain,key)
print('字符表长度:',len(alphabet));print(repr(coded));print(table_cipher(coded,key,-1))
assert len(alphabet)==97 and table_cipher(coded,key,-1)==plain
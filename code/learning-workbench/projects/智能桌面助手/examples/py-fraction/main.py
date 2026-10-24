from math import gcd
def fraction(prefix,cycle):
    if not cycle or not all('0'<=c<='9' for c in prefix+cycle):
        raise ValueError('循环节非空，且只能含0..9')
    den=10**len(prefix)*(10**len(cycle)-1)
    num=int(prefix or '0')*(10**len(cycle)-1)+int(cycle)
    d=gcd(num,den)
    return num//d,den//d

for prefix,cycle in [('1','6'),('00','9'),('0','0'),('9','9')]:
    print(prefix,cycle,'->',fraction(prefix,cycle))

assert fraction('1','6')==(1,6)
assert fraction('0','0')==(0,1)
assert fraction('9','9')==(1,1)
print('零、循环9和约分均通过；用9020的整除性质解释gcd步骤。')
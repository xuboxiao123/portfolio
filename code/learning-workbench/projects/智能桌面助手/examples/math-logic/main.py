from itertools import product
for p,q in product([False,True],repeat=2):
    implication=(not p) or q
    print(p,q,'p=>q:',implication,'逆:',(not q) or p)
    assert not(p and q)==((not p) or (not q))

def command(hot,connected,manual):return (hot and connected) or manual
for hot,connected,manual in product([False,True],repeat=3):
    print(hot,connected,manual,'on' if command(hot,connected,manual) else 'off')
assert not command(True,False,False)
assert command(False,False,True)
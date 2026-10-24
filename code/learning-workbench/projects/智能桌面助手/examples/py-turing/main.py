rules={}
with open('rules.txt',encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith('#'):continue
        state,read,new_state,write,direction=line.split()
        if direction not in ('L','R') or read not in ('0','1') or write not in ('0','1'):raise ValueError('无效指令')
        key=(state,int(read))
        if key in rules:raise ValueError('同一状态与符号有重复指令')
        rules[key]=(new_state,int(write),direction)
print('规则数:',len(rules))

def divide_by_two(n, trace=False):
    if type(n) is not int or n<0:raise ValueError('输入应为非负整数')
    tape={i:1 for i in range(1,n+1)}
    state,pos='del1',1
    for step in range(10000):
        key=(state,tape.get(pos,0))
        if key not in rules:break
        new_state,new_bit,direction=rules[key]
        tape[pos]=new_bit
        pos += 1 if direction=='R' else -1
        state=new_state
        if trace:print(step+1,state,pos,''.join(str(tape.get(i,0)) for i in range(n+6)))
    else:raise RuntimeError('步数上限')
    return sum(v==1 for i,v in tape.items() if i>n+1)

n=6
answer=divide_by_two(n,trace=True)
print('输出:',answer)
assert answer==n//2
for n in range(20):assert divide_by_two(n)==n//2
print('0..19检查通过')
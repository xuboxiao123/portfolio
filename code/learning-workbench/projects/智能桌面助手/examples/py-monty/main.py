from random import Random
rng=Random(0)
trials=int(input('实验次数（例如10000）：'))
if not 1<=trials<=100000:raise ValueError('次数应为1..100000')

stay=switch=0
for _ in range(trials):
    prize=rng.randrange(3);first=rng.randrange(3)
    host=rng.choice([d for d in range(3) if d not in (prize,first)])
    other=next(d for d in range(3) if d not in (first,host))
    stay += first==prize
    switch += other==prize
print('不换:',stay/trials,'换门:',switch/trials)

assert stay+switch==trials
print('每轮两种策略恰有一种赢；样本比例不一定恰等于1/3与2/3。')
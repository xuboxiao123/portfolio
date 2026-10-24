import csv
with open('names.csv',encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
print(rows)

totals={}
for row in rows:
    name=row['name'];totals[name]=totals.get(name,0)+int(row['count'])
print(sorted(totals.items(),key=lambda item:(-item[1],item[0])))

assert sum(totals.values())==21
print('这里count已是人数，不能套用另一题的千人单位。')

from pathlib import Path
from collections import defaultdict
years=defaultdict(set)
for filename in sorted(Path('.').glob('yob*.txt')):
    year=int(filename.stem[3:])
    with filename.open(encoding='utf-8',newline='') as file:
        for name,gender,count in csv.reader(file):years[name].add(year)
revivals=[]
for name,values in years.items():
    ordered=sorted(values)
    for start,end in zip(ordered,ordered[1:]):revivals.append((end-start,start,name))
print(sorted(revivals,key=lambda x:(-x[0],x[1],x[2])))
assert (4,2020,'Alex') in revivals
print('4是再出现年份差；中间未出现的完整年份数为3。')
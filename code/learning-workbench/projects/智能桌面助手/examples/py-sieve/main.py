n=50
prime=[True]*(n+1)
prime[0]=prime[1]=False

p=2
while p*p<=n:
    if prime[p]:
        for multiple in range(p*p,n+1,p):prime[multiple]=False
    p+=1
answer=[i for i in range(n+1) if prime[i]]
print(answer)

assert answer==[i for i in range(2,n+1) if all(i%d for d in range(2,i))]
print('和小范围试除法结果相同；效率模型见复杂度卡。')
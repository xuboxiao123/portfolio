import json
packet={'device':'desk-01','temperature':29,'unit':'C'}
encoded=json.dumps(packet)
decoded=json.loads(encoded)
print(decoded)

def decide(p):
    value=p.get('temperature')
    if isinstance(value,bool) or not isinstance(value,(int,float)):
        raise ValueError('temperature必须是数字')
    return {'device':p.get('device'),'led':'on' if value>=28 else 'off'}
print(decide(decoded))

for bad in [{},{'temperature':True},{'temperature':'hot'}]:
    try:decide(bad)
    except ValueError as error:print('已拒绝:',bad,error)
print('电脑上的策略再发送到commands/led；真实MQTT、串口需设备和连接。')
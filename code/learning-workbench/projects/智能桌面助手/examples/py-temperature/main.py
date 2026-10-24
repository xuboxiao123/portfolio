def c_to_f(c):
    return c * 9 / 5 + 32
c_to_f(20)

for c in range(0, 31, 10):
    print(f'{c:4d} C -> {c_to_f(c):6.1f} F')

assert c_to_f(0) == 32
assert c_to_f(100) == 212
print('两端测试通过')
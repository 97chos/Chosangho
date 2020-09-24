"""
rainbow = ['red','orange','yellow','green','blue','navy','purple']

for color in rainbow :
    print(color)
"""
"""
def my_sum(numbers) :
    """"""numbers의 모든 요소 합 반환""""""
    total = 0
    for n in numbers :
        total += n
    return total

print(my_sum([1,2,3,4,5]))
"""
"""
total = 0

for n in [1,2,3,4,5,6,7,8,9,10] :
    if n%2==0 :
        total+=n

print(total)
"""
"""
for i in range(4) :
    print("현재 주기 :",i)
    continue
    print("나오면 안되는 워딩")
"""

for i in range(4) :
    print("현재주기 :",i)
    break
    print("나오면 안되는 워딩")
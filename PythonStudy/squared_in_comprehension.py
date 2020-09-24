numbers = [0,1,2,3,4,5,6,7,8,9]

print([e*e for e in numbers])

def squared(n) :
    return n*n
print(list(map(squared,numbers)))

print(list(map(lambda e:e*e, numbers)))
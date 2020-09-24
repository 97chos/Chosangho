numbers = [0,1,2,3,4,5,6,7,8,9]
total = 0

def length() :
    for e in numbers :
        total += 1
    return total

print(length(*numbers))

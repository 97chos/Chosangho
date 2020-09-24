def findmax(numbers) :
    """입력받은 수 중 가장 큰 수를 반환하는 함"""
    m=0
    for i in numbers :
        if m<i :
            m=i
        else :
            continue

    return m

print(findmax(list(map(int,input().split()))))



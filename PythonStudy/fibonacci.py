def fibonacci(n) :
    """n번째 피보나치 수열 반환"""
    if n==1 :
        return 1
    elif n==2 :
        return 1
    else :
        return fibonacci(n-1) + fibonacci(n-2)


for i in range(1,12) :
    print(fibonacci(i))

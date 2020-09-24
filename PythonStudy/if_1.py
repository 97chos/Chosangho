def absolute(n):
    """수 n을 입력받아 절댓값을 반환한다."""
    if n>=0:
        return n
    if n<0:
        return -n
print("절댓값을 입력하세요: ",end="")

a = int(input())
print(a,"의 절댓값 :",absolute(a))

def absolute_number(n) :
    """절댓값을 구하는 함수. 단, abs() 함수와 if문을 사용하지 않고 조건부 식만 사용"""
    abs=-n if n<=0 else n

    print(abs)

print("수를 입력하세요:",end="")
number=float(input())

absolute_number(number)
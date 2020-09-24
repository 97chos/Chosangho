def price(a):
    """상품 갯수에 따른 가격 변동 및 최종 금액 구하기"""
    if a<10 :
        md=100
    elif 10<=a<30 :
        md=95
    elif 30<=a<100 :
        md=90
    else :
        md=85

    end_price = a*md
    return end_price

print("상품의 개수를 입력하세요:",end="")
count = int(input())

print("최종 가격:",prce(count),"원")


prices = [2500, 3000, 1800, 3500, 2000, 3000, 2500, 2000]
"""
new_price = []                      "append를 이용해서서 가격 변경"
for price in prices :
    new_price.append(price+50)

print(new_price)
"""
"""
new_price = [price+50 for price in prices]          "원소나열법을 이용해서 가격 변경"

print(new_price)
"""
"""         
def plus50(n):                      "map()함수를 이용하여 가격 변경"
    return n+50

print(list(map(plus50,prices)))
"""

"print(list(map(lambda n:n+50,prices)))"        "위 map()함수를 이용한 가격 변경에서 lambda 식으로 변경"


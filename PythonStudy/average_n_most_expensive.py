prices = [2500, 3000, 1800, 3500, 2000, 3000, 2500, 2000]
"평균구하기"
total_price = 0
num_item = 0

for price in prices :
    total_price += price
    num_item += 1

aver = total_price / num_item

print(aver)

"최고값 구하기"
most_expensive = 0

for price in prices :
    if most_expensive < price :
        most_expensive = price

print(most_expensive)

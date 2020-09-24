total = 0

while True :
    print("더할 수를 입력하세요.")
    sum_total = input()

    if sum_total == "그만" :
        break

    if not sum_total.isnumeric() :
        print("잘못된 입력입니다.")
        continue

    total += int(sum_total)

    print("합계:",total)

print("프로그램을 종료합니다.")
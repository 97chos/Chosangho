print("금일 기온을 입력하세요 :",end="")
a = float(input())

if 28.0 <= a :
    print("바닷가에서 더위를 피한다.")
elif 16.0 <= a :
    print("한강에서 자전거를 탄다.")
elif 8.0 <= a :
    print("도서관에서 책을 읽는다.")
else :
    print("집에서 TC를 짠다.")
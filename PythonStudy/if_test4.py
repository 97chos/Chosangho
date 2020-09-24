def obesity(t,w) :
    """키와 몸무게를 입력받아 비만도를 측정하는 함수"""
    bmi = w/(t*t)
    if bmi<18.5 :
        print("저체중입니다.")
    elif 18.5<=bmi<23 :
        print("정상입니다.")
    elif 23<=bmi<25 :
        print("과체중입니다.")
    elif 25<=bmi :
        print("비만입니다.")
    else :
        print("잘못된 값을 입력하였습니다.")

print("키와 몸무게를 입력하세요.")
print("키(m):",end="")
tall=float(input())
print("몸무게(kg):",end="")
weight=float(input())

obesity(tall,weight)
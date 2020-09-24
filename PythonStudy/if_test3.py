def is_leap_year(y):
    """연도를 입력받아 윤년 여부를 판단하는 함수"""
    if y%4==0 and y%100!=0 :
        return "true"
    elif y%400==0 :
        return "true"
    else :
        return "false"

def days_in_month(year,month):
    """윤년 여부를 구하고, 해당 년도 달 일수를 구하는 함수"""
    if (0<month<=7 and month%2==1) or (8<=month<13 and month%2==0) :
        days=31
    elif (3<month<=7 and month%2==0) or (8<=month<13 and month%2==1) :
        days=30
    elif (is_leap_year(year)=="true") and (month==2) :
        days=28
    elif (is_leap_year(year)=="false") and (month==2) :
        days=29
    else :
        days="올바르지 않은 월을 입력하였습니다."

    print(days)

print("연도와 월을 입력하세요")
print("연도:",end="")
y = int(input())
print("월:",end="")
m = int(input())

days_in_month(y,m)


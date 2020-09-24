def 첫_짝수_찾기(numbers) :
    """numbers에서 첫번쨰 짝수를 찾아 출력하는 함수"""
    for n in numbers :
        if n%2==0 :
            print(n,"이(가) 첫 번째 짝수입니다.")
            break
    else :
        print("짝수가 없습니다.")

print("찾을 수를 입력하세요.")
n=list(map(int,input().split())) #map = 입력받은 리스트를 int 값으로 변경해줌 / split = 입력 값을 띄어쓰끼 기준으로 나눔
첫_짝수_찾기(n)
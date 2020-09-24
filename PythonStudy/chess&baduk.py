# 이곳에 체스말 데이터 유형 정의하기
# 체스말 유형은 다음 키를 갖는 사전이다.
# * x= 종
# * y= 행
# * color= 체스말 색
# * role= 체스말의 역할
체스말1 = {'type':'체스', 'x': 'A', 'y': '8', 'color': 'black', 'role': '룩'}
체스말2 = {'type':'체스', 'x': 'E', 'y': '1', 'color': 'white', 'role': '킹'}

# 이곳에 바둑돌 데이터 유형 정의하기
# 바둑돌 유형은 다음 키를 갖는 사전이다.
# * x= 가로축
# * y= 세로축
# * order= 수의 순서
# * color= 바둑돌의 색
바둑돌1 = {'type':'바둑', 'x': 8, 'y': 14, 'order': 83, 'color': '흑'}
바둑돌2 = {'type':'바둑', 'x': 12, 'y': 3, 'order': 84, 'color': '백'}


def print_piece(game) :
    if game['type'] == '체스' :
        return print(game['color']+game['role']+'이', game['x']+game['y'],'위치에 놓여 있어요.')

    elif game['type'] == '바둑' :
        return print('제',game['order'],'수:',game['color'],'이 (',game['x'],',',game['y'],') 위치에 두었습니다.')

print_piece(체스말1)
print_piece(체스말2)
print_piece(바둑돌1)
print_piece(바둑돌2)
board = [
    [['black', '룩'], None, None, None, None, None, None, None],
    [None, None, None, ['black', '킹'], None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, ['white', '비숍'], None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, ['white', '킹'], None, None, None],
]

for row in board:                 # 체스판(바깥쪽 리스트)의 각 행(요소)을 순회한다
    for piece in row:             # 행(안쪽 리스트)의 각 체스말(요소)을 순회한다
        if piece:                 # 체스말이 있으면 I를, 없으면 .을 출력한다
            print('I', end=' ')
        else:
            print('.', end=' ')
    print()

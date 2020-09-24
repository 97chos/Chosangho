coordinate_1 = {'x': 5, 'y': 3}   #점 (좌표)

triangle_1 = {                    #삼각형
    'type' : '삼각형',
    'point_a': {'x': 0, 'y': 0},
    'point_b': {'x': 3, 'y': 0},
    'point_c': {'x': 3, 'y': 4},
}

rectangle_1 = {                   #사각형
    'type' : '사각형',
    'point_a': {'x': 2, 'y': 2},
    'point_b': {'x': 6, 'y': 2},
    'point_c': {'x': 6, 'y': 6},
    'point_d': {'x': 2, 'y': 6},
}

import math   # 제곱근(math.sqrt()) 계산을 위해 수학 모듈 임포트

def sqaure(x) :
    """전달받은 수의 제곱수 반환"""
    return x*x

def distance(point_a,point_b) :
    """피타고라스의 정리를 이용하여 두 점 사이의 거리 구하기"""
    return math.sqrt(sqaure(point_a['x'] - point_b['x']) + sqaure(point_a['y'] - point_b['y']))

def circumference_of_triangle(shape):
    """삼각형 데이터를 받아 둘레의 길이를 반환"""
    a_to_b = distance(shape['point_a'],shape['point_b'])
    b_to_c = distance(shape['point_b'],shape['point_c'])
    c_to_a = distance(shape['point_a'],shape['point_c'])

    return a_to_b+b_to_c+c_to_a

def circumference_of_rectangle(shape):
    """사각형 데이터를 전달받아 둘레를 구해 반환한다."""
    a_to_b = distance(shape['point_a'], shape['point_b'])
    b_to_c = distance(shape['point_b'], shape['point_c'])
    c_to_d = distance(shape['point_c'], shape['point_d'])
    d_to_a = distance(shape['point_d'], shape['point_a'])

    return a_to_b + b_to_c + c_to_d + d_to_a

def circumference(shape) :
    if shape['type'] == '삼각형' :
        a_to_b = distance(shape['point_a'], shape['point_b'])
        b_to_c = distance(shape['point_b'], shape['point_c'])
        c_to_a = distance(shape['point_a'], shape['point_c'])

        return a_to_b + b_to_c + c_to_a

    elif shape['type'] == '사각형' :
        a_to_b = distance(shape['point_a'], shape['point_b'])
        b_to_c = distance(shape['point_b'], shape['point_c'])
        c_to_d = distance(shape['point_c'], shape['point_d'])
        d_to_a = distance(shape['point_d'], shape['point_a'])

        return a_to_b + b_to_c + c_to_d + d_to_a


print(circumference_of_rectangle(rectangle_1))
print(circumference_of_triangle(triangle_1))
print(circumference(rectangle_1))
print(circumference(triangle_1))
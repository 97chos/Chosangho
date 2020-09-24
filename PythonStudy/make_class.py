class Coordinate :
    """좌표를 나타내는 클래스"""
    x = 0,
    y = 0

"""Coordinate 클래스에 인스턴스 추가"""
point_1 = Coordinate()
point_2 = Coordinate()

"""각 인스턴스에 속성 추가"""
point_1.x = -1
point_1.y = 2
point_2.x = 2
point_2.y = 3

import math

def square(x) :
    """전달받은 수의 제곱수 구하기"""
    return x*x

def distance(point_a, point_b) :
    """피타고라스 방정식을 이용하여 두 점 사이 거리 구하기"""
    return math.sqrt(square(point_a.x - point_b.x) + square(point_a.y - point_b.y))

print(distance(point_1,point_2))


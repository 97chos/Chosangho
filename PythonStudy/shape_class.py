import math

def sqaure(x):
    """제곱 함수"""
    return x * x

class Coordinate :
    """속성 초기화 클래스"""
    def __init__(self,x=0,y=0) :
        self.x = x
        self.y = y

class Shape :
    """상위 클래스"""
    def desciription(self) :
         print("이 도형은 "+self.sides+"개의 변 갯수를 갖고 있습니다.")

class Triangle(Shape) :
    """삼각형 클래스"""
    def __init__(self, point_a, point_b, point_c) :
        """속성 초기화 메서드"""
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c

    def circumference(self) :
        """둘레 계산 메서드"""
        a_to_b = math.sqrt(sqaure(self.point_a.x - self.point_b.x) + sqaure(self.point_a.y - self.point_b.y))
        b_to_c = math.sqrt(sqaure(self.point_b.x - self.point_c.x) + sqaure(self.point_b.y - self.point_c.y))
        c_to_a = math.sqrt(sqaure(self.point_c.x - self.point_a.x) + sqaure(self.point_c.y - self.point_a.y))

        return  a_to_b  + b_to_c + c_to_a

    sides = '3'

class Rectangle(Shape) :
    """사각형 클래스"""
    def __init__(self, point_a, point_b, point_c, point_d) :
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        self.point_d = point_d

    def circumference(self) :
        """둘레 계산 메서드"""
        a_to_b = math.sqrt(sqaure(self.point_a.x - self.point_b.x) + sqaure(self.point_a.y - self.point_b.y))
        b_to_c = math.sqrt(sqaure(self.point_b.x - self.point_c.x) + sqaure(self.point_b.y - self.point_c.y))
        c_to_d = math.sqrt(sqaure(self.point_c.x - self.point_d.x) + sqaure(self.point_c.y - self.point_d.y))
        d_to_a = math.sqrt(sqaure(self.point_d.x - self.point_a.x) + sqaure(self.point_d.y - self.point_a.y))

        return a_to_b + b_to_c + c_to_d + d_to_a

    sides = '4'

Shape = [
    Triangle(Coordinate(0, 0), Coordinate(3, 0), Coordinate(3, 4)),
    Rectangle(Coordinate(2, 2), Coordinate(6, 2), Coordinate(6, 6), Coordinate(2, 6)),
]

for shape in Shape :
    shape.desciription()
    print('둘레 :',shape.circumference())
import math


class coordinate :
    """좌표를 나타내는 클래스"""

    """인스턴스 값 초기화 함수"""
    def __init__(self,x=0,y=0) :
        self.x = x
        self.y = y

    def distance(self, point_b) :
        return math.sqrt((self.x - point_b.x) * (self.x - point_b.x) +
                         (self.y - point_b.y) * (self.y - point_b.y))

"""인스턴스 값 생성 및 초기화"""

point_1 = coordinate(-1,2)
point_2 = coordinate(y=3,x=2)
point_3 = coordinate()
point_4 = coordinate(10)


print(point_1.x,point_1.y)
print(point_2.x,point_2.y)
print(point_3.x,point_3.y)
print(point_4.x,point_4.y)

print(point_1.distance(point_2))
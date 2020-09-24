import math

class Coordinate :
    """좌표를 나타내는 클래스"""
    x = 0,
    y = 0

    def distance(self,point_b) :
        return math.sqrt((self.x - point_b.x) * (self.x - point_b.x) +
                         (self.y - point_b.y) * (self.y - point_b.y))


"""인스턴스 값 생성"""
point_1 = Coordinate()
point_2 = Coordinate()

"""인스턴스에 x,y라는 속성 추가"""
point_1.x = -1
point_1.y = 2
point_2.x = 2
point_2.y = 3


print(point_1.distance(point_2))
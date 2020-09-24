class cake() :
    """케익을 나타내는 클래스"""
    coat = '생크림'
    price = '18,000원'
    topping = '과일'
    candles = '8개'


    def __init__(self,topping,price,candles) :
        self.topping = topping
        self.price = price
        self.candles = candles

    def describe(self) :
        print(self.coat)
        print('이 케익은',self.coat+'(으)로 덮여있다.')
        print(self.topping+'을(를) 올려 장식했다.')
        print('가격은',self.price+'이다')
        print('초는',self.candles+'가 꽂혀있다.')

class chocolateCake(cake) :
    """초콜렛 케익을 나타내는 클래스"""
    coat = '초콜릿'
    cacao_percent = 32.0

chocolateCake_1 = chocolateCake('이슬','12000원','9개')

print(chocolateCake_1.cacao_percent)
chocolateCake_1.describe()


class IcecreamCake(cake) :
    """아이스크림 케이크를 나타내는 클래스"""
    coat = '아이스크림'
    flavor = '정의하지 않은 맛'

    def __init__(self,price,flavor,topping,candles='0') :
        self.flavor = flavor
        """super = 상위 킆래스를 의미, 상위 클래스의 속성값 초기화"""
        super().__init__(price,topping,candles)

IcecreamCake_1 = IcecreamCake('쿠키','뉴욕치즈케이크','25,000원')


print(IcecreamCake_1.flavor)
IcecreamCake_1.describe()

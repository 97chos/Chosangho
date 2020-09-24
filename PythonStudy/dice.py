import random

class dice() :

    def __init__(self, x):
        self._sides = x

    def top(self) :
        _top = random.randint(1,self._sides)
        return _top

    def role(self):
        _role = random.randint(1,self._sides)
        return _role

dice_4 = dice(4)

print('사면체 주사위 테스트 ----')
print('처음 나온 면:', dice_4.top())
print('다시 굴리기:', dice_4.role())
print('다시 굴리기:', dice_4.role())

dice_100 = dice(100)

print('백면체 주사위 테스트 ----')
print('처음 나온 면:', dice_100.top())
print('다시 굴리기:', dice_100.role())
print('다시 굴리기:', dice_100.role())
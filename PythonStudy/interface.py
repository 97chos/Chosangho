class FruitJuice() :
    """과일 주스를 나타내는 클래스"""
    fruits = {'귤', '복숭아', '청포도','딸기', '사과'}     #넣을 수 있는 과일

    def __init__(self):
        self.ingredients = []

    def add_ingredients(self,ingredient) :
        if ingredient in self.fruits :
            self.ingredients.append(ingredient)

        else:
            print(ingredient,'은(는) 과일 주스에 넣을 수 없습니다.')

    def describe(self) :
        print('이 주스에는',len(self.ingredients),'개의 과일이 들어가있습니다.')
        print('넣은 재료 : ',end='')

        for ingredient in self.ingredients :
            print(ingredient,end=' ')



juice_1 = FruitJuice()
juice_1.add_ingredients('청포도')
juice_1.add_ingredients('도라지')
juice_1.add_ingredients('복숭아')
juice_1.describe()

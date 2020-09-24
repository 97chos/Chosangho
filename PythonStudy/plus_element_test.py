def plus_element(x,y) :
    for i,j in zip(x,y) :
        element_list = []
        element_list.append(i+j)
        print(element_list,end="")

a = (1,2,3)
b = [4,5,6]
plus_element(a,b)

#기대 결과 값 [5,7,9]
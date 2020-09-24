coll = [10, 5, 1, 9, 7, 3]

"""버블정렬 : 바로 옆 요소와 비교하여 정렬하는 방"""
for _ in coll :
    for i in range(len(coll)-1) :
        if coll[i] > coll[i+1] :
            coll[i], coll[i+1] = coll[i+1], coll[i]

print(coll)

print(sorted(coll))

print(sorted(coll, reverse=True))





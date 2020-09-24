diameters = [0.985, 0.992, 1.004, 0.995, 0.899, 1.001, 1.002, 1.003, 1.009, 0.998]

"""불량률 함수"""

def faulty_rate(n) :
    fault_sum=0
    total=0
    faulty=0
    for e in n :
        total += 1
        if e < 0.99 or e > 1.01 :
            fault_sum += 1
    faulty = (fault_sum/100)*total

    return faulty


print(faulty_rate(diameters))
import math
def time_predict(clocks, number_CPG, number_num):
    time_sum = 0
    if 'Horvath Clock' in clocks:
        time_sum = time_sum + 9.310446620181525e-05 * number_num * math.log(number_CPG)
        print('H working')
        print(time_sum)
    if 'Skin&Blood Clock' in clocks:
        time_sum = time_sum + 2.888888888888889e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'Zhang Clock' in clocks:
        time_sum = time_sum + 0.0004479738452328178 * number_num * math.log(number_CPG)
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'Hannum Clock' in clocks:
        time_sum = time_sum + 2.888888888888889e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'Weidner Clock' in clocks:
        time_sum = time_sum + 2.888888888888889e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'Lin Clock' in clocks:
        time_sum = time_sum + 2.888888888888889e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'PedBE' in clocks:
        time_sum = time_sum + 3.148148148148148e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'FeSTwo' in clocks:
        time_sum = time_sum + 1
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'MEAT' in clocks:
        time_sum = time_sum + 0.085 * number_num
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'AltumAge' in clocks:
        time_sum = time_sum + 2.888888888888889e-06 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'PhenoAge' in clocks:
        time_sum = time_sum + 2.888888888888889e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'BNN' in clocks:
        time_sum = time_sum + 2
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'EPM' in clocks:
        time_sum = time_sum + 2 * 2.888888888888889e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'Cortical Clock' in clocks:
        time_sum = time_sum + 4.6296296296296297e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'VidalBralo Clock' in clocks:
        time_sum = time_sum + 2.888888888888889e-07 * ( number_num * number_CPG ) / 60
        # time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
    if 'OriginalMethod' in clocks:
        # time_sum = time_sum + 0
        time_sum = time_sum + 55.86267972108915/600000 * number_num * math.log(number_CPG)
        print('H working')
        print(time_sum)
    return time_sum

def try_predict():
    return 'using'

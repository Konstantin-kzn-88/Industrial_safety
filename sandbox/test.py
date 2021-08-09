# данные из экселя
def power_data(max_r=60):

    radius = []
    power = [i / 100 for i in range(100)]

    for i in power:
        radius.append(max_r*i)
    power.sort(reverse=True)
    power_data = [power, radius]
    return power_data





if __name__ == '__main__':
    a = power_data()
    print(a)

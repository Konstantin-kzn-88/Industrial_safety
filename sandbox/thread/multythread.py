import threading

# Посчитаем уравнение y=x **2 + 4*x

def square_number(x):
    y1 = x ** 2
    return y1


def quadruple_num(x):
    y2 = 4 * x
    return y2


def wrapme(func, res, *args, **kwargs):
    res.append(func(*args, **kwargs))


# допустим x = 2
x = 2
res = []

t1 = threading.Thread(target=wrapme, args=(square_number, res, x,))
t2 = threading.Thread(target=wrapme, args=(quadruple_num, res, x,))
t1.start()
t2.start()
t1.join()
t2.join()

print(sum(res))  # 12
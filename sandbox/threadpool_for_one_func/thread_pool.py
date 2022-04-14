from concurrent.futures import ThreadPoolExecutor
import time

#
start_time = time.time()

obj = [1,2,3,4,5]

def square_number(x):
    time.sleep(2)
    y1 = x ** 2
    return y1

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(square_number, x) for x in obj]
    print(futures)
    print([f.result() for f in futures])

print("--- %s секунд ---" % (time.time() - start_time))



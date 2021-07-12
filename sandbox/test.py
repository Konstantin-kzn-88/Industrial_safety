
iter = int(input("Введеите целое число: "))

list_out = list(range(1,iter+1))
print(list_out)

i = 0
while i <= len(list_out)-1:
    print(list_out[i])
    i += 1
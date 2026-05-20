list_1 = [(x, x**2) for x in range(5)]
print(list_1)

gen = map(lambda x: 2**(x[0] + x[1]), list_1)
print(list(gen))

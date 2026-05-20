list_1 = [x for x in range(5)]

# using a named function instead of a lambda
def raise_two_to_the_power_of(x):
    return 2**x

list_2 = list(map(raise_two_to_the_power_of, list_1))
print(list_2)

for x in map(lambda x: x * x, list_2):
    print(x, end=' ')
print()
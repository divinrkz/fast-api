my_set = {1, 2, 4, 4, 5}
print(len(my_set))

my_set.discard(4)
for x in my_set:
    print(x)

my_set.clear()
print(my_set)
my_set.add(65)
print(my_set)
my_set.update([20, 293])
print(my_set)

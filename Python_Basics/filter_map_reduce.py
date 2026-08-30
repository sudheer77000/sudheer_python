from functools import reduce
num = [1,2,3,4,5,6,7,8,9]
evens = list(filter(lambda x :  x % 2 == 0,num))
doubles = list(map(lambda x :  x * 2 ,evens))
sum = reduce(lambda a,b : a + b,doubles,1)
print(evens)
print(doubles)
print(sum)
alpfa = ['a','b','c','d','e','f']
sum1 = reduce(lambda a,b : a + b,alpfa,"o")
print(sum1)
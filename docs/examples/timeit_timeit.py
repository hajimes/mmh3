import timeit

n = 1000000
result = timeit.Timer("for i in it: hex(i)", setup="it=range(10)").timeit(n)
print(f"mean time in seconds to execute hex: {result / n / 10}")

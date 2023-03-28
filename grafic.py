import matplotlib.pyplot as plt
import math

def func(x):
    a = -8
    b = 8
    eps = 0.1

    return (x + 1)*(math.trunc(math.log((b-a)/eps, x/2)) + 1)
h = 0.01

grid_n = [n for n in range(3, 20)]
grid_y = [func(x) for x in grid_n]

plt.scatter(grid_n, grid_y)
plt.xlabel('$n$')
plt.ylabel('$число вызовов функции$')
plt.title('$a=-8, b=8, eps=0.1$')
plt.grid(True)
plt.show()

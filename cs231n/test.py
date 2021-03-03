import numpy as np
t = 2**3
print(t)

x = np.random.randn(2,4)
y = (np.random.rand(*x.shape) < 0.5)/0.5

print(x)
print(y)
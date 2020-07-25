import pandas as pd
import copy
import numpy as np

a = np.zeros((28, 28), int)

switch = False
right = True

k = 0
for i in range(0, 14):
    for j in range(0, 28, 1):
        a[i][j] = k
        k += 1
        a[i+14][j] = k
        k += 1

a[:14] = a[13::-1]

a = a.T

a = pd.DataFrame(data=a)



print(a)


a.to_csv("symmetry.csv", header=False, index=False)




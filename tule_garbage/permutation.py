import pandas as pd

a = [[i+j*28 for i in range(28)] for j in range(28)]

a = pd.DataFrame(data=a)

a.to_csv("default.csv", header=False, index=False)
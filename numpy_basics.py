import pandas  as pd 
import numpy as np

list=[]
for i in range(100):
    list.append(i+1)

a=np.array(list)
print("original array is :")
print(a)
print("squared array is :")
print(a**2)
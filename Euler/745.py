import numpy as np, matplotlib.pyplot as plt
nums = np.arange(2,10**7+1)
sqrs = np.power(nums,2,dtype=np.int64)
gn = np.ones(10,dtype=np.int64)
#for i in sqrs:
 #   a = i*2
i = 0
while i<1000000000:
    i+=1
print(gn)
print(nums[:5])
print(nums[-1]**2)
print(sqrs[-1])
plt.plot(nums,sqrs)
plt.show()
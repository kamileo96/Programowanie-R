import numpy as np

class Circle():
    def __init__(self,x,y,r):
        x = x
        y = y
        r = r
    def circumference(self):
        return(2*np.pi*self.r)

    def intersection(self, B):
        a = [0,0]
        b = [0,0]
        return [a,b]

A = Circle(0,0,1)
A.r = 1
l = A.circumference()
print(l)
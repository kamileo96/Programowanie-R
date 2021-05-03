import math as m, numpy as np

class Velocity():
    beta = 0
    def __init__(self,beta=0):
        self.beta = beta
    def gamma(self):
        return 1/m.sqrt(1-self.beta**2)
    def __add__(self,other):
        return (self.beta+other.beta)/(1+self.beta*other.beta)
    def __str__(self):
        return(str(self.beta))

a = Velocity(0.5)
b = Velocity(0.5)
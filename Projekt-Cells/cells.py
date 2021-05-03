import numpy as np, math as m, matplotlib.pyplot as plt, time

#a - string złożony z 0,1,2. Nie ma potrzeby uogulniać dla innych baz
def base3to10(a):
    sum = 0
    i = 0
    for x in a[::-1]:
        sum += int(x)*3**i
        i += 1
    return sum
#b - int większy od zera
def base10to3(b):
    sum = b
    num = ""
    while sum>0:
        x = sum % 3
        num = str(int(x)) + num
        sum = (sum-x)/3
    return num
#args - int'y. Eksploruję możliwości uproszczania kodu własnymi funkcjami.
def stradd(*args):
    string = ""
    for arg in args: string += str(arg)
    return string

#f - funkcja w dziesiętnym. L,C,R - left,centre,right; int'y od 0 do 2.
def evolve(f,L,C,R):
    index = -base3to10(stradd(L,C,R))-1 #ważny minus, bo kolejność ma być malejąca. minus jedynka, bo od końca liczymy od 1 nie od 0.
    func = str(base10to3(f))
    while len(func)<27: func = "0"+func
    return int(func[index]) #jakie to proste!

#A - jednowymiarowy array int'ów od 0 do 2
def row_evolve(f,A):
    result = []
    i = 0
    for C in A:
        result.append(evolve(f,A[i-1],C,A[(i+1)%len(A)]))
        i += 1
    return result

def generator(f,r0,n):
    rows = [r0]

    for i in range(n):
        row = rows[-1]
        rows.append(row_evolve(f,row))
    return(rows)


#Main:
#dodać input??
f = int(np.random.rand()*10000000000000 % 7625597484986)
r0 = np.random.randint(0, 3, 300)
n = 200
"""
for f in range(10):
    rows = generator(f,r0,n)
    plt.matshow(rows)
    print(f)
    plt.show()
    time.sleep(1)
    plt.close()
"""
rows = generator(f,r0,n)
plt.matshow(rows)
plt.title(f'{n} steps of type {f} evolution')
print(f)
plt.show()
plt.close()
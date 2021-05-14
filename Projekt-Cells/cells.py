import numpy as np, math as m, matplotlib.pyplot as plt, sys
from matplotlib.colors import LinearSegmentedColormap
#import time -- do animacji (debug)

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
    index = -base3to10(stradd(L,C,R))-1 
    #ważny minus, bo kolejność ma być malejąca. minus jedynka, bo od końca liczymy od 1 nie od 0.

    func = str(base10to3(f))
    while len(func)<27: func = "0"+func
    return int(func[index]) 
    #jakie to proste!

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
f = int(sys.argv[1])
r0 = np.array([int(x) for x in str(sys.argv[2])])
n = int(sys.argv[3])

#debug:
"""
#f = 7654321#int(np.random.rand()*10000000000000 % 7625597484986)
#r0 = np.random.randint(0, 3, 200)
#print(r0)
#n = 200

for f in range(10):
    rows = generator(f,r0,n)
    plt.matshow(rows)
    print(f)
    plt.show()
    time.sleep(1)
    plt.close()
"""
#w tej skromnej pojedynczej linijce zaprzęgamy całą napisaną przez nas machinerię
rows = generator(f,r0,n)


"""
#tworzymy canvas o takich samych wymiarach, jak docelowe rows
#samo stworzenie canvas 2x2 tworzyłoby problemy dla innych proporcji rows niż 1:1. Robimy tak tylko dla 1x1, 1x2, 2x1.
#całe to zamieszanie po to, by mieć na colorbarze wszystkie wartości, nawet jeśli nasze rows nie będą jej zawierać (np dostaniemy macierz zer)
l = len(r0)

#if l/n < 0.5: l = n//2+1 
#próba naprawy tytułu wychodzącego poza ramkę skończyła się niepowodzeniem. 
#W takim przypadku druga połowa tytułu pozostawiona jest do odgadnięcia, jako zadanie dla czytelnika.

canvas = np.zeros([n+1,l])
if l<=2 and n+1<=2:
    canvas = np.zeros([2,2])
    canvas[0][0]=0
    canvas[0][1]=1
    canvas[1][0]=2
if l>= 3:
    canvas[0][0]=0
    canvas[0][1]=1
    canvas[0][2]=2
if n+1>=3:
    canvas[0][0]=0
    canvas[1][0]=1
    canvas[2][0]=2

#oszukuję pythona tworząc 
im_copy = plt.matshow(canvas, cmap='hot',origin='lower')
plt.colorbar(im_copy, shrink=0.3, aspect=3, boundaries=[-0.5,0.5,1.5,2.5], ticks=[0, 1, 2])

#działa
"""
#EDIT - nie działa. Zapomniałem że drugi matshow przyporządkuje złe kolory, gdy nie będziemy korzystać z samych zer (np same jedynki będą czarne)
#zdecydowałem się na trochę inny sposób naprawy, nie udało mi się osiągnąć tworzenia macierzy jedynek jako samych pomarańczowych kwadratów. 
# (musiałbym tworzyć własne mapy dla szczególnych przypadków)
#ten problem wyszedł w końcowej fazie testów i po prostu nie zdążyłem go rozwiązać
#kod zostawiam na wypadek gdybym kiedyś taką próbę podjął.



#kolory:
"""
#tworzę własne mapy (nie zdążyłem dokończyć na tyle, żeby działało). problem rozwiązałem naokoło dla jednokolorowych.
r = [0,255,255]
g = [0,92,255] #- środkowe wartości odpowiadają pomarańczowemu z 'hot'
b = [0,0,255]
cmaps = []
for i in range(2):
    cdict = {'red': (0, r[i], r[i]),
            'green': (0, g[i], g[i]),
            'blue': (0, b[i], b[i])}
    cmap = LinearSegmentedColormap('custom_cmap'+str(i), cdict)
    cmaps.append(cmap)
"""

arr = np.array(rows)
values = []
for i in range(3):
    if i in arr:
        values.append(i)

#if values == [0,1,2]: niepotrzebne.
boundaries=[-0.5,0.5,1.5,2.5] 
ticks=[0, 1, 2]
aspect=3
map_name='hot'
if values == [0,1]:
    boundaries=[-0.5,0.5,1.5] 
    ticks=[0, 1]
    aspect=2
    map_name='copper' #najlepsze co znalazłem
if values == [1,2]:
    boundaries=[0.5,1.5,2.5] 
    ticks=[1, 2]
    aspect=2
    map_name='Oranges_r'
if values == [0,2]:
    boundaries=[-1,1,3]
    ticks=[0, 2]
    aspect=2

if values == [0]:
    boundaries=[-0.5,0,0.5]
    ticks=[0]
    aspect=1
if values == [1]:
    boundaries=[0.5,1,1.5]
    ticks=[1]
    aspect=1
    map_name='Wistia_r'
if values == [2]:
    boundaries=[1.5,2,2.5]
    ticks=[2]
    aspect=1
    map_name='binary'
#obraz
im = plt.matshow(rows,fignum=0, cmap=map_name,origin='lower')
plt.colorbar(im, shrink=0.3, aspect=aspect, boundaries=boundaries, ticks=ticks)

#opis i legenda
plt.title(f' {n} kroków ewolucji typu: {f} ')

plt.xlabel('Numer komórki')
plt.gca().xaxis.tick_bottom()
plt.ylabel('Numer ewolucji')
plt.show()
plt.close()
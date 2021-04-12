import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as ani
FPS = 120
#FPS = int(input("Podaj liczbę klatek FPS animacji (polecane 120): "))
dt = 1/FPS

#t = 0. (niepotrzebne, bo dt jest stałe)

g = -9.81

m = float(input("Podaj masę m[kg]: "))
h = float(input("Podaj wysokość h[m]: "))
B = float(input("Podaj współczynnik oporu B[kg/m]: "))
v0 = float(input("Podaj prędkość v0 [m/s]: "))
alp = str(input("Podaj kąt alpha jaki tworzy v0 z osią Ox w radianach. Dodaj pi jeśli chcesz wyrazić ułamek pi lub deg jeśli chcesz podać w stopniach: "))

#errormessages
if m==0: print("Nie animujemy fotonów."), exit()
if m<0: print("Proszę wybierz pocisk z dostępnych na ziemi materiałów."), exit()
if h<0: print("Pocisk utknął w ziemi"), exit()
if B<0: print("Ciekawe...")#, exit()
if not alp[0].isdigit: print("Chyba się nie zrozumieliśmy. Podaj float i na końcu określ jego jednostkę."), exit()
if h>1000 or v0>100: print("Ostrożnie: dla wysokich parametrów h oraz v0 obliczenia potrafią być długie a animacja powolna.")


if alp[-2:] == "pi":
    alp = float(alp[:-2])
elif alp[-3:] == "deg":
    alp = np.deg2rad(float(alp[:-3]))
else:
    alp = float(alp)

    
x = 0.
y = h
xs = np.array([])
ys = np.array([])
vx = v0*np.cos(alp)
vy = v0*np.sin(alp)

#do animacji po odbiciu, dla max_odb = 0 animacja do pierwszego odbicia
odb = 0
max_odb = 0
max_odb = int(input("Podaj liczbę odbić n>=0 które chcesz zobaczyć. Podaj zero by nie animować żadnego odbicia: " ))
#Najpierw generuję dane, żeby nie spowalniać i tak już wolnej animacji
print("Generuję dane", end="\r")
count = 0
dots = 0

while odb < max_odb+1 :

    #żeby umilić czekanie na długie obliczenia... A tak naprawdę pozwala śledzić prędkość obliczeń.
    count += 1
    if count>10000:
        dots = (dots+1)%4
        print("Generuję dane"+dots*"."+(3-dots)*" ", end="\r")
        count = 0


    xs = np.append(xs, x)
    ys = np.append(ys, y)
    
    if (vy<0 and y<0):
        vy = -vy
        odb += 1

    #wiadome jest, że dokładniejszym algorytmem jest najpierw ustalenie przyspieszenia, następnie prędkości a finalnie położenia 
    #(niż odwrotnej kolejności)

    v = np.sqrt(vx**2+vy**2)
    ax = -B*v*vx/m
    ay = (-B*v*vy + g)/m

    vx += ax*dt
    vy += ay*dt

    x+=vx*dt
    y+=vy*dt

#Następnie wyświetlam dane:
print("Wyświetlam animację")

fig = plt.figure()
ns = np.arange(len(xs))
#przezroczysty wykres jako płótno (canvas) dla ustalenia osi
plt.plot(xs,ys, alpha=0)

print(plt.axis())

#plt.axis('equal') - obsolete, nie działa
plt.gca().set_aspect('equal', adjustable='box')
xmin, xmax, ymin, ymax = plt.axis()
plt.ylim(bottom=0, top=ymax+1)
plt.xlim(left=xmin-ymax*0.1,right=xmax+ymax*0.1)

#marker
ball, = plt.plot([0],[h],'ro',ms=20,mfc='r')
#ślad
trace, = plt.plot([0],[h])


def animate(i):
    ball.set_data(xs[i],ys[i])
    trace.set_data(xs[:i],ys[:i])
    return trace,ball,

#niestety, chociaż matematycznie animacja powinna odbywać się w czasie rzeczywistym
#(zmierzone z animacji g powinno wynosić 9,81)
#oraz liczba klatek powinna wynosić FPS, to w praktyce animacja często zostaje z tyłu.
Animation = ani.FuncAnimation(fig,animate,frames=ns,interval=dt*1000,blit=True,repeat=True)



plt.show()
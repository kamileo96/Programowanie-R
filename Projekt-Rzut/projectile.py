import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as ani

FPS = 120
#FPS = int(input("Podaj liczbę klatek FPS animacji (polecane 120): "))

#Tutaj zmieniamy z samej animacji do renderowania!
create_gif = False
if create_gif: FPS = 50

dt = 1/FPS

#t = 0. (niepotrzebne, bo dt jest stałe)

g = -9.81#[m/s^2]

m, h, B, v0, alp = 1, 10, 0.035, 7, "45deg" #deafult values (edit: dla źle podanych i tak nie działa)

#input:
m = float(input("Podaj masę m[kg]: "))
h = float(input("Podaj wysokość h[m]: "))
B = float(input("Podaj współczynnik oporu B[kg/m]: "))
v0 = float(input("Podaj prędkość v0 [m/s]: "))
alp = str(input("Podaj kąt alpha jaki tworzy v0 z osią Ox w radianach. \n\
Dodaj na końcu 'pi' jeśli chcesz wyrazić ułamek pi lub 'deg' jeśli chcesz podać w stopniach: "))

#errormessages
if m==0: print("Nie animujemy fotonów."), exit()
if m<0: print("Proszę wybierz pocisk z dostępnych na ziemi materiałów."), exit()
if h<0: print("Pocisk utknął w ziemi"), exit()
if B<0: print("Ciekawe...")#, exit()
if not alp[0].isdigit: print("Chyba się nie zrozumieliśmy. Podaj float i na końcu określ jego jednostkę."), exit()
if h>=1000 or v0>=100: print("Ostrożnie: dla wysokich parametrów h oraz v0 obliczenia potrafią być długie a animacja powolna.")

#konwerter jednostek alp
if alp[-2:] == "pi":
    alp = float(alp[:-2])*np.pi
elif alp[-3:] == "deg":
    alp = np.deg2rad(float(alp[:-3]))
else:
    alp = float(alp)

#do animacji po odbiciu, dla max_odb = 0 animacja do pierwszego odbicia
odb = 0
max_odb = 0
max_odb = int(input("Podaj liczbę odbić n>=0 które chcesz zobaczyć. Podaj zero by nie animować żadnego odbicia: " )) #<-zakomentować jeśli niepotrzebne

#skalowanie - lekka optymalizacja dla dużych wysokości.
is_scaled = False
vy0 = v0*np.sin(alp)
if vy0<0 and max_odb == 0:
    expected_h = h
else:
    expected_h = h + (vy0*vy0)/(2*(-g)) #energetyczne oszacowanie, nie do końca dokładne dla dużych B

scale = int(np.log10(expected_h))

if scale>=3: 
    scale = scale - 2
    h = h/(10**scale)
    v0 = v0/(10**scale)
    g = g/(10**scale)
    is_scaled = True

#warunki początkowe
x = 0.
y = h
xs = np.array([])
ys = np.array([])
vx = v0*np.cos(alp)
vy = v0*np.sin(alp)


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
#opisy osi etc
if not is_scaled:
    plt.xlabel("x[m]")
    plt.ylabel("y[m]")
else:
    plt.xlabel(f"x[m·$10^{scale}$]")
    plt.ylabel(f"y[m·$10^{scale}$]")
#Dla zachowania ścisłości przy skalowaniu



plt.title("Animacja rzutu")
#plt.grid("major") optional, usunięte dla zwiększenia płynności 
#(chociaż mamy włączony blitting, więc możliwe że niewiele zmienia, bo grid jest nieruchomy)

#plt.axis('equal') - obsolete, nie działa
plt.gca().set_aspect('equal', adjustable='box')
#limity proponowane przez nasze canvas:
xmin, xmax, ymin, ymax = plt.axis()

plt.ylim(bottom=0, top=ymax*1.05)
plt.xlim(left=xmin-ymax*0.1,right=xmax+ymax*0.1)
#drobne poprawki, żeby kula mieściła się w kadrze.
#długi rzut horyzontalny nie jest możliwy, ale dla wysokiego rzutu pionowego potrzebujemy skalujących się limitów.
#(rozmiar kuli skaluje się z wielkością wykresu)


#ślad
trace, = plt.plot([0],[h])
#marker
ball, = plt.plot([0],[h],'ro',ms=20,mfc='r')



def animate(i):
    trace.set_data(xs[:i],ys[:i])
    ball.set_data(xs[i],ys[i])
    return trace,ball,

#niestety, chociaż matematycznie animacja powinna odbywać się w czasie rzeczywistym
#(zmierzone z animacji g powinno wynosić 9,81, a czas trwania powinien trwać len(xs)*dt)
#oraz liczba klatek powinna wynosić FPS, to w praktyce animacja często zostaje z tyłu.
Animation = ani.FuncAnimation(fig,animate,frames=ns,interval=dt*1000,blit=True,repeat=True)


plt.show()


#Możliwym fixem jest zmiejszenie ilości klatek do obsługiwanej przez .gif (50) i zapisanie animacji.
if create_gif:
    print("Renderuję animację...")
    Animation.save("animation.gif",fps=FPS)
    print("Gotowe")
#można sprawdzić, że czas takiej animacji wynosi mniej więcej len(xs)*dt, czyli się zgadza.


#możnaby też adaptacyjnie zmieniać liczbę animowanych klatek dla długich animacji:
#if len(xs)>???: xs = xs[::2]...
#lub short = len(xs)%???, xs = xs[::short]...

#innym, może najlepszym sposobem byłoby skalowanie całej animacji: h = h/10^n...
#i następnie oznaczenie osi [10^n m]
#musielibyśmy jednak przed animacją zgadnąć, że będzie ona powolna.

#po zastanowieniu umieściłem ten warunek, dla dużych h. 
#pozostałoby przeprowadzić prasymulację, żeby zobaczyć czy duże v0 nie spowoduje opóźnień animacji.
#zamiast tego decyduję się na szacowanie energetyczne.
#niestety zmiana skali w niewielkim stopniu optymalizuje animację



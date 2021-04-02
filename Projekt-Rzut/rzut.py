import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as ani
FPS = 120
dt = 1/FPS
t = 0.

g = -9.81

m = 1.
h = 1.
B = 0.1
v0 = 10.
alp = np.pi/4

x = 0.
y = h
xs = np.array([])
ys = np.array([])
vx = v0*np.cos(alp)
vy = v0*np.sin(alp)

#do animacji po odbiciu, dla max_odb = 0 animacja do pierwszego odbicia
odb = 0
max_odb = 4

#Najpierw generuję dane

while odb < max_odb+1 :
    xs = np.append(xs, x)
    ys = np.append(ys, y)
    
    if (vy<0 and y<0):
        vy = -vy
        odb += 1

    v = np.sqrt(vx**2+vy**2)
    ax = -B*v*vx/m
    ay = (-B*v*vy + g)/m

    vx += ax*dt
    vy += ay*dt

    x+=vx*dt
    y+=vy*dt

#Następnie wyświetlam dane:


fig = plt.figure()
ns = np.arange(len(xs))
#przezroczysty wykres jako płótno dla ustalenia osi
plt.plot(xs,ys, alpha=0)
#plt.axis('equal')
plt.ylim(bottom=0)
#marker
ball, = plt.plot([0],[h],'ro',ms=20,mfc='r')
#ślad
trace, = plt.plot([0],[h])
#ziemia
xmin, xmax, ymin, ymax = plt.axis()

def animate(i):
    ball.set_data(xs[i],ys[i])
    trace.set_data(xs[:i],ys[:i])
    return trace,ball,

print([xs,ys])

Animation = ani.FuncAnimation(fig,animate,frames=ns,interval=dt*1000,blit=True,repeat=True)



plt.show()
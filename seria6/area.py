import math as m, sys
if len(sys.argv)<4: print("Brak wystarczającej liczby argumentów"); exit()
a = sys.argv[1]
b = sys.argv[2]
c = sys.argv[3]
l = [a,b,c]
for x in l:
    try:
        x = float(x)
    except ValueError:
        print(f'"{x}" nie jest liczbą. Podaj liczbę.')
        exit()
a,b,c = float(a),float(b),float(c)

def Nierownosc_weglowskiego():
    print(f"Nie da się zbudować trójkąta o bokach {a}, {b}, {c}")
    exit()

if a>=b+c or b>=a+c or c>=a+b:
    Nierownosc_weglowskiego()


p = (a+b+c)/2
S = m.sqrt(p*(p-a)*(p-b)*(p-c))

print("Pole: "+str(S))
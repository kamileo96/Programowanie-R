import networkx as nx, matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph 
class MyGraph:
    def __init__(self, instruction, new_nodes=[]):
        self.edges = instruction
        self.nodes = []
        self.real_nodes = []
        self.g_edges = []
        self.new_nodes=new_nodes
        for e in instruction:
            #lista wierzcholkow
            if not e[0] in self.nodes:
                self.nodes.append(e[0])
                self.real_nodes.append(e[0])
            if not e[1] in self.nodes:
                self.nodes.append(e[1])
                self.real_nodes.append(e[1])
            #edges w formacie nx
            self.g_edges.append((e[0],e[1]))
        
        #próbuję móc tworzyć grafy z kropkami:
        for n in self.new_nodes:
            if not n in self.nodes:
                self.nodes.append(n)

        #można prościej, ale tak najlepiej rysuje (debug) (czyżby?):
        self.G = nx.Graph()
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.g_edges)

    def Disconect(self,n):
        #zwraca siebie z "dziurą" zamiast wierzchołka n
        n_edges = self.edges.copy()
        nnds = self.nodes.copy()
        nnds.remove(n)
        for e in self.edges:
            if n in e:
                
                n_edges.remove(e)
        #przekazuję kropki:


        return(MyGraph(n_edges,nnds))
    def Short(self,n):
        #zwraca siebie ze "zwarciem" - połączeniem zamiast wierzchołka n
        #Działa tylko dla dwóch sąsiadów!!! inaczej wypisuje błąd i robi to co Disconect()
        #przekazuję kropki:
        nnds = self.nodes.copy()
        nnds.remove(n)
        
        n_edges = self.edges.copy()
        neibrs = []
        for e in self.edges:
            if n in e:
                n_edges.remove(e)
                if not Neighbour(n, e) == n:
                    neibrs.append(Neighbour(n, e))
        if len(neibrs) == 2:
            n_edges.append(neibrs)
        else:
            print("Błąd - próbujesz zastosować zwarcie przy mniejszej/większej ilości sąsiadów")

        return(MyGraph(n_edges,nnds))

    def Undot(self):
        #zwraca listę: [liczba,self_bez_kropek]
        #odkropkowanie (zgodnie z zasadą, że kropka zwiększa liczbę sześciokrotnie)
        #być może się nie przyda
        dot_count = 0
        for n in self.nodes:
            if n not in self.real_nodes:
                dot_count += 1
        return([6**dot_count,MyGraph(self.edges)])
                

def Neighbour(n,e):
    #zwraca element z pary nie będący n (chyba że oba są n)
    if n == e[0]:
        return(e[1])
    elif n == e[1]:
        return(e[0])
    print("Błąd - nie znaleziono")
    return(None)

def Connected(n,edges):
    c = []
    for e in edges:
        if n == e[0]:
            c.append(e[1])
        elif n == e[1]: #zdecydowałem się na konwencję, gdzie loop liczy się za 1 edge. Stąd elif.
            c.append(e[0])
    return(c)
def Simplify(mg):
    for n in mg.nodes:
        c = Connected(n,mg.edges)
        total = len(c) #połączenia
        loops = c.count(n) #połączenia ze sobą
        real = total - loops #połączenia z innymi

        #te trzy wartości wystarczą do rozpoznania czy możemy uprościć.
        #jeśli znajdziemy możliwość uproszczenia, wychodzimy z pętli (przez return)
        #format: return([[liczba1,uproszczony1],[liczba2,uproszczony2]])
        #niektóre ify możnaby uprościć, np w gałęzi nie muszę sprawdzać czy nie mam do czynienia z jedną pętlą, ale zostawię dla przejrzystości

        #kropka
        if total == 0:
            return([[6,mg.Disconect(n)]])
            print("k")           
        #dwie pętle lub jedna pętla
        if (total == 2 and loops == 2) or (total == 1 and loops == 1):
            return([[4,mg.Disconect(n)]])
            print("p")

        #róg
        if total == 2 and loops == 0:
            print("r")
            return([[1,mg.Short(n)],[1,mg.Disconect(n)]])
            print("r")
        
        #róg z pętelką
        if total == 3 and loops == 1:
            return([[1,mg.Short(n)]])
            print("rp")

        #gałąź
        if total == 1 and loops == 0:
            return([[3,mg.Disconect(n)]])
            print("g")

        #gałąź z pętelką
        if total == 2 and loops == 1:
            return([[2,mg.Disconect(n)]])
            print("gp")            

    #Tu dochodzimy jeśli nie da się uprościć
    #na razię zwrócę False, ale możliwe że zmienię na [-1,mg], -1 byłoby kodem po którym main wiedziałby, że nie nastąpiła żadna redukcja.
    return(False)

#main
x = MyGraph([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 1]])

work = [x]
done = []

#while len(work)>0:
#    cg = work.pop() #current graph
#    sg = Simplify(cg) #simplified graphs (list of lists)





#x = MyGraph([[1,2],[2,3],[3,1]])
#y = MyGraph([[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 1],[1,1],[1,1]])
simp = Simplify(x)
print(simp)
y = simp[0][1]
#z = simp[1][1]
print(y.edges)
#print(simp[1][1].edges)
#print(nx.is_isomorphic(x.G,y.G))

#debug. jeśli zainstalujemy 2.6 networkx'a, zobaczymy self-loops - niestety tylko jedną.
#Strzałki są zbyteczne, ale mogą pomóc.

nx.draw(y.G,with_labels=True)
plt.show()

#nx.draw(z.G,with_labels=True)
#plt.show()

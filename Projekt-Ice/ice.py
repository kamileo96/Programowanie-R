import networkx as nx, matplotlib.pyplot as plt, ast
from networkx.drawing.nx_agraph import to_agraph 
class MyGraph:
    def __init__(self, instruction, new_nodes=[]):
        self.edges = instruction
        self.nodes = []
        self.real_nodes = [] #nodes które mają edge's
        self.g_edges = [] #edges w formacie nx
        self.new_nodes=new_nodes #opcjonalne "kropki" przekazane przy tworzeniu
        for e in instruction:
            #lista wierzcholkow
            if not e[0] in self.nodes:
                self.nodes.append(e[0])
                self.real_nodes.append(e[0])
            if not e[1] in self.nodes:
                self.nodes.append(e[1])
                self.real_nodes.append(e[1])
            
            self.g_edges.append((e[0],e[1]))
        
        #dodaję kropki:
        for n in self.new_nodes:
            if not n in self.nodes:
                self.nodes.append(n)

        #tworzę odpowiednik grafu w nx, do sprawdzania izomorfizmu i rysowania
        #można prościej, ale tak najczytelniej:
        self.G = nx.MultiGraph()
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.g_edges)

    def __repr__(self):
        #przydatne do debugu
        return f"nodes: {str(self.nodes)}; edges: {str(self.edges)}"

    def Disconect(self,n):
        #zwraca siebie z "dziurą" zamiast wierzchołka n (type MyGraph)
        n_edges = self.edges.copy()
        #przekazuję "kropki"
        nnds = self.nodes.copy()
        nnds.remove(n)
        for e in self.edges:
            if n in e:
                
                n_edges.remove(e)


        return(MyGraph(n_edges,nnds))
    def Short(self,n):
        #zwraca siebie ze "zwarciem" - połączeniem zamiast wierzchołka n (type MyGraph)
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
        #być może się nie przyda (możliwe byłoby zaimplementowanie w celu optymalizacji)
        #nie przydało się
        dot_count = 0
        for n in self.nodes:
            if n not in self.real_nodes:
                dot_count += 1
        return([6**dot_count,MyGraph(self.edges)])

    def SmoothEdges(self):
        #no pun intended
        #przenumerowuje wierzchołki (w liście krawędzi) i sortuje
        #funkcjonalność czysto wizualna
        #zwraca listę krawędzi (jak instrukcja, czyli nie może zwrócić kropek)
        
        s_edges = []
        for e in self.edges:
            new_e = [self.real_nodes.index(e[0])+1, self.real_nodes.index(e[1])+1]
            new_e.sort()
            s_edges.append(new_e)
        s_edges.sort()
        return(s_edges)
                

def Neighbour(n,e):
    #pomocnicze
    #zwraca element z pary nie będący n (chyba że oba są n)
    if n == e[0]:
        return(e[1])
    elif n == e[1]:
        return(e[0])
    print("Błąd - nie znaleziono")
    return(None)

def Connected(n,edges):
    #zwraca sąsiadów, w tym siebie za każdy loop.
    #każdy sąsiad raz za każde połączenie z nim
    c = []
    for e in edges:
        if n == e[0]:
            c.append(e[1])
        elif n == e[1]: #zdecydowałem się na konwencję, gdzie loop liczy się za 1 edge. Stąd elif.
            c.append(e[0])
    return(c)

def AddPairs(pair, ls):
    #dodaję liczebności izomorficznych grafów
    #funkcja na danym ls (zmienianie ls.copy() i return pewnie byłoby wolniejsze)
    for p in ls:
        if nx.is_isomorphic(pair[1].G,p[1].G):
            p[0] += pair[0]
            return
    ls.append(pair)
    
def Simplify(mg):
    #input: MyGraph
    #output: MyGraph z jednym uproszczeniem, LUB:
    #False, jeśli nie da się uprościć
    #dwa typy outputu niezbyt eleganckie, ale działają.
    for n in mg.nodes:
        c = Connected(n,mg.edges)
        total = len(c) #połączenia
        loops = c.count(n) #połączenia ze sobą
        #real = total - loops #połączenia z innymi

        #te dwie (#trzy) wartości wystarczą do rozpoznania czy możemy uprościć.
        #jeśli znajdziemy możliwość uproszczenia, wychodzimy z pętli (przez return)
        #format: return([[liczba1,uproszczony1],[liczba2,uproszczony2]])
        #niektóre ify możnaby uprościć, np w gałęzi nie muszę sprawdzać czy nie mam do czynienia z jedną pętlą, ale zostawię dla przejrzystości

        #kropka
        if total == 0:
            return([[6,mg.Disconect(n)]])
        #dwie pętle lub jedna pętla
        if (total == 2 and loops == 2) or (total == 1 and loops == 1):
            return([[4,mg.Disconect(n)]])

        #róg
        if total == 2 and loops == 0:
            return([[1,mg.Short(n)],[1,mg.Disconect(n)]])
        
        #róg z pętelką
        if total == 3 and loops == 1:
            return([[1,mg.Short(n)]])

        #gałąź
        if total == 1 and loops == 0:
            return([[3,mg.Disconect(n)]])

        #gałąź z pętelką
        if total == 2 and loops == 1:
            return([[2,mg.Disconect(n)]])

    #Tu dochodzimy jeśli nie da się uprościć
    #zwracam False, ale mógłbym: [-1,mg], -1 byłoby kodem po którym main wiedziałby, że nie nastąpiła żadna redukcja.
    return(False)

#main function
def Evaluate(x):
    #rozkłada graf na czynniki pierwsze
    #wejście: MójGraf, wyjście: [[liczba1,Graf1],...]

    #pomysł - nazwa work skojarzyła mi się z omawianymi na ćwiczeniach "workers"
    #możliwe że dałoby się podzielić work w połowie, jeśli byłoby wystarczająco długie
    #i wysłać do dwóch rdzeni. Albo trzech. etc... 
    #Na razie jednak nie spotkałem się ze spadkami wydajności na rozsądnych rozmiarach testów.

    work = [[1,x]]
    done = []

    while len(work)>0:
        cp = work.pop() #current pair
        cg = cp[1] #current graph
        sg = Simplify(cg) #simplified graphs (list of lists)
        if sg is False: #Jeśli nie dało się uprościć:
            AddPairs(cp, done)
        else: #Jeśli dało się uprościć:
            for pair in sg:
                multi_pair = [cp[0]*pair[0],pair[1]]
                AddPairs(multi_pair, work)
    return(done)


#MAIN
def Main(instruction):
    #Evaluate dla ludzi posługujących się istrukcjami zamiast klasą MyGraph.
    #input: [[w1,w2],...] (type: list)
    x = MyGraph(instruction)
    done = Evaluate(x)
    really_done = done.copy()
    for pair in really_done:
        pair[1] = pair[1].SmoothEdges()
    return(really_done)

ipt = str(input("Podaj listę dwuelementowych list, opisującą krawędzie grafu: \n")).strip()
#zainspirowany filmem o SQL injections napisałem:
#try: exec("instruction = "+ipt)
#wykonywanie kodu wpisanego przez użytkownika może i jest niezbyt bezpiecznym rozwiązaniem... 
#ale jednolinijkowym.
#slice nie działał ze względu na zagnieżdżone listy.
#chciałem zatem:
"""
def StrToList(ipt):
    ipt = ipt.strip()
    instruction = []
    pair = []
    t = ""
    for s in ipt:
        if s.isdigit():
            t += s
            last = "digit"
        if s == ",":
            if last ==  "digit":
                pair.append(int(t))
                t = ""
        if s == "]":
            if len(pair)>0:
                pair.append(int(t))
                t = ''
                instruction.append(pair)
                pair = []
                last = "bracket"
            else:
                return(instruction)
    print("Niepoprawna lista")
    return
"""
#ale poddałem się, nie chcąc ryzykować utraty funkcjonalności np dla list [[1,2,]] etc.
#pozwoliłem sobie zaimportować ast:

instruction = ast.literal_eval(ipt)

really_done = Main(instruction)
print(really_done)


#Rysowanie, przydatne do debugowania. 
#jeśli zainstalujemy 2.6 networkx'a (pre release), połączenia [a,a]
#niestety ta biblioteka nie potrafi rysować dwóch "takich samych" krawędzi (a raczej rysuje je na sobie)
#graphviz mi nie działał.
#Co prawda grafy są nieskierowane, ale strzałki pomagają zobaczyć którą krawędź rysujemy.
debug = True #zostawiłem włączonego, dla wygody sprawdzającego.
if debug:
    i = input("Czy chcesz zobaczyć któryś z grafów? Podaj jego indeks. [int/'nie'] \n")
    if i == "nie": exit()
    else:
        try:
            i = int(i)
            nx.draw(MyGraph(really_done[i][1]).G,with_labels=True)
            print("Pamiętaj że niektóre wyświetlone krawędzie mogą być podwójne.")
            plt.show()
        except ValueError:
            print("Podany indeks był niewłaściwy.")
        except IndexError:
            print("Podany indeks nie należy do listy. Pamiętaj, że informatycy liczą od zera.")

"""
Końcowe przemyślenia:
Program działa, choć nie idealnie.
Brakuje mi testów, a odręcznie można wykonywać tylko proste.
Dla testu drugiego z instrukcji otrzymuję 6 grafów o≡o, które nie są redukowalne,
a ich wartość to 6 każdy, zatem 6*6+14790=14826 i wszystko się zgadza.
Wynika to pewnie z innych kolejności algorytmów.

Możnaby wykrywać rozłączne grafy i rozpisać je jako iloczyn/potęgę.
Możnaby pomyśleć nad równoległym obliczaniem.
Żałuję, że nie udało mi się zainstalować biblioteki Graphviz, która pozwala rysować 
podwójne połączenia między wierzchołkami. NX nie posiada na chwilę obecną takiej funkcji (a w 2.5 nie rysuje nawet loop'ów)


Starałem się wyłapać najczęstsze błędy ale pewnie jakieś mi się omsknęły
Finalnie jestem zadowolony z efektu, sam projekt był bardzo ciekawy i 
w końcu zmotywował mnie do korzystania z klas.
"""
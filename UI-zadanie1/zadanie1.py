from hash_zoznam import *
import time

#priority q na ukladanie nerozvinutych uzlov
class Priority:
    def __init__(self):
        self.queue = []
        self.najmensi = 100
        self.deleted = []
    #vloz nerozvinuty uzol
    def insert(self, uzol):
        for i in range(len(self.deleted)):
            if porovnanie(self.deleted[i], uzol):
                return
        self.queue.append(uzol)
        if uzol.ohodnotenie < self.najmensi:
            self.najmensi = uzol.ohodnotenie

    #vymazanie nerozvinuteho uzla s najmensim ohodnotenim
    def delete(self):
        maly = 0
        if len(self.queue) == 0:
            print("chyba")
        else:
            for i in range(len(self.queue)):
                if self.queue[i].ohodnotenie <= self.queue[maly].ohodnotenie:
                    maly = i
            vysledok = self.queue[maly]
            del self.queue[maly]
            self.najmensi = 100
            if len(self.queue) != 0:
                for i in range(len(self.queue)):
                    if self.queue[i].ohodnotenie <= self.najmensi:
                        self.najmensi = self.queue[i].ohodnotenie
            self.deleted.append(vysledok)
            return vysledok

class Uzol:
    def __init__(self, parent):
        global x
        global y
        self.plocha = prazdne(x, y)
        self.ohodnotenie = 0
        self.children = []
        self.parent = parent

    #skopirovanie plochy
    def vytvor_plochu(self, plocha):
        for i in range(len(plocha)):
            for j in range(len(plocha[i])):
                self.plocha[i][j] = plocha[i][j]

    #najdi suradnice M
    def findM(self):
        for i in range(len(self.plocha)):
            for j in range(len(self.plocha[i])):
                if type(self.plocha[i][j]) is str:
                    return (i, j)

##    #vypocitanie ohodnotenia na zaklade poctu cisel, ktore nie su na svojom mieste
##    def heuristika(self, ciel, pocet):
##        for i in range (len(self.plocha)):
##            for j in range(len(self.plocha[i])):
##                if self.plocha[i][j] != ciel[i][j]:
##                    self.ohodnotenie += 1


    #vypocitanie ohodnotenia na zaklade vzdialenosti cisel od ciela
    def heuristika(self, ciel, pocet):
        #vzdialenost cisel
        for i in range(1, pocet):
            i1 = 0
            j1 = 0
            i2 = 0
            j2 = 0
            x = self.plocha[i1][j1]
            while x != i:
                j1 += 1
                if j1 > len(self.plocha[0]) -1:
                    j1 = 0
                    i1 += 1
                x = self.plocha[i1][j1]
            x = ciel[i2][j2]
            while x != i:
                j2 += 1
                if j2 > len(self.plocha[0]) -1:
                    j2 = 0
                    i2 += 1
                x = ciel[i2][j2]
            self.ohodnotenie += abs(i1 - i2)
            self.ohodnotenie += abs(j1 - j2)

    #vytvorenie vsetkych deti pre uzol
    def vytvor_deti(self, ciel, pocet, tabulka):
        global counter
        mi = self.findM()[0]
        mj = self.findM()[1]

        vytvor_vlavo(self, mi, mj)
        vytvor_vpravo(self, mi, mj)
        vytvor_hore(self, mi, mj)
        vytvor_dole(self, mi, mj)
        for i in range(len(self.children)):
            if self.parent != None:
                if porovnanie(self.children[i], self.parent):
                    self.children.pop(i)
                    break
        for i in range(len(self.children)):
            if HZsearch(uprav_value(self.children[i]), tabulka):
                self.children.pop(i)
                break
        #ohodnotenie deti uzla
        for i in range(len(self.children)):
            self.children[i].heuristika(ciel, pocet)
            counter += 1

            
    def vytvor_strom(self, ciel, root, pocet, uzly):
        global tabulka
        uzol = self
        #ak je ohodnotenie 0, ukoncenie vytvarania (algoritmus nasiel ciel)
        while True:
            if uzol.ohodnotenie == 0:
                return uzol
                break

            #ak uzol este nema deti, vytvor
            if len(uzol.children) == 0:
                uzol.vytvor_deti(ciel, pocet, tabulka)
                HZinsert(uprav_value(uzol), tabulka)
                #HZvypis(tabulka)
            

            #ak uzol ma deti, najdi dieta s najlepsim ohodnotenim
            if len(uzol.children) > 0:
                najmensi = uzol.children[0]
                for i in range(len(uzol.children)):
                    if najmensi.ohodnotenie > uzol.children[i].ohodnotenie:
                        najmensi = uzol.children[i]
                #ulozenie nerozvinutych uzlov
                for i in range(len(uzol.children)):
                    if najmensi != uzol.children[i]:
                        uzly.insert(uzol.children[i])

    ##            print('---------------------------------------------')
    ##            print('V PARENT V')
    ##            for i in range(len(uzol.plocha)):
    ##                print(uzol.plocha[i])
    ##            print(uzol.ohodnotenie)
    ##            print('V CHILDREN V')
    ##            for j in range(len(uzol.children)):
    ##                for i in range(len(uzol.children[j].plocha)):
    ##                    print(uzol.children[j].plocha[i])
    ##                print(uzol.children[j].ohodnotenie)
    ##                print('=====================')

                if najmensi.ohodnotenie > uzly.najmensi:
                    novy = uzly.delete()
                    uzol = novy
                else:
                    uzol = najmensi
            else:
                novy = uzly.delete()
                uzol = novy


#porovnanie dvoch uzlov    
def porovnanie(a, b):
    for i in range(len(a.plocha)):
        for j in range(len(a.plocha[i])):
            if a.plocha[i][j] != b.plocha[i][j]:
                return False
    return True

#vytvorenie dietata posunom M hore     
def vytvor_hore(parent, i, j):
    if i-1 >= 0:
        new = Uzol(parent)
        new.vytvor_plochu(parent.plocha)
        new.plocha[i][j] = new.plocha[i-1][j]
        new.plocha[i-1][j] = 'm'
        parent.children.append(new)

#vytvorenie dietata posunom M dole  
def vytvor_dole(parent, i, j):
    if i+1 < len(parent.plocha):
        new = Uzol(parent)
        new.vytvor_plochu(parent.plocha)
        new.plocha[i][j] = new.plocha[i+1][j]
        new.plocha[i+1][j] = 'm'
        parent.children.append(new)

#vytvorenie dietata posunom M dolava  
def vytvor_vlavo(parent, i, j):
    if j-1 >= 0:
        new = Uzol(parent)
        new.vytvor_plochu(parent.plocha)
        new.plocha[i][j] = new.plocha[i][j-1]
        new.plocha[i][j-1] = 'm'
        parent.children.append(new)

#vytvorenie dietata posunom M doprava 
def vytvor_vpravo(parent, i, j):
    if j+1 < len(parent.plocha[0]):
        new = Uzol(parent)
        new.vytvor_plochu(parent.plocha)
        new.plocha[i][j] = new.plocha[i][j+1]
        new.plocha[i][j+1] = 'm'
        parent.children.append(new)

#vypis riesenia
def vypis_cesty(uzol):
    global cesta
    last_M = None
    M = None
    cesta2 = []
    while uzol != None:
        cesta += 1
##        for i in range(len(uzol.plocha)):
##            print(uzol.plocha[i])
##        print("Ohodnotenie:" + str(uzol.ohodnotenie))
##        print('=====================')
        M = uzol.findM()
        if last_M == None:
            last_M = M
        else:
            if M[0] - last_M[0] > 0:
                cesta2.append(4)
            elif M[0] - last_M[0] < 0:
                cesta2.append(3)
            else:
                if M[1] - last_M[1] > 0:
                    cesta2.append(2)
                elif M[1] - last_M[1] < 0:
                    cesta2.append(1)
            last_M = M
        uzol = uzol.parent
    j = 1
    for i in range(len(cesta2) - 1, -1, -1):
        print(str(j) + ".")
        if cesta2[i] == 1:
            print('Doprava')
        elif cesta2[i] == 2:
            print('Dolava')
        elif cesta2[i] == 3:
            print('Dole')
        elif cesta2[i] == 4:
            print('Hore')
        j += 1

#upravenie plochy na hodnotu, ktora sa moze ulozit do hash tabulky
def uprav_value(uzol):
    value = []
    for i in range(len(uzol.plocha)):
        for j in range(len(uzol.plocha[i])):
            if uzol.plocha[i][j] == 'm':
                value.append(0)
            else:
                value.append(uzol.plocha[i][j])
    return value

#vytvorenie prazdnej plochy v uzle
def prazdne(x, y):
    pole = []
    for i in range(x):
        riadok = []
        for j in range(y):
            riadok.append(0)
        pole.append(riadok)
    return pole

while True:
    #pouzivatel zada pocet riadkov a stlpcov
    x = int(input('Zadaj pocet riadkov (zadaj q pre ukoncenie): '))
    if x == 'q':
        break
    y = int(input('Zadaj pocet stlpcov: '))

    #pouzivatel zada postupnost
    
    print('Na mieste prazdneho policka zadaj 0')
    priklad = []
    #ulozenie postupnosti do pola priklad
    for i in range(x):
        riadok = []
        for j in range(y):
            riadok.append(int(input('Zadaj hodnotu na mieste [' + str(i) +'][' + str(j) + ']')))
        priklad.append(riadok)

    for i in range (x):
        for j in range(y):
            if priklad[i][j] == 0:
                priklad[i][j] = 'm'
    start = time.time()
    ciel = []

    for i in range(x):
        riadok = []
        for j in range(y):
            riadok.append(j + i*y)
        ciel.append(riadok)
    ciel[0][0] = 'm'

    pocet = x * y

    counter = 1
    cesta = 0
    uzly = Priority()

    velkost = 1001
    tabulka = [None] * velkost
    pocet1 = 0

    root = Uzol(None)
    root.vytvor_plochu(priklad)
    uprav_value(root)
    print('V ROOT V')
    for i in range(len(root.plocha)):
        print(root.plocha[i])
    root.heuristika(ciel, pocet)
    print(root.ohodnotenie)

    uzol = root.vytvor_strom(ciel, root, pocet, uzly)
    end = time.time()
    print("---------------------postupnosť krokov od zaciatku k cielu----------------------")
    print('=====================')
    vypis_cesty(uzol)
    print("Pocet nodov: " + str(counter))
    print("Dlzka cesty (Hlbka): " + str(cesta))
    print("Cas na vytvorenie: " + str(end - start))

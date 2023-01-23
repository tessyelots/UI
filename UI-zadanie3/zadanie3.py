import matplotlib.pyplot as plt
import numpy as np
import random
import math
import time
from collections import deque
from heapq import heappop, heappush, heapreplace

#trieda prevzata z internetu, sluzi na ukladanie susedov v poradi od najvzdialenejsieho po najblizsieho
class PriorityQueue:
    def __init__(self):
        self._elements = []

    def enqueue_with_priority(self, priority, value):
        try:
            heappush(self._elements, (-priority, value))
        except TypeError:
            pass

    def dequeue(self):
        heappop(self._elements)

    def replace(self, priority, value):
        try:
            heapreplace(self._elements, (-priority, value))
        except TypeError:
            pass

#trieda, ktora reprezentuje jeden bod na ploche, ma suradnice a farbu
class Node:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    #funkcia na vlozenie bodu do spravneho stvorceka
    def insert(self, root, expected_color, k):
        i = (self.y - 5000) // -250
        j = abs(((self.x - 5000) // -250) - 39)
        root[i][j].append(self)
        if self.color == '':
            self.classify(root, i, j, k, 0, None)
            if self.color == expected_color:
                stats()

    #funkcia, ktora skontroluje vsetky body vo stvorci a upravi zoznam najblizsich susedov
    def check_box(self, box, k, closest):
        for l in range(len(box)):
            if box[l] != self:
                if len(closest._elements) < k:
                    closest.enqueue_with_priority(self.vzdialenost(box[l]), box[l])
                else:
                    if self.vzdialenost(box[l]) < self.vzdialenost(closest._elements[0][1]):
                        closest.replace(self.vzdialenost(box[l]), box[l])
        return closest


    #funkcia, ktora postupne kontroluje stvorceky v poradi od stvorca, v ktorom sa bod, ktory sa prave klasifikuje
    #nachadza smerom k okraju az kym nenajde k-pocet susedov
    def classify(self, root, i, j, k, level, closest):
        koniec = False
        #vytvorenie zoznamu najblizsich susedov a skontrolovanie stvorca, v ktorom sa bod nachadza
        if closest == None:
            closest = PriorityQueue()
            box = root[i][j]
            closest = self.check_box(box, k, closest)

        #skontrolovanie susednych stvorcov 
        if level == 0:
            if i - 1 >= 0:
                try:
                    box = root[i - 1][j]
                    closest = self.check_box(box, k, closest)
                except IndexError:
                    pass
                try:
                    box = root[i - 1][j + 1]
                    closest = self.check_box(box, k, closest)
                except IndexError:
                    pass
                if j - 1 >= 0:
                    try:
                        box = root[i - 1][j - 1]
                        closest = self.check_box(box, k, closest)
                    except IndexError:
                        pass
            if j - 1 >= 0:
                try:
                    box = root[i][j - 1]
                    closest = self.check_box(box, k, closest)
                except IndexError:
                    pass
                try:
                    box = root[i + 1][j - 1]
                    closest = self.check_box(box, k, closest)
                except IndexError:
                    pass
            try:
                box = root[i][j + 1]
                closest = self.check_box(box, k, closest)
            except IndexError:
                pass
            try:
                box = root[i + 1][j]
                closest = self.check_box(box, k, closest)
            except IndexError:
                pass
            try:
                box = root[i + 1][j + 1]
                closest = self.check_box(box, k, closest)
            except IndexError:
                pass
            
            if len(closest._elements) < k:
                self.classify(root, i, j, k, level + 2, closest)
            else:
                koniec = True

        #v pripade, ze pocet susedov je < k skontrolujeme dalsi level stvorcekov dookola
        elif level > 0 and len(closest._elements) < k:
            for l in range(level + 1):
                if i - level >= 0:
                    try:
                        box = root[i - level][j + l]
                        closest = self.check_box(box, k, closest)
                    except IndexError:
                        pass
                    if j - l >= 0:
                        try:
                            box = root[i - level][j - l]
                            closest = self.check_box(box, k, closest)
                        except IndexError:
                            pass
                if j - level >= 0:
                    try:
                        box = root[i + l][j - level]
                        closest = self.check_box(box, k, closest)
                    except IndexError:
                        pass
                    if i - l >= 0:
                        try:
                            box = root[i - l][j - level]
                            closest = self.check_box(box, k, closest)
                        except IndexError:
                            pass
                if i - l >= 0:
                    try:
                        box = root[i - l][j + level]
                        closest = self.check_box(box, k, closest)
                    except IndexError:
                        pass
                if j - l >= 0:
                    try:
                        box = root[i + level][j - l]
                        closest = self.check_box(box, k, closest)
                    except IndexError:
                        pass
                try:
                    box = root[i + l][j + level]
                    closest = self.check_box(box, k, closest)
                except IndexError:
                    pass
                try:
                    box = root[i + level][j + l]
                    closest = self.check_box(box, k, closest)
                except IndexError:
                    pass
                
            if len(closest._elements) < k:
                self.classify(root, i, j, k, level + 1, closest)
            else:
                koniec = True

        #ak je pocet susedov rovny k, vyberieme farbu
        if koniec:
            self.color = vyber_z_farieb(closest._elements)
            
    #funkcia na vypocitanie vzdialenosti medzi dvoma bodmi
    def vzdialenost(self, node):
        a = abs(self.x - node.x)
        b = abs(self.y - node.y)
        c = math.sqrt(a**2 + b**2)
        return c

#funkcia, ktora vrati farbu, ktora sa vyskytuje v zozname najviac
def vyber_z_farieb(listik):
    rs = 0
    gs = 0
    bs = 0
    ms = 0
    for i in range(len(listik)):
        if listik[i][1].color == 'rs':
            rs += 1
        elif listik[i][1].color == 'gs':
            gs += 1
        elif listik[i][1].color == 'bs':
            bs += 1
        elif listik[i][1].color == 'ms':
            ms += 1
    if (rs >= gs and rs >= bs) and rs >= ms:
        return 'rs'
    elif (gs >= rs and gs >= bs) and gs >= ms:
        return 'gs'
    elif (bs >= gs and bs >= rs) and bs >= ms:
        return 'bs'
    elif (ms >= gs and ms >= bs) and ms >= rs:
        return 'ms'

#funkcia na vypis poli, ktore reprezentuju plochu rozdelenu na stvorceky
def vypis(root):
    for i in range(len(root)):
        print(root[i])

#prejdenie vsetkych poli, ktore reprezentuju plochu a nakreslenie bodov do grafickej reprezentacie
def nakresli(root):
    for i in range(len(root)):
        for j in range(len(root[i])):
            for k in range(len(root[i][j])):
                node = root[i][j][k]
                plt.plot([node.x], [node.y], node.color, markersize=4)

#fukcia, ktora pocita spravne klasifikovanie
def stats():
    global pocet
    pocet += 1

#funkcia, ktora vytvori polia pre stvorceky, vytvori zaciatocne body a v loope vytvara 40 000 bodov, pri ktorych
#vola funkciu classify
def make_all(k):
    global pocet
    start = time.time()
    plt.figure(k)
    plt.axis([-4999, 5000, -4999, 5000])

    root = []
    for i in range(40):
        root.append([])
        for j in range(40):
            root[i].append([])

    
    new = Node(-2000, -1400, 'rs')
    new.insert(root, 'rs', k)
    new = Node(2000, -1400, 'gs')
    new.insert(root, 'gs', k)
    new = Node(-2000, 1400, 'bs')
    new.insert(root, 'bs', k)
    new = Node(2000, 1400, 'ms')
    new.insert(root, 'ms', k)
    new = Node(-2500, -3400, 'rs')
    new.insert(root, 'rs', k)
    new = Node(2500, -3400, 'gs')
    new.insert(root, 'gs', k)
    new = Node(-2500, 3400, 'bs')
    new.insert(root, 'bs', k)
    new = Node(2500, 3400, 'ms')
    new.insert(root, 'ms', k)
    new = Node(-1800, -2400, 'rs')
    new.insert(root, 'rs', k)
    new = Node(1800, -2400, 'gs')
    new.insert(root, 'gs', k)
    new = Node(-1800, 2400, 'bs')
    new.insert(root, 'bs', k)
    new = Node(1800, 2400, 'ms')
    new.insert(root, 'ms', k)
    new = Node(-4100, -3000, 'rs')
    new.insert(root, 'rs', k)
    new = Node(4100, -3000, 'gs')
    new.insert(root, 'gs', k)
    new = Node(-4100, 3000, 'bs')
    new.insert(root, 'bs', k)
    new = Node(4100, 3000, 'ms')
    new.insert(root, 'ms', k)
    new = Node(-4500, -4400, 'rs')
    new.insert(root, 'rs', k)
    new = Node(4500, -4400, 'gs')
    new.insert(root, 'gs', k)
    new = Node(-4500, 4400, 'bs')
    new.insert(root, 'bs', k)
    new = Node(4500, 4400, 'ms')
    new.insert(root, 'ms', k)

    for i in range(10000):
        if random.randint(1, 100) == 1:
            new = Node(random.randint(-4999, 5000), random.randint(-4999, 5000), '')
            new.insert(root, 'rs', k)
        else:
            new = Node(random.randint(-4999, 500), random.randint(-4999, 500), '')
            new.insert(root, 'rs', k)
        if random.randint(1, 100) == 1:
            new = Node(random.randint(-4999, 5000), random.randint(-4999, 5000), '')
            new.insert(root, 'gs', k)
        else:
            new = Node(random.randint(-500, 5000), random.randint(-4999, 500), '')
            new.insert(root, 'gs', k)
        if random.randint(1, 100) == 1:
            new = Node(random.randint(-4999, 5000), random.randint(-4999, 5000), '')
            new.insert(root, 'bs', k)
        else:
            new = Node(random.randint(-4999, 500), random.randint(-500, 5000), '')
            new.insert(root, 'bs', k)
        if random.randint(1, 100) == 1:
            new = Node(random.randint(-4999, 5000), random.randint(-4999, 5000), '')
            new.insert(root, 'ms', k)
        else:
            new = Node(random.randint(-500, 5000), random.randint(-500, 5000), '')
            new.insert(root, 'ms', k)

    nakresli(root)
    end = time.time()

    print("k = " + str(k))
    print("Uspesnost: " + str(int((pocet / 40000) * 100)) + "%")
    print("Time: " + str(end - start))
    print("--------------------------------------")
    
    #vypis(root)
    pocet = 0

pocet = 0
make_all(1)
make_all(3)
make_all(7)
make_all(15)
print("Genenerujem graficke zobrazenie...")
plt.show()



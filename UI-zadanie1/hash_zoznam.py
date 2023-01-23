import random

velkost = 1001
tabulka = [None] * velkost
pocet = 0

class Zoznam:
    def __init__(self, data, dalsi):
        self.data = data
        self.dalsi = dalsi

def Poly(vstup):
    c = 31
    vystup = 0
    for i in range(len(vstup)):
        vystup += int(vstup[i]) * c**i
    return vystup

def Hash(vstup):
    global velkost
    key = vstup % velkost
    return key

def velkostTabulky(prvky):
    global velkost
    if prvky >= (velkost - 1) * 2:
        #HZvypis()
        velkost += 1000
        #print(velkost)
        uprava_prvkov(velkost)

def uprava_prvkov(velkost):
    global pocet
    global tabulka
    pomoc = [None] * velkost
    for i in tabulka:
        if i != None:
            ptr = i
            while ptr != None:
                newPlace = Hash(Poly(ptr.data))
                if pomoc[newPlace] is None:
                    pomoc[newPlace] = Zoznam(ptr.data, None)
                    break
                else:
                    ptr1 = pomoc[newPlace]
                    while True:
                        if ptr1.dalsi is None:
                            ptr1.dalsi = Zoznam(ptr.data, None)
                            break
                        else:
                            ptr1 = ptr1.dalsi
                    ptr = ptr.dalsi
    tabulka = pomoc

def HZsearch(string, tabulka):
    pozicia = Hash(Poly(string))
    ptr = tabulka[pozicia]
    while True:
        if ptr != None:
            if ptr.data == string:
                #print("Slovo " + string + " sa nachadza na pozicii " + str(pozicia))
                return True
            else:
                ptr = ptr.dalsi
        else:
            #print("Slovo " + string + " sa v tabulke nenachadza")
            return False

def HZinsert(string, tabulka):
    global pocet
    cislo = Poly(string)
    pozicia = Hash(cislo)
    if tabulka[pozicia] is None:
        tabulka[pozicia] = Zoznam(string, None)
    else:
        ptr = tabulka[pozicia]
        while True:
            if ptr.dalsi is None:
                ptr.dalsi = Zoznam(string, None)
                pocet += 1
                #velkostTabulky(pocet)
                break
            else:
                ptr = ptr.dalsi

def HZdelete(string):
    global tabulka
    pozicia = Hash(Poly(string))
    ptr = tabulka[pozicia]
    while True:
        if ptr != None:
            if ptr.data == string:
                if ptr == tabulka[pozicia]:
                    tabulka[pozicia] = ptr.dalsi
                else:
                    parent.dalsi = ptr.dalsi
            parent = ptr
            ptr = ptr.dalsi
        else:
            break
                
x = []

def HZvypis(tabulka):
    for i in range (velkost):
        if tabulka[i] != None:
            ptr = tabulka[i]
            print(str(i) + ".-----------------")
            while True:
                if ptr.dalsi is None:
                    print(ptr.data)
                    break
                else:
                    print(ptr.data)
                    x.append(ptr.data)
                    ptr = ptr.dalsi
    return x

def zoznam_test(pocet_testov):
    abeceda = "qwertyuiopasdfghjklzxcvbnm1234567890"
    slovo = ""
    for i in range(pocet_testov):
        for j in range(random.randint(3, 6)):
            slovo += random.choice(abeceda)
        HZinsert(slovo)
        slovo = ""
    HZvypis()

#zoznam_test(1000)

##znak = ""
##while True:
##    znak = input()
##    if znak == "i":
##        HZinsert(input())
##    elif znak == "s":
##        HZsearch(input())
##    elif znak == "v":
##        HZvypis()
##    elif znak == "d":
##        HZdelete(input())

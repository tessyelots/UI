import random
import math


#trieda jedinca s listom adries a hodnotou fitnes
class Jedinec:
    def __init__(self, hodnoty):
        self.hodnoty = hodnoty
        self.fitnes = 1

    def copy_hodnoty(self):
        new = []
        for i in range(len(self.hodnoty)):
            new.append(self.hodnoty[i])
        return new


#trieda pole, reprezentuje mriezku s pokladmi
class Pole:
    def __init__(self, x, y, pocet_pokladov):
        self.plocha = vytvor_plochu(x, y)
        self.pos = [(x)//2, y-1]
        self.pridaj_poklady(pocet_pokladov, x, y, self.pos)
        

    def pridaj_poklady(self, pocet_pokladov, x, y, start_pos):
        pridane = 0
        list_sur = []
        while pridane != pocet_pokladov:
            x_sur = random.randint(0, x-1)
            y_sur = random.randint(0, y-1)
            suradnice = [x_sur, y_sur]
            if not (suradnice in list_sur) and (suradnice != start_pos):
                list_sur.append(suradnice)
                pridane += 1

        for i in range(len(list_sur)):
            self.plocha[list_sur[i][1]][list_sur[i][0]] = 1

    def copy_plocha(self, plocha):
        for i in range(len(self.plocha)):
            for j in range(len(self.plocha[i])):
                self.plocha[i][j] = plocha[i][j]

#funkcia na vytvorenie prazdnej plochy
def vytvor_plochu(x, y):
    plocha = []
    for i in range(y):
        riadok = []
        for j in range(x):
            riadok.append(0)
        plocha.append(riadok)

    return plocha

#funkcia na vytvorenie prazdneho jedinca, vsetky adresy su 00000000
def vytvor_prazdny_jedinec():
    listik = []
    for i in range(64):
        listik.append('00000000')
    return listik

#vytvorenie prvej generacie, kazdy jedinec dostane random hodnoty do prvych 16 adries
def vytvor_prvu_gen(pocet):
    gen = []
    for i in range(pocet):
        jed = Jedinec(vytvor_prazdny_jedinec())
        for j in range(16):
            num = random.randint(0, 255)
            num = bin(num).zfill(8)
            if len(num) == 9:
                num = num.replace('0b', '0')
            elif len(num) == 10:
                num = num.replace('0b', '')
            elif len(num) == 8:
                num = num.replace('b', '0')
            jed.hodnoty[j] = num
        gen.append(jed)
    return gen

#funkcia inkrementacie v jedincovi
def inc(adresa, hodnoty):
    adresa = int(adresa, 2)
    if hodnoty[adresa] == '11111111':
        hodnoty[adresa] = '00000000'
    else:
        hodnoty[adresa] = int(hodnoty[adresa], 2) + 1
        hodnoty[adresa] = bin(hodnoty[adresa]).zfill(8)
        if len(hodnoty[adresa]) == 9:
            hodnoty[adresa] = hodnoty[adresa].replace('0b', '0')
        elif len(hodnoty[adresa]) == 10:
            hodnoty[adresa] = hodnoty[adresa].replace('0b', '')
        elif len(hodnoty[adresa]) == 8:
            hodnoty[adresa] = hodnoty[adresa].replace('b', '0')
    return hodnoty

#funkcia dekrementacie v jedincovi
def sub(adresa, hodnoty):
    adresa = int(adresa, 2)
    if hodnoty[adresa] == '00000000':
        hodnoty[adresa] = '11111111'
    else:
        hodnoty[adresa] = int(hodnoty[adresa], 2) - 1
        hodnoty[adresa] = bin(hodnoty[adresa]).zfill(8)
        if len(hodnoty[adresa]) == 9:
            hodnoty[adresa] = hodnoty[adresa].replace('0b', '0')
        elif len(hodnoty[adresa]) == 10:
            hodnoty[adresa] = hodnoty[adresa].replace('0b', '')
        elif len(hodnoty[adresa]) == 8:
            hodnoty[adresa] = hodnoty[adresa].replace('b', '0')
    return hodnoty

#funkcia vypisu v jedincovi
def vypis(adresa, hodnoty):
    count = 0
    adresa = int(adresa, 2)
    for i in range(len(hodnoty[adresa])):
        if hodnoty[adresa][i] == '1':
            count += 1

    if count < 3:
        return 'H'
    elif count > 2 and count < 5:
        return 'D'
    elif count > 4 and count < 7:
        return 'P'
    else:
        return 'L'

#funkcia skoku v jedincovi
def posun(pohyb, pos):
    if pohyb == 'H':
        pos[1] -= 1
    elif pohyb == 'D':
        pos[1] += 1
    elif pohyb == 'P':
        pos[0] += 1
    elif pohyb == 'L':
        pos[0] -= 1
    return pos

#funkcia, ktora vyhodnoti jedinca (prejde po ploche a jedincovi da fitnes)
def vyhodnot_jedinca(hodnoty, pole, end):
    fitnes = 1
    i = 0
    x = 0
    while i < len(hodnoty) and x < 500:
        if hodnoty[i][0] + hodnoty[i][1] == '00':
            adresa = hodnoty[i][2:8]
            hodnoty = inc(adresa, hodnoty)
        elif hodnoty[i][0] + hodnoty[i][1] == '01':
            adresa = hodnoty[i][2:8]
            hodnoty = sub(adresa, hodnoty)
        elif hodnoty[i][0] + hodnoty[i][1] == '11':
            adresa = hodnoty[i][2:8]
            if end:
                print(vypis(adresa, hodnoty))
            pole.pos = posun(vypis(adresa, hodnoty), pole.pos)
            if (pole.pos[0] < 0 or pole.pos[0] > 6) or (pole.pos[1] < 0 or pole.pos[1] > 6):
                return fitnes
            elif pole.plocha[pole.pos[1]][pole.pos[0]] == 1:
                pole.plocha[pole.pos[1]][pole.pos[0]] = 0
                fitnes += 1
            if end and fitnes == 6:
                break
        elif hodnoty[i][0] + hodnoty[i][1] == '10':
            adresa = hodnoty[i][2:8]
            adresa = int(adresa, 2)
            i = adresa - 1
            x += 1
            
        i += 1
        if i == len(hodnoty):
            i = 0

    return fitnes

#selektovanie rodicov z kazdej generacie, typ ruleta
def ruleta(gen):
    listik = []
    parents = []
    for i in range(len(gen)):
        for j in range(gen[i].fitnes**2):
            listik.append(i)

    for i in range(int(math.sqrt(len(gen)))):
        parents.append(gen[listik[random.randint(0, len(listik) - 1)]])

    return parents

#krizenie jedincov, dieta nahodne dedi celu adresu od jedneho z rodicov (gen = adresa)
def krizenie1(parents):
    new = []
    for i in range(len(parents)):
        new.append(parents[i])
    for i in range(len(parents)):
        for j in range(len(parents)):
            if i != j:
                hodnoty = []
                for k in range(64):
                    x = random.randint(0, 1)
                    if x == 0:
                        hodnoty.append(parents[i].hodnoty[k])
                    else:
                        hodnoty.append(parents[j].hodnoty[k])
                jed = Jedinec(hodnoty)
                new.append(jed)
    return new

#krizenie jedincov, dieta nahodne dedi 1 alebo 0 v adrese od jedneho z rodicov (gen = 1 alebo 0)
def krizenie2(parents):
    new = []
    for i in range(len(parents)):
        new.append(parents[i])
    for i in range(len(parents)):
        for j in range(len(parents)):
            if i != j:
                hodnoty = []
                for k in range(64):
                    gen = ""
                    for l in range(8):
                        x = random.randint(0, 1)
                        if x == 0:
                            gen += parents[i].hodnoty[k][l]
                        else:
                            gen += parents[j].hodnoty[k][l]
                    hodnoty.append(gen)
                jed = Jedinec(hodnoty)
                new.append(jed)
    return new

#funkcia, ktora zmutuje vytvorenu generaciu
def mutacia(gen):
    for i in range(len(gen)):
        x = random.randint(0, 1)
        if x == 0:
            y = random.randint(0, 63)
            z = random.randint(0, 7)
            if gen[i].hodnoty[y][z] == '0':
                temp = list(gen[i].hodnoty[y])
                temp[z] = '1'
                gen[i].hodnoty[y] = "".join(temp)
            elif gen[i].hodnoty[y][z] == '1':
                temp = list(gen[i].hodnoty[y])
                temp[z] = '0'
                gen[i].hodnoty[y] = "".join(temp)
    return gen

#input od uzivatela
def get_pocet():
    pocet = int(input("Zadaj pocet jedincov v generacii (odmocnina tohto cisla musi byt cele cislo)"))
    return pocet

#loop na ziskanie inputov
while True:
    pocet_jedincov = get_pocet()
    print("krizenie1 -z rodicov sa vyberaju cele adresy")
    print("krizenie2 -z rodicov sa vyberaju miesta v adresach (1 a 0)")
    krizenie = int(input("Zadaj 1 ak chces krizenie1, 2 ak chces krizenie2 "))
    if (math.sqrt(pocet_jedincov) % 1) == 0 and (krizenie == 1 or krizenie == 2):
        break


#mainloop
pole = Pole(7, 7, 5)
print("PLOCHA S POKLADMI")
for i in range(len(pole.plocha)):
    print(pole.plocha[i])
print("------------------------------------------")
gen = vytvor_prvu_gen(pocet_jedincov)
stop = False
print("Program pracuje...")
q = 0
while not stop:
    j = 0
    while not stop:
    #for j in range(1000):
        if stop:
            break
        for i in range(len(gen)):
            copy = gen[i].copy_hodnoty()
            copy_pole = Pole(7, 7, 5)
            copy_pole.copy_plocha(pole.plocha)
            gen[i].fitnes = vyhodnot_jedinca(copy, copy_pole, False)

            if gen[i].fitnes == 6:
                end = gen[i]
                stop = True
                break
            #if j % 100 == 0:
                #print(gen[i].fitnes)

        if krizenie == 2:
            gen = krizenie2(ruleta(gen))
        elif krizenie == 1:
            gen = krizenie1(ruleta(gen))
        gen = mutacia(gen)
        q += 1
        if q % 100 == 0:
            print("uz mame " + str(q) + " generacii")
    if not stop:
        x = input("stlac ENTER ak chces vytvorit dalsich 1000 generacii")
        if x != '':
            stop = True

if end is not None:
    print("po " + str(q) + " generaciach sme nasli cestu:")
    vyhodnot_jedinca(end.copy_hodnoty(), pole, True)

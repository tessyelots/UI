# UI  
Zadanie č. 1  
Toto zadanie sa venuje niekoľkým základným algoritmom prehľadávania stavového priestoru.  
Definovanie problému:  
Našou úlohou je nájsť riešenie 8-hlavolamu. Hlavolam je zložený z 8 očíslovaných políčok a jedného prázdneho miesta. Políčka je možné presúvať hore, dole, vľavo alebo vpravo, ale len ak je tým smerom medzera. Je vždy daná nejaká východisková a nejaká cieľová pozícia a je potrebné nájsť postupnosť krokov, ktoré vedú z jednej pozície do druhej.  
Príkladom môže byť nasledovná začiatočná a koncová pozícia:  
  
Začiatok:  
1	2	3  
4	5	6  
7	8	   
 	Koniec:  
1	2	3  
4	6	8  
7	5	   
Im zodpovedajúca postupnosť krokov je: VPRAVO, DOLE, VĽAVO, HORE.  
  
  
  
Zadanie č. 2  
Úloha  
Majme hľadača pokladov, ktorý sa pohybuje vo svete definovanom dvojrozmernou mriežkou a zbiera poklady, ktoré nájde po ceste. Začína na políčku označenom písmenom S a môže sa pohybovať štyrmi rôznymi smermi: hore H, dole D, doprava P a doľava L. K dispozícii má konečný počet krokov. Jeho úlohou je nazbierať čo najviac pokladov. Za nájdenie pokladu sa považuje len pozícia, pri ktorej je hľadač aj poklad na tom istom políčku. Susedné políčka sa neberú do úvahy.  
  
Zadanie  
Horeuvedenú úlohu riešte prostredníctvom evolučného programovania nad virtuálnym strojom.  
Tento špecifický spôsob evolučného programovania využíva spoločnú pamäť pre údaje a inštrukcie. Pamäť je na začiatku vynulovaná a naplnená od prvej bunky inštrukciami. Za programom alebo od určeného miesta sú uložené inicializačné údaje (ak sú nejaké potrebné). Po inicializácii sa začne vykonávať program od prvej pamäťovej bunky. (Prvou je samozrejme bunka s adresou 000000.) Inštrukcie modifikujú pamäťové bunky, môžu realizovať vetvenie, programové skoky, čítať nejaké údaje zo vstupu a prípadne aj zapisovať na výstup. Program sa končí inštrukciou na zastavenie, po stanovenom počte krokov, pri chybnej inštrukcii, po úplnom alebo nesprávnom výstupe. Kvalita programu sa ohodnotí na základe vyprodukovaného výstupu alebo, keď program nezapisuje na výstup, podľa výsledného stavu určených pamäťových buniek.  
  
Virtuálny stroj  
Náš stroj bude mať 64 pamäťových buniek o veľkosti 1 byte.  
Bude poznať štyri inštrukcie: inkrementáciu hodnoty pamäťovej bunky, dekrementáciu hodnoty pamäťovej bunky, skok na adresu a výpis (H, D, P alebo L) podľa hodnoty pamäťovej bunky. Inštrukcie majú tvar podľa nasledovnej tabuľky:  
  
inštrukcia	 	tvar  
inkrementácia		00XXXXXX  
dekrementácia		01XXXXXX  
skok		10XXXXXX  
výpis		11XXXXXX  
Hodnota XXXXXX predstavuje 6-bitovú adresu pamäťovej bunky s ktorou inštrukcia pracuje (adresovať je teda možné každú). Prvé tri inštrukcie by mali byť jasné, pri poslednej je potrebné si dodefinovať, čo sa vypíše pri akej hodnote bunky. Napríklad ak bude obsahovať maximálne dve jednotky, tak to bude H, pre tri a štyri to bude D, pre päť a šesť to bude P a pre sedem a osem jednotiek v pamäťovej bunke to bude L. Ako ukážku si uvedieme jednoduchý príklad:  

 Adresa:	000000	  000001	  000010	  000011	  000100	  000101	  000110	  ...  
Hodnota:	00000000	00011111	00010000	01010000	00000101	11000000	10000100	...  
Výstup tohoto programu bude postupnosť: P H H H D H ... Ďalšie hodnoty budú závisieť od hodnôt nasledujúcich pamäťových buniek. (Dúfam, že je jasné, že uvedenú postupnosť vypisuje inštrukcia v pamäťovej bunke s adresou 5. A program je samomodifikujúci sa, takže vypísané hodnoty nezodpovedajú hodnotám na začiatku, ale počas behu programu.) Sú možné (a odporúčané) aj lepšie reprezentácie hodnôt pre H D P a L, napríklad podľa posledných dvoch bitov.  
  
Program sa zastaví, akonáhle bude splnená niektorá z nasledovných podmienok:  
  
program našiel všetky poklady  
postupnosť, generovaná programom, vybočila zo stanovenej mriežky  
program vykonal 500 krokov (inštrukcií)  
Či sa program zastaví, keď príde na poslednú bunku alebo pokračuje znovu od začiatku, si môžete zvoliť sami. (Môžete to nechať aj na voľbu používateľovi.)
Je možné navrhnúť aj komplikovanejší virtuálny stroj s rozšírenými inštrukciami a veľkosťou pamäťovej bunky viac ako osem bitov, ale musí sa dodržať podmienka maximálneho počtu pamäťových buniek 64 a limit 500 krokov programu. Rozšírenie inštrukcií sa využíva nielen na zadefinovanie nových typov inštrukcií, ale hlavne na vytvorenie inštrukcií s podmieneným vykonávaním.  
Evolučný algoritmus  
Hľadanie riešenia prebieha podľa nasledovného postupu:  
Zo vstupného súboru sa načíta rozmer mriežky, štartovacia pozícia, počet a rozmiestnenie pokladov.  
Počiatočná populácia jedincov (najmenej 20) sa nainicializuje náhodnými hodnotami v stanovenom rozsahu (napríklad prvých 16 alebo viac buniek každého jedinca).  
Každému jedincovi sa určí fitness – počet nájdených pokladov do zastavenia jeho programu.  
Ak je nájdený jedinec, ktorý našiel všetky poklady, riešenie končí s úspechom a vypísaním programu a postupnosti, ktorú vygeneroval. Ak sa vytvoril požadovaný počet populácií, algoritmus vypíše doteraz nájdené najlepšie riešenie a čaká na rozhodnutie používateľa – koniec alebo ďalšie opakovanie.  
Jednou z metód selekcie (ruleta, turnaj a iné) sa určia rodičia a krížením vytvoria nových potomkov.  
Nové jedince s istou pravdepodobnosťou mutujú a vstupujú do novej populácie.  
Keď je nová generácia kompletná, prejde sa na vykonávanie kroku 3.  
Hodnota fitness závisí v prvom rade od počtu nájdených pokladov, ale je vhodné ju zjemniť podľa počtu vykonaných krokov – kratšia postupnosť je lepšia.  
  
  
  
Zadanie 3  
Máme 2D priestor, ktorý má rozmery X a Y, v intervaloch od -5000 do +5000. V tomto priestore sa môžu nachádzať body, pričom každý bod má určenú polohu pomocou súradníc X a Y. Každý bod má unikátne súradnice (t.j. nemalo by byť viacej bodov na presne tom istom mieste). Každý bod patrí do jednej zo 4 tried, pričom tieto triedy sú: red (R), green (G), blue (B) a purple (P). Na začiatku sa v priestore nachádza 5 bodov pre každú triedu (dokopy teda 20 bodov). Súradnice počiatočných bodov sú:  
  
R: [-4500, -4400], [-4100, -3000], [-1800, -2400], [-2500, -3400] a [-2000, -1400]  
G: [+4500, -4400], [+4100, -3000], [+1800, -2400], [+2500, -3400] a [+2000, -1400]  
B: [-4500, +4400], [-4100, +3000], [-1800, +2400], [-2500, +3400] a [-2000, +1400]  
P: [+4500, +4400], [+4100, +3000], [+1800, +2400], [+2500, +3400] a [+2000, +1400]  
  
Vašou úlohou je naprogramovať klasifikátor pre nové body – v podobe funkcie classify(int X, int Y, int k), ktorá klasifikuje nový bod so súradnicami X a Y, pridá tento bod do nášho 2D priestoru (s farbou podľa klasifikácie) a vráti triedu, ktorú pridelila pre tento bod. Na klasifikáciu použite k-NN algoritmus, pričom k môže byť 1, 3, 7 alebo 15.  
  
Na demonštráciu Vášho klasifikátora vytvorte testovacie prostredie, v rámci ktorého budete postupne generovať nové body a klasifikovať ich (volaním funkcie classify). Celkovo vygenerujte 40000 nových bodov (10000 z každej triedy). Súradnice nových bodov generujte náhodne, pričom nový bod by mal mať zakaždým inú triedu (dva body vygenerované po sebe by nemali byť rovnakej triedy):  
  
R body by mali byť generované s 99% pravdepodobnosťou s X < +500 a Y < +500  
G body by mali byť generované s 99% pravdepodobnosťou s X > -500 a Y < +500  
B body by mali byť generované s 99% pravdepodobnosťou s X < +500 a Y > -500  
P body by mali byť generované s 99% pravdepodobnosťou s X > -500 a Y > -500  
  
(Zvyšné jedno percento bodov je generované v celom priestore.)  
Návratovú hodnotu funkcie classify porovnávajte s triedou vygenerovaného bodu. Na základe týchto porovnaní vyhodnoťte úspešnosť Vášho klasifikátora pre daný  experiment.  
  
Experiment vykonajte 4-krát, pričom zakaždým Váš klasifikátor použije iný parameter k (pre k = 1, 3, 7 a 15) a vygenerované body budú pre každý experiment rovnaké.  
  
Vizualizácia: pre každý z týchto experimentov vykreslite výslednú 2D plochu tak, že vyfarbíte túto plochu celú. Prázdne miesta v 2D ploche vyfarbite podľa Vášho klasifikátora.  
  
Poznámka 1: Je vhodné využiť nejaké optimalizácie na zredukovanie zložitosti:  
Pre hľadanie k najbližších bodov som rozdelil plochu na viaceré menšie štvorce, do ktorých umiestňujem body s príslušnými súradnicami, aby som nemusel vždy porovnávať všetky body, ale len body vo štvorci, kde sa nachádza aktuálny bod a susedných štvorcoch.  
  

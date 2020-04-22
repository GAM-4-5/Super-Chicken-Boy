import pygame ##jedan modul koji je trebao
pygame.init() ##pokretanje

prozor = pygame.display.set_mode((590,400)) ##veličina ekrana

pygame.display.set_caption("Razvali Bundevu") ##naslov ekrana, ime igrice

hoda_desno = [pygame.image.load('R1.png'), ##spriteovi za hodanje u desno glavnog lika, svaka slika traje 3 fps-a
              pygame.image.load('R2.png'),
              pygame.image.load('R3.png'),
              pygame.image.load('R4.png'),
              pygame.image.load('R5.png'),
              pygame.image.load('R6.png'),
              pygame.image.load('R7.png'),
              pygame.image.load('R8.png'),
              pygame.image.load('R9.png')]
hoda_lijevo = [pygame.image.load('L1.png'), ##spriteovi za hodanje u lijevo glavnog lika, svaka slika traje 3 fps-a
               pygame.image.load('L2.png'),
               pygame.image.load('L3.png'),
               pygame.image.load('L4.png'),
               pygame.image.load('L5.png'),
               pygame.image.load('L6.png'),
               pygame.image.load('L7.png'),
               pygame.image.load('L8.png'),
               pygame.image.load('L9.png')]

pozadina = pygame.image.load('bg2.jpg') ##pozadinska slika, veličina ekrana je namještena po njoj

glavni_lik = pygame.image.load('standing.png') ##slika glavnog lika kad stoji na mjestu

vrijeme = pygame.time.Clock()

class igrač(object): ##klasa glavnog lika sa svim atributima
    def __init__(self,x,y,širina,visina):
        self.x = x
        self.y = y
        self.širina = širina
        self.visina = visina
        self.brzina = 5
        self.skače = False ##varijabla skače li lik ili ne, po defaultu ne
        self.lijevo = False
        self.desno = True
        self.koraci = 0 ##broj koraka, ovisi o broju spriteova koje imamo
        self.skok = 11.5 ##maksimalna visina skoka
        self.standing = True
        self.okvir = (self.x + 17, self.y + 11, 29, 52) ##okvir lika koji interaktira sa okolinom

    def draw(self, prozor): ##funkcija za crtanje glavnog lika
        if self.koraci + 1 >= 27: ##27 jer imamo 9 spriteova za jedan smjer a svaki traje 3 fps-a
            self.koraci = 0

        if not(self.standing): ##ako ne stoji tj. ako je dana naredba za lijevo ili desno
            if self.lijevo:
                prozor.blit(hoda_lijevo[self.koraci//3], (self.x,self.y)) ##lijepljenje spriteova na prozor,lijevo
                self.koraci += 1
            elif self.desno:
                prozor.blit(hoda_desno[self.koraci//3], (self.x,self.y)) ##lijepljenje spriteova na prozor,desno
                self.koraci +=1
        else:
            if self.desno:
                prozor.blit(hoda_desno[0], (self.x, self.y)) ##kod da ne ide van prozora
            else:
                prozor.blit(hoda_lijevo[0], (self.x, self.y))
        self.okvir = (self.x + 17, self.y + 11, 29, 52)

    def pogodak(self): ##događaj ako je okvir lika dotaknuo okvir nečega drugoga
        self.skače = False
        self.skok = 11.5
        self.x = 50
        self.y = 320
        self.koraci = 0
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get(): ##igirca se može ugasiti dok je zaustavljena tj. kada je lik pogođen
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
                


class projectile(object): ##klasa za metke
    def __init__(self,x,y,radius,color,smijer):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.smijer = smijer ##smjer u kojem metak ide
        self.brzina = 8 * smijer ##brzina je određena smjerom, zbog minusa ako ide lijevo

    def draw(self,prozor): ##crtanje metka
        pygame.draw.circle(prozor, self.color, (self.x,self.y), self.radius)


class neprijatelj(object): ##klasa običnog neprijatelja
    hoda_desno = [pygame.image.load('R1E.png'), ##slike neprijatelja za u desno
                 pygame.image.load('R2E.png'),
                 pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'),
                 pygame.image.load('R5E.png'),
                 pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'),
                 pygame.image.load('R8E.png'),
                 pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'),
                 pygame.image.load('R11E.png')]
    hoda_lijevo = [pygame.image.load('L1E.png'), ##slike neprijatelja za u lijevo
                pygame.image.load('L2E.png'),
                pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'),
                pygame.image.load('L5E.png'),
                pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'),
                pygame.image.load('L8E.png'),
                pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'),
                pygame.image.load('L11E.png')]

    def __init__(self, x, y, širina, visina, kraj):
        self.x = x
        self.y = y
        self.širina = širina
        self.visina = visina
        self.kraj = kraj
        self.putanja = [self.x, self.kraj] ##raspon na kojem se neprijatelj kreće
        self.koraci = 0 ##koraci neprijatelja
        self.brzina = 4
        self.okvir = (self.x + 17, self.y + 2, 31, 57)
        self.snaga = 10
        self.vidljiv = True ##ako neprijatelj postoji tj. ako je vidljiv na ekranu

    def draw(self,prozor): ##crtanje neprijatelja
        self.kretanje()
        if self.vidljiv:
            if self.koraci + 1 >= 33:
                self.koraci = 0

            if self.brzina > 0:
                prozor.blit(self.hoda_desno[self.koraci //3], (self.x, self.y))
                self.koraci += 1
            else:
                prozor.blit(self.hoda_lijevo[self.koraci //3], (self.x, self.y))
                self.koraci += 1

            pygame.draw.rect(prozor, (255,0,0), (self.okvir[0], self.okvir[1] - 20, 50, 10)) ##health bar neprijatelja, crveni koji je stalan i stoji ispod zelenog
            pygame.draw.rect(prozor, (0,128,0), (self.okvir[0], self.okvir[1] - 20, 50 - (5 * (10 - self.snaga)), 10)) ##zeleni koji se smanjuje
            self.okvir = (self.x + 17, self.y + 2, 31, 57)

    def kretanje(self): ##kretanje neprijatelja
        if self.brzina > 0:
            if self.x + self.brzina < self.putanja[1]: ##kretanje desno
                self.x += self.brzina
            else:
                self.brzina = self.brzina * -1 ##kretanje lijevo, brzina se množi sa -1
                self.koraci = 0
        else:
            if self.x - self.brzina > self.putanja[0]:
                self.x += self.brzina
            else:
                self.brzina = self.brzina * -1
                self.koraci = 0

    def pogodak(self): ##funkcija ako je neprijatelj pogođen sa metkom
        if self.snaga > 0:
            self.snaga -= 1 ##ovdje se smanjuje zeleni health bar
        else:
            self.vidljiv = False ##ako nema više snage onda nestaje sa prozora

class boss(object): ##klasa velikog neprijatelja
    hoda_desno = [pygame.image.load('walk1.png'), ##slike kad boss ide desno
                 pygame.image.load('walk2.png'),
                 pygame.image.load('walk3.png'),
                 pygame.image.load('walk4.png'),
                 pygame.image.load('walk5.png'),
                 pygame.image.load('walk6.png'),
                 pygame.image.load('walk7.png'),
                 pygame.image.load('walk9.png'),
                 pygame.image.load('walk10.png')]
    hoda_lijevo = [pygame.image.load('walk1c.png'), ##slike kad boss ide lijevo
                pygame.image.load('walk2c.png'),
                pygame.image.load('walk3c.png'),
                pygame.image.load('walk4c.png'),
                pygame.image.load('walk5c.png'),
                pygame.image.load('walk6c.png'),
                pygame.image.load('walk7c.png'),
                pygame.image.load('walk9c.png'),
                pygame.image.load('walk10c.png')]

    def __init__(self, x, y, širina, visina, kraj): ##svi atributi bossa, slično kao kod običnog neprijatelja
        self.x = x
        self.y = y
        self.širina = širina
        self.visina = visina
        self.kraj = kraj
        self.putanja = [self.x, self.kraj]
        self.koraci = 0
        self.brzina = 5
        self.okvir = (self.x + 17, self.y + 2, 31, 57)
        self.snaga = 50
        self.vidljiv = False ##kada je boss pozvan na početku igrice ne pokazuje se još

    def draw(self,prozor): ##crtanje bossa na ekranu
        self.kretanje()
        if self.vidljiv:
            if self.koraci + 1 >= 27: ##drugačiji je broj koraka jer boss ima manje spriteova od ostala dva lika, fps mora ostati prilagođen
                self.koraci = 0

            if self.brzina > 0:
                prozor.blit(self.hoda_desno[self.koraci//3], (self.x, self.y))
                self.koraci += 1
            else:
                prozor.blit(self.hoda_lijevo[self.koraci//3], (self.x, self.y))
                self.koraci += 1

            pygame.draw.rect(prozor, (255,0,0), (self.okvir[0]-70, self.okvir[1] - 20, 250, 10)) ##health bar neprijatelja, crveni koji je stalan i stoji ispod zelenog
            pygame.draw.rect(prozor, (0,128,0), (self.okvir[0]-70, self.okvir[1] - 20, 250 - (5 * (50 - self.snaga)), 10)) ##zeleni koji se smanjuje
            self.okvir = (self.x + 32, self.y + 40, 93, 140)

    def kretanje(self): ##kretanje bossa po prozoru
        if self.brzina > 0:
            if self.x + self.brzina < self.putanja[1]:
                self.x += self.brzina
            else:
                self.brzina = self.brzina * -1
                self.koraci = 0
        else:
            if self.x - self.brzina > self.putanja[0]:
                self.x += self.brzina
            else:
                self.brzina = self.brzina * -1
                self.koraci = 0

    def pogodak(self): ##ako je pogođen, isto kao kod neprijatelja
        if self.snaga > 0:
            self.snaga -= 1
        else:
            self.vidljiv = False ##ako nema health pointsa ponovno postaje nevidljiv i ne interaktira
        

def crtanje_po_prozoru(): ##sva crtanja po ekranu, likovi, tekst, metci, pozadina
    prozor.blit(pozadina, (0,0))
    man.draw(prozor)
    čudovište.draw(prozor)
    šef.draw(prozor)
    text = font.render('POBIJEDIO SI, KUL', 1, (255,0,0))
    if šef.snaga == 0:
        prozor.blit(text, (110, 180))
    for metak in metci:
        metak.draw(prozor)
    
    pygame.display.update() ##osvježavanje ekrana da likovi budu nacrtani, inače budu samo prvi frame pa ih ne možemo primjetiti


man = igrač(350, 310, 64,64) ##pozvan je glavni lik sa svim karakteristikama
čudovište = neprijatelj(15, 315, 64, 64, 520) ##pozvan je obični neprijatelj sa svim karakteristikama
šef = boss(55, 200, 150, 198, 450) ##pozvan je boss sa svim karakteristikama, stoji dosta niže od ostalih zbog većih spriteova
petlja = 0
metci = []
run = True ##pokrenuto
broj_goblina = 0
font = pygame.font.SysFont('comicsans', 50, True) ##font i veličina svog teksta u igrici
while run: ##kad igrica traje
    vrijeme.tick(27) ##odabiranje fps-a

    if čudovište.vidljiv == False and broj_goblina < 4: ##nakon što neprijatelj umre pojavljuje se novi, tako dok ih ne prođe 5
        čudovište = neprijatelj(100, 320, 64, 64, 520)
        broj_goblina += 1

    if broj_goblina == 4 and čudovište.vidljiv == False and šef.snaga > 0: ##kada više nema neprijatelja tj. prošlo ih je 5, dolazi boss
        šef.vidljiv = True
        
    if čudovište.vidljiv == True: ##mora biti uvjet da neprijatelj postoji inače će interaktirati i kada se nevidi
        if man.okvir[1] < čudovište.okvir[1] + čudovište.okvir[3] and man.okvir[1] + man.okvir[3] > čudovište.okvir[1]:
            if man.okvir[0] + man.okvir[2] > čudovište.okvir[0] and man.okvir[0] < čudovište.okvir[0] + čudovište.okvir[2]:
                man.pogodak() ##pozvana funkcija za pogađanje glavnog lika ako je njegov okvir dotaknuo okvir neprijatelja

    if šef.vidljiv == True:
        if man.okvir[1] < šef.okvir[1] + šef.okvir[3] and man.okvir[1] + man.okvir[3] > šef.okvir[1]:
            if man.okvir[0] + man.okvir[2] > šef.okvir[0] and man.okvir[0] < šef.okvir[0] + šef.okvir[2]:
                man.pogodak() ##pozvana funkcija za pogađanje glavnog lika ako je njegov okvir dotaknuo okvir neprijatelja

    if petlja > 0:
        petlja += 1
    if petlja > 3:
        petlja = 0
    
    for event in pygame.event.get(): ##ako u bilo kojem trenutku želimo ugasiti igricu
        if event.type == pygame.QUIT:
            run = False ##prestaje biti pokrenuta
        
    for metak in metci: ##interakcija metka i neprijatelja, dodir sa okvirom
        if metak.y - metak.radius < čudovište.okvir[1] + čudovište.okvir[3] and metak.y + metak.radius > čudovište.okvir[1] and čudovište.vidljiv == True:
            if metak.x + metak.radius > čudovište.okvir[0] and metak.x - metak.radius < čudovište.okvir[0] + čudovište.okvir[2]:
                čudovište.pogodak()
                metci.pop(metci.index(metak)) ##ako je mtak pogodio, on nestaje

    for metak in metci: ##interakcija metka i bossa, dodir sa okvirom
        if metak.y - metak.radius < šef.okvir[1] + šef.okvir[3] and metak.y + metak.radius > šef.okvir[1] and šef.vidljiv == True:
            if metak.x + metak.radius > šef.okvir[0] and metak.x - metak.radius < šef.okvir[0] + šef.okvir[2]:
                šef.pogodak()
                metci.pop(metci.index(metak)) ##ako je metak pogodio, on nestaje
                
        if metak.x < 590 and metak.x > 0: ##gleda je li metak van prozora
            metak.x += metak.brzina
        else:
            metci.pop(metci.index(metak)) ##ako je onda ga briše iz liste tj. nestaje

    tipka = pygame.key.get_pressed() ##pritisnute komande

    if tipka[pygame.K_SPACE] and petlja == 0: ##SPACE je tipka za pucanje, ako je pritisnuta crtaju se metci iz liste
        if man.lijevo:
            smijer = -1 ##ako idu lijevo
        else:
            smijer = 1 ##ako idu desno
            
        if len(metci) < 7: ##ne može biti više od sedam metaka na ekranu
            metci.append(projectile(round(man.x + man.širina //2), round(man.y + man.visina//2), 7, (255,0,0), smijer)) ##metak kreće izvan ekrana glavnog lika

        petlja = 1

    if tipka[pygame.K_LEFT] and man.x > man.brzina: ##ako je stisnuta naredba za u lijevo
        man.x -= man.brzina
        man.lijevo = True
        man.desno = False
        man.standing = False
    elif tipka[pygame.K_RIGHT] and man.x < 500 - man.širina - man.brzina: ##ako je stisnuta naredba za u lijevo
        man.x += man.brzina
        man.desno = True
        man.lijevo = False
        man.standing = False
    else: ## ako stoji na mjestu
        man.standing = True
        man.koraci = 0 ##koraci se vraćaju na 0 jer stoji na mjestu
        
    if not(man.skače): ##ako skače po defaultu je False
        if tipka[pygame.K_UP]: ##ako je stisnuta tipka za skok
            man.skače = True
            man.koraci = 0 ##resetiranje koraka
    else:
        if man.skok >= -11.5:
            neg = 1
            if man.skok < 0:
                neg = -1
            man.y -= (man.skok ** 2) * 0.5 * neg ##skakanje po paraboli, malo reducirano da izgleda realnije (*0.5),
            man.skok -= 1                        ##kada skače prema gore ide po negativnom y, a kada se vraća ide po pozitivnom
        else:
            man.skače = False
            man.skok = 11.5
            
    crtanje_po_prozoru() ##pozivanje funkcije za crtanje svega

pygame.quit() ##zatvaranje programa

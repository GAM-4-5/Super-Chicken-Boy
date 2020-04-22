import pygame ##jedan modul koji je trebao
pygame.init() ##pokretanje

win = pygame.display.set_mode((590,400)) ##veličina ekrana

pygame.display.set_caption("Super_Chicken_Boy") ##naslov ekrana, ime igrice

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

class player(object): ##klasa glavnog lika sa svim atributima
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False ##varijabla skače li lik ili ne, po defaultu ne
        self.left = False
        self.right = True
        self.walkCount = 0 ##broj koraka, ovisi o broju spriteova koje imamo
        self.jumpCount = 11.5 ##maksimalna visina skoka
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) ##okvir lika koji interaktira sa okolinom

    def draw(self, win): ##funkcija za crtanje glavnog lika
        if self.walkCount + 1 >= 27: ##27 jer imamo 9 spriteova za jedan smjer a svaki traje 3 fps-a
            self.walkCount = 0

        if not(self.standing): ##ako ne stoji tj. ako je dana naredba za lijevo ili desno
            if self.left:
                win.blit(hoda_lijevo[self.walkCount//3], (self.x,self.y)) ##lijepljenje spriteova na prozor,lijevo
                self.walkCount += 1
            elif self.right:
                win.blit(hoda_desno[self.walkCount//3], (self.x,self.y)) ##lijepljenje spriteova na prozor,desno
                self.walkCount +=1
        else:
            if self.right:
                win.blit(hoda_desno[0], (self.x, self.y)) ##kod da ne ide van prozora
            else:
                win.blit(hoda_lijevo[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def hit(self): ##događaj ako je okvir lika dotaknuo okvir nečega drugoga
        self.isJump = False
        self.jumpCount = 11.5
        self.x = 50
        self.y = 320
        self.walkCount = 0
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get(): ##igirca se može ugasiti dok je zaustavljena,kada je lik pogođen
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
                


class projectile(object): ##klasa za metke
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing ##smjer u kojem metak ide
        self.vel = 8 * facing ##brzina je određena smjerom, zbog minusa ako ide lijevo

    def draw(self,win): ##crtanje metka
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)


class enemy(object): ##klasa običnog neprijatelja
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

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end] ##raspon na kojem se neprijatelj kreće
        self.walkCount = 0 ##koraci neprijatelja
        self.vel = 4
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True ##ako neprijatelj postoji tj. ako je vidljiv na ekranu

    def draw(self,win): ##crtanje neprijatelja
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.hoda_desno[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.hoda_lijevo[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10)) ##health bar neprijatelja, crveni koji je stalan i stoji ispod zelenog
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10)) ##zeleni koji se smanjuje
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self): ##kretanje neprijatelja
        if self.vel > 0:
            if self.x + self.vel < self.path[1]: ##kretanje desno
                self.x += self.vel
            else:
                self.vel = self.vel * -1 ##kretanje lijevo, brzina se množi sa -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self): ##funkcija ako je neprijatelj pogođen sa metkom
        if self.health > 0:
            self.health -= 1 ##ovdje se smanjuje zeleni health bar
        else:
            self.visible = False ##ako nema više snage onda nestaje sa prozora

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

    def __init__(self, x, y, width, height, end): ##svi atributi bossa, slično kao kod običnog neprijatelja
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 5
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 50
        self.visible = False ##kada je boss pozvan na početku igrice ne pokazuje se još

    def draw(self,win): ##crtanje bossa na ekranu
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27: ##drugačiji je broj koraka jer boss ima manje spriteova od ostala dva lika, fps mora ostati prilagođen
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.hoda_desno[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.hoda_lijevo[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0]-70, self.hitbox[1] - 20, 250, 10)) ##health bar neprijatelja, crveni koji je stalan i stoji ispod zelenog
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0]-70, self.hitbox[1] - 20, 250 - (5 * (50 - self.health)), 10)) ##zeleni koji se smanjuje
            self.hitbox = (self.x + 32, self.y + 40, 93, 140)

    def move(self): ##kretanje bossa po prozoru
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self): ##ako je pogođen, isto kao kod neprijatelja
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False ##ako nema health pointsa ponovno postaje nevidljiv i ne interaktira
        

def redrawGameWindow(): ##sva crtanja po ekranu, likovi, tekst, metci, pozadina
    win.blit(pozadina, (0,0))
    man.draw(win)
    goblin.draw(win)
    šef.draw(win)
    text = font.render('POBIJEDIO SI, KUL', 1, (255,0,0))
    if šef.health == 0:
        win.blit(text, (110, 180))
    for metak in metci:
        metak.draw(win)
    
    pygame.display.update() ##osvježavanje ekrana da likovi budu nacrtani, inače budu samo prvi frame pa ih ne možemo primjetiti


man = player(350, 310, 64,64) ##pozvan je glavni lik sa svim karakteristikama
goblin = enemy(15, 315, 64, 64, 520) ##pozvan je obični neprijatelj sa svim karakteristikama
šef = boss(55, 200, 150, 198, 450) ##pozvan je boss sa svim karakteristikama, stoji dosta niže od ostalih zbog većih spriteova
shootLoop = 0
metci = []
run = True ##pokrenuto
broj_goblina = 0
font = pygame.font.SysFont('comicsans', 50, True) ##font i veličina svog teksta u igrici
while run: ##kad igrica traje
    vrijeme.tick(27) ##odabiranje fps-a

    if goblin.visible == False and broj_goblina < 4: ##nakon što neprijatelj umre pojavljuje se novi, tako dok ih ne prođe 5
        goblin = enemy(100, 320, 64, 64, 520)
        broj_goblina += 1

    if broj_goblina == 4 and goblin.visible == False and šef.health > 0: ##kada više nema neprijatelja tj. prošlo ih je 5, dolazi boss
        šef.visible = True
        
    if goblin.visible == True: ##mora biti uvjet da neprijatelj postoji inače će interaktirati i kada se nevidi
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit() ##pozvana funkcija za pogađanje glavnog lika ako je njegov okvir dotaknuo okvir neprijatelja

    if šef.visible == True:
        if man.hitbox[1] < šef.hitbox[1] + šef.hitbox[3] and man.hitbox[1] + man.hitbox[3] > šef.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > šef.hitbox[0] and man.hitbox[0] < šef.hitbox[0] + šef.hitbox[2]:
                man.hit() ##pozvana funkcija za pogađanje glavnog lika ako je njegov okvir dotaknuo okvir neprijatelja

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    
    for event in pygame.event.get(): ##ako u bilo kojem trenutku želimo ugasiti igricu
        if event.type == pygame.QUIT:
            run = False ##prestaje biti pokrenuta
        
    for metak in metci: ##interakcija metka i neprijatelja, dodir sa okvirom
        if metak.y - metak.radius < goblin.hitbox[1] + goblin.hitbox[3] and metak.y + metak.radius > goblin.hitbox[1] and goblin.visible == True:
            if metak.x + metak.radius > goblin.hitbox[0] and metak.x - metak.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                metci.pop(metci.index(metak)) ##ako je mtak pogodio, on nestaje

    for metak in metci: ##interakcija metka i bossa, dodir sa okvirom
        if metak.y - metak.radius < šef.hitbox[1] + šef.hitbox[3] and metak.y + metak.radius > šef.hitbox[1] and šef.visible == True:
            if metak.x + metak.radius > šef.hitbox[0] and metak.x - metak.radius < šef.hitbox[0] + šef.hitbox[2]:
                šef.hit()
                metci.pop(metci.index(metak)) ##ako je metak pogodio, on nestaje
                
        if metak.x < 590 and metak.x > 0: ##gleda je li metak van prozora
            metak.x += metak.vel
        else:
            metci.pop(metci.index(metak)) ##ako je onda ga briše iz liste tj. nestaje

    keys = pygame.key.get_pressed() ##pritisnute komande

    if keys[pygame.K_SPACE] and shootLoop == 0: ##SPACE je tipka za pucanje, ako je pritisnuta crtaju se metci iz liste
        if man.left:
            facing = -1 ##ako idu lijevo
        else:
            facing = 1 ##ako idu desno
            
        if len(metci) < 7: ##ne može biti više od sedam metaka na ekranu
            metci.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 7, (255,0,0), facing)) ##metak kreće izvan ekrana glavnog lika

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel: ##ako je stisnuta naredba za u lijevo
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel: ##ako je stisnuta naredba za u lijevo
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else: ## ako stoji na mjestu
        man.standing = True
        man.walkCount = 0 ##koraci se vraćaju na 0 jer stoji na mjestu
        
    if not(man.isJump): ##ako skače po defaultu je False
        if keys[pygame.K_UP]: ##ako je stisnuta tipka za skok
            man.isJump = True
            man.walkCount = 0 ##resetiranje koraka
    else:
        if man.jumpCount >= -11.5:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg ##skakanje po paraboli, malo reducirano da izgleda realnije (*0.5),
            man.jumpCount -= 1                        ##kada skače prema gore ide po negativnom y, a kada se vraća ide po pozitivnom
        else:
            man.isJump = False
            man.jumpCount = 11.5
            
    redrawGameWindow() ##pozivanje funkcije za crtanje svega

pygame.quit() ##zatvaranje programa

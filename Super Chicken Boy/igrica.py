import pygame
pygame.init()

win = pygame.display.set_mode((600,400)) ##predispozicije prozora

pygame.display.set_caption("Super_Chicken_Boy") ##ime tj. naslov prikazan na prozoru

walkRight = [pygame.image.load('R1.png'), ##slike koje se mijenjaju kad je dana naredba za kretanje u desno
             pygame.image.load('R2.png'),
             pygame.image.load('R3.png'),
             pygame.image.load('R4.png'),
             pygame.image.load('R5.png'),
             pygame.image.load('R6.png'),
             pygame.image.load('R7.png'),
             pygame.image.load('R8.png'),
             pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), ##slike koje se mijenjaju kad je dana naredba za kretanje u desno
            pygame.image.load('L2.png'),
            pygame.image.load('L3.png'),
            pygame.image.load('L4.png'),
            pygame.image.load('L5.png'),
            pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), 
            pygame.image.load('L8.png'),
            pygame.image.load('L9.png')]

bg = pygame.image.load('bg2.jpg') ##pozadinska slika,fiksna je
char = pygame.image.load('standing.png') ##slika lika na početku prije davanja komandi za kretanje

clock = pygame.time.Clock()


class player(object): ##atributi lika (početna pozicija, brzina itd.)
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing): ##komande ako je lik u pokretu
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:                  ##ako se prestao gibati koja će slika ostati ovisno o zadnjem smjeru kretanja
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
                


class projectile(object): ##atributi metka
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing

    def draw(self,win): ##crtanje metka
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)



def redrawGameWindow():
    win.blit(bg, (0,0))
    man.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update() ##osvježavanje prozora da prikazuje elemente na ekranu


##glavna petlja, tu su sve radnje koje se trenutno izvode
man = player(50, 320, 64,64)
bullets = [] ##prazna lista u kojoj su poslije metci 
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get(): ##zatvaranje prozora ako se stisne X
        if event.type == pygame.QUIT:
            run = False
        
    for bullet in bullets:
        if bullet.x < 600 and bullet.x > 0: ##metak smije ispalit ako je u granicama prozora
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet)) ##ako metak izađe van ekrana onda mora nestat

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1 ##ako ide u lijevo onda mora oduzet
        else:
            facing = 1 ##ako ide u desno onda dodaje prema x osi
            
        if len(bullets) < 8: ##broj metaka koji maksimalno može bit na ekranu
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 9, (255,0,0), facing))

    if keys[pygame.K_LEFT] and man.x > man.vel: ##kretanje po x osi u lijevo, ovisi o brzini koja je zadana
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel: ##kretanje po x osi u desno, ovisi o brzini koja je zadana
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]: ##skakanje 
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg ##kvadratna funkcija, skok je prezentiran kao parabola
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()

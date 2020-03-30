import pygame
pygame.init()

win = pygame.display.set_mode((600,600))
screenwidth=600
screenheight=600

pygame.display.set_caption("Super Chicken boy")

x = int(50)
y = int(450)
width = int(40)
height = int(50)
vel = 10

isJump = False
jumpCount=10

run = True
while run:
    pygame.time.delay(50)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            

    pygame.draw.rect(win,(255,0,0),(x,y,width,height))
    pygame.display.update()
    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < (screenwidth - width - vel):
        x += vel
    if not (isJump):
        if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < (screenheight - height - vel):
            y+= vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount**2)*0.5 *neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    win.fill((0,0,0))
    

    


pygame.quit()

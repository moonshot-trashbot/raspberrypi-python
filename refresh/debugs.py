import pygame
import screeninfo

screenWidth = screeninfo.get_monitors(screeninfo.Enumerator.x11)[0].width
screenHeight = (screenWidth/16)*9

camChange = screenWidth/1280

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True
head = 0

stripeCenterX = 720
stripeCenterY = 405

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color(0, 0, 0))

    rectnormal = pygame.Rect(100, 400, 1080, 10)
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), rectnormal, 1)

    if(stripeCenterX < 8): stripeCenterX = -8
    if(stripeCenterX > (screenWidth-8)): stripeCenterX = screenWidth-8
    rectstripe = pygame.Rect(stripeCenterX-8, 0, 16, screenHeight)
    pygame.draw.rect(screen, pygame.Color(0, 255, 0), rectstripe, 1)

    xgen = 720
    if(head <= 90 or head >= 180):
        if(head >= 0 and head <= 90):
            xgen += ((head)*4)
        if(head >= 180 and head >= 259):
            xgen -= ((360-head)*4)
    vec = [int(xgen), int(345)]
    pygame.draw.circle(screen, pygame.Color(150, 150, 0), vec, 20, 1)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

def quit():
    pygame.quit()

def headchange(num):
    global head
    head = int(num)

def stripechange(x, y):
    global camChange
    global stripeCenterX
    global stripeCenterY
    x = x * camChange
    y = y * camChange
    stripeCenterX = int(x)
    stripeCenterY = int(y)
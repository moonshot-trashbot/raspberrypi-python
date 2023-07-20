import pygame

screenWidth = 1440
screenHeight = 810

camChange = 1440/1280

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

    screen.fill("white")

    rectnormal = pygame.Rect(100, 400, 1080, 10)
    pygame.draw.rect(screen, "black", rectnormal, 1)

    if(stripeCenterX < 8): stripeCenterX = -8
    if(stripeCenterX > (screenWidth-8)): stripeCenterX = screenWidth-8
    rectstripe = pygame.Rect(stripeCenterX-8, 0, 16, screenHeight)
    pygame.draw.rect(screen, "green", rectstripe, 1)

    xgen = 720
    if(head <= 90 or head >= 180):
        if(head >= 0 and head <= 90):
            xgen += ((head)*4)
        if(head >= 180 and head >= 259):
            xgen -= ((360-head)*4)
    vec = pygame.Vector2(xgen, 345)
    pygame.draw.circle(screen, "purple", vec, 20, 1)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

def quit():
    pygame.quit()

def headchange(num):
    global head
    head = num

def stripechange(x, y):
    global camChange
    global stripeCenterX
    global stripeCenterY
    x = x * camChange
    y = y * camChange
    stripeCenterX = x
    stripeCenterY = y
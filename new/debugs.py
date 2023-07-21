import pygame
from screeninfo import get_monitors, Enumerator
import _classes

screenWidth = int(get_monitors(Enumerator.Xinerama)[0].width)
screenHeight = int((screenWidth/16)*9)

camChange = screenWidth/1280
cmult = int(screenWidth/360)

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True
head = 0

xMid = int(screenWidth/2)
yMid = int(screenHeight/2)
stripeCenterX = xMid
stripeCenterY = yMid

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
    stripeCenterX = int(screenWidth - x)
    stripeCenterY = int(screenHeight - y)

def main():
    global xMid
    global yMid
    global cmult
    global running
    global head
    global stripeCenterY
    global stripeCenterX
    global stripeCenterY
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        screen.fill(pygame.Color(0, 0, 0))

        rectnormal = pygame.Rect(int((screenWidth - (360*cmult))/2), 400, 360*cmult, 5)
        pygame.draw.rect(screen, pygame.Color(100, 100, 255), rectnormal)

        if(stripeCenterX < 25): stripeCenterX = -25
        if(stripeCenterX > (screenWidth-25)): stripeCenterX = screenWidth-25
        rectstripe = pygame.Rect(stripeCenterX-10, 0, 20, screenHeight)
        pygame.draw.rect(screen, pygame.Color(10, 255, 10), rectstripe)

        xgen = xMid

        if(head <= 90 and head >= -90):
            xgen = xMid + ((head)*cmult)
        vec = [int(xgen), int(yMid-10)]
        pygame.draw.circle(screen, pygame.Color(150, 150, 0), vec, 20)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


thr = _classes.StoppableThread(target=main)
thr.start()
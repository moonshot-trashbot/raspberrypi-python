import pygame
from screeninfo import get_monitors, Enumerator
import _classes

screenWidth = int(get_monitors(Enumerator.Xinerama)[0].width)
screenHeight = int((screenWidth/16)*9)

camChange = screenWidth/1280

global head
global stripeCenterX
global stripeCenterY
global xMid
global yMid

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
    stripeCenterX = int(x)
    stripeCenterY = int(y)

def main():
    global xMid
    global yMid
    global running
    global stripeCenterY
    global stripeCenterX
    global stripeCenterY
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(pygame.Color(0, 0, 0))

        rectnormal = pygame.Rect(int((screenWidth - (360*4))/2), 400, 360*4, 10)
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), rectnormal)

        if(stripeCenterX < 8): stripeCenterX = -8
        if(stripeCenterX > (screenWidth-8)): stripeCenterX = screenWidth-8
        rectstripe = pygame.Rect(stripeCenterX-8, 0, 16, screenHeight)
        pygame.draw.rect(screen, pygame.Color(0, 255, 0), rectstripe)

        xgen = xMid
        if(head <= 90 or head >= 180):
            if(head >= 0 and head <= 90):
                xgen = xMid + ((head)*4)
            if(head >= 180 and head >= 259):
                xgen = xMid - ((360-head)*4)
        vec = [int(xgen), int(yMid-10)]
        pygame.draw.circle(screen, pygame.Color(150, 150, 0), vec, 20)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


thr = _classes.StoppableThread(target=main)
thr.start()
thr.join()
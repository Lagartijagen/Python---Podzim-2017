from pygame import display, draw, time, event
import pygame
from random import randint

class Bubble:
    def __init__(self):
        self.colour = [randint(0,255), randint(0,255), randint(0,255)]
        self.center = [randint(1,599) , randint(1,799)]
        self.radius = 1

    def expand(self):
        self.radius += 1




screen = display.set_mode([800, 600])

def CreateBubbles(Bubbles):
    if Bubbles.__len__() < 30:
        Bubbles.append(Bubble())
    else:
        Bubbles.pop(0)

def DrawBubbles(Bubbles):
    for bubble in Bubbles:
        draw.circle(screen, bubble.colour, bubble. center, bubble.radius, 1)
        if bubble.radius < 50:
            bubble.expand()

def main():
    Bubbles = []
    infoObject = display.Info()
    screen = display.set_mode((infoObject.current_w, infoObject.current_h))
    keypressed = True
    while keypressed:
        screen.fill([0, 0, 0])
        CreateBubbles(Bubbles)
        DrawBubbles(Bubbles)
        time.wait(15)
        display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keypressed = False


if __name__ == '__main__':
    main()
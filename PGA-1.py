import random

import pygame as p
import sys  # most commonly used to turn the interpreter off (shut down your game)
from golf_ball import *

# Constants - sets the size of the window
window_bounds = WIDTH, HEIGHT, scale = 600, 600, 0.5
origin = x0, y0 = WIDTH/2, HEIGHT-HEIGHT/2  # This is the new origin
dt = 0.001
timer = 0
ballsize = 1
object_list = []


def ball_xy(ball):
    return ball.pos.x*scale, origin[1] - ball.pos.y*scale - 1


screen = p.display.set_mode((WIDTH, HEIGHT))


def pygame_init():
    # Screen or whatever you want to call it is your best friend - it's a canvas
    # or surface where you can draw - generally you'll have one large canvas and
    # additional surfaces on top - effectively breaking things up and giving
    # you the ability to have multiples scenes in one window
    p.init()
    screen.fill((180, 210, 255))
    p.display.set_caption('Fireworks')


def drawer(object_list, place_to_draw_stuff=screen):
    for i in object_list:
        p.draw.circle(place_to_draw_stuff, i.color, ball_xy(i), 1)


# PUT SETUP CODE HERE ----------------------------------------------------------
object_list = [golf_ball_from_angle(Vec(0, 0), 77, 12, spin(240), Vec(0,0,0), 20), golf_ball_from_angle(Vec(0, 0), 75, 10, spin(280), Vec(0,0,0), 20), golf_ball_from_angle(Vec(0, 0), 77, 12, spin(240), Vec(15,0,0), 20), golf_ball_from_angle(Vec(0, 0), 75, 10, spin(280), Vec(15,0,0), 20)]
#golf_ball_from_angle(Vec(0, 0), 40, 42, spin(0), Vec(0,0,0)), golf_ball_from_angle(Vec(0, 0), 75, 10, spin(0), Vec(0,0,0)),
print(object_list)

# PUT SETUP CODE HERE ----------------------------------------------------------

running = False
screen.fill((150, 210, 255))
while True:
    #keystroke example
    for event in p.event.get():

        if event.type == p.QUIT:  # this refers to clicking on the "x"-close
            p.quit()
            sys.exit()

        elif event.type == p.KEYDOWN:  # there's a separate system built in
            # for multiple key presses or presses
            # that result in changes of state - tba
            if event.key == p.K_g:
                print("n")

            if event.key == p.K_a:
                print("goodbye")

            if event.key == p.K_SPACE:
                if running is False:
                    running = True
                    print("START")
                elif running is True:
                    running = False
                    print("PAUSE")

    if running:
        #background

        for z in range(100):

            timer += dt

            for o in object_list:
                o.step()
    drawer(object_list)

    # p.draw.rect(screen, (50, 200, 100), (0, y0, WIDTH, HEIGHT))
    p.display.flip()

    # This sets an upper limit on the frame rate (here 100 frames per second)
    # often you won't be able
    # p.time.Clock().tick(100)

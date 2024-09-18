import random

import pygame as p
import sys  # most commonly used to turn the interpreter off (shut down your game)
from golf_ball import *

# Constants - sets the size of the window
window_bounds = WIDTH, HEIGHT, scale = 600, 600, 16
origin = x0, y0 = WIDTH/2, HEIGHT-HEIGHT/2  # This is the new origin
dt = 0.001
timer = 0
ballsize = 1
object_list = []
current_best_speed = 14.2
precision_value = 0.000001
balls_per_run = 500


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


def check_finished(object_list):
    willoutput = True
    for o in object_list:
        if isinstance(o.range, bool):
            willoutput = False
    return willoutput


def find_closest_range(object_list):
    ranges = []
    for o in object_list:
        ranges.append([o.initialv, o.range])
    ranges.sort(key= lambda x: abs(36.576-x[1]))
    return ranges[0][0]

def set_up_balls():
    global object_list
    for i in range(balls_per_run):
        object_list = []
        object_list.append(
            golf_ball_from_angle(Vec(0, 0), current_best_speed + precision_value * (i - balls_per_run / 2),
                                 8.5, spin(0), Vec(0, 0, 0)))
        for o in object_list:
            o.force_due_to_gravity = o.m * Vec(0, -1.62, 0)
            # I didn't want to change the air density
            o.dragCoefficient = 0
            o.printedend = True

# PUT SETUP CODE HERE ----------------------------------------------------------
# object_list = [golf_ball_from_angle(Vec(0, 0), 15, 8.5, spin(0), Vec(0,0,0))]
for i in range(balls_per_run):
    object_list.append(golf_ball_from_angle(Vec(0, 0), current_best_speed+precision_value*(i-balls_per_run/2), 8.5, spin(0), Vec(0,0,0)))
for o in object_list:
    o.force_due_to_gravity = o.m * Vec(0, -1.62, 0)
    #I didn't want to change the air density
    o.dragCoefficient = 0
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

        for z in range(1):

            timer += dt

            for o in object_list:
                o.step()

            if check_finished(object_list):
                current_best_speed = find_closest_range(object_list)
                precision_value = precision_value/10
                set_up_balls()
                print(current_best_speed)


    drawer(object_list)

    p.draw.rect(screen, (50, 200, 100), (0, y0, WIDTH, HEIGHT))
    p.display.flip()

    # This sets an upper limit on the frame rate (here 100 frames per second)
    # often you won't be able
    # p.time.Clock().tick(100)

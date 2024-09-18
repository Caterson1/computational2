import random

import pygame as p
import sys  # most commonly used to turn the interpreter off (shut down your game)
from golf_ball import *

# Constants - sets the size of the window
window_bounds = WIDTH, HEIGHT, scale = 600, 600, 3
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


def drawer_of_lists(object_list):
    for i in object_list:
        drawer(i)


def check_finished(object_list):
    willoutput = True
    for o in object_list:
        if isinstance(o.range, bool):
            willoutput = False
    return willoutput


def generate_list(num_balls, speed, angle, spin, color):
    if math.sqrt(num_balls).is_integer():
        output = []
        windspeeds = []
        xz = 0
        for i in range(int(math.sqrt(num_balls))):
            for ii in range(int(math.sqrt(num_balls))):
                windspeeds.append(vectorize(15, (360 * ii)/math.sqrt(num_balls), xz))
            xz = (360 * i)/math.sqrt(num_balls)
        print(windspeeds)
        for i in range(num_balls):
            output.append(golf_ball_from_angle(Vec(), speed, angle, spin, windspeeds[i], 20))
            output[i].color = color
        return output
    raise TypeError(f"numballs must be a perfect square, you inputted {num_balls}")

# PUT SETUP CODE HERE ----------------------------------------------------------
number_of_balls = 16
driver1 = generate_list(number_of_balls, 77, 12, spin(240), (255, 0, 0))
driver2 = generate_list(number_of_balls, 75, 10, spin(280), (0, 255, 0))
print(object_list)

# PUT SETUP CODE HERE ----------------------------------------------------------

running = False
screen.fill((150, 210, 255))
printed1 = False
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
            if check_finished(driver1) and check_finished(driver2) and not printed1:
                ranges = []
                for o in driver1:
                    ranges.append(o.range)
                print(f"DRIVER1 RANGES: {ranges}\nD1 AVERAGE: {sum(ranges)/len(ranges)}")
                ranges = []
                for o in driver2:
                    ranges.append(o.range)
                print(f"DRIVER2 RANGES: {ranges}\nD2 AVERAGE: {sum(ranges) / len(ranges)}")
                printed1 = True
            timer += dt
            for o in driver1:
                o.step()
            for o in driver2:
                o.step()
    drawer(driver1)
    drawer(driver2)

    # p.draw.rect(screen, (50, 200, 100), (0, y0, WIDTH, HEIGHT))
    p.display.flip()

    # This sets an upper limit on the frame rate (here 100 frames per second)
    # often you won't be able
    # p.time.Clock().tick(100)

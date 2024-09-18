from random import randrange
from random import random
import vectors
from physics import *

airdensity = {"skydiver" : "VARIABLE", "racecar" : 1.15, "pumkin chunkin" : 0.95}


class Ball:
    def __init__(self, pos: Vec = Vec(),
                 velocity: Vec = Vec(10, 10),
                 acceleration: Vec = g,
                 mass: float = 4,
                 radius_or_rad_plus_drag_coeffs: int = 0.10,
                 wind_speed: Vec = Vec(0, 0, 0),
                 color: tuple = (255 * random(), 255 * random(), 255 * random()),
                 force_list: list = [],
                 floor: float = 0,
                 does_drag: bool = True):
        self.pos = pos
        self.v = velocity
        self.a = acceleration
        self.m = mass
        # Allows me to set drag coefficients in setup
        if isinstance(radius_or_rad_plus_drag_coeffs, (float, int)):
            self.r = radius_or_rad_plus_drag_coeffs
        elif isinstance(radius_or_rad_plus_drag_coeffs, tuple):
            self.r = radius_or_rad_plus_drag_coeffs[0]
            self.A = radius_or_rad_plus_drag_coeffs[1]
            self.dragCoefficient = radius_or_rad_plus_drag_coeffs[2]
        else:
            raise TypeError("radius must be either just an int or a tuple in the format: (radius, "
                            "front facing area, drag coefficient)")
        self.color = color
        self.forces = force_list
        self.does_drag = does_drag
        self.vba = self.v - wind_speed
        self.wind_speed = wind_speed
        self.floor = floor
        if not isinstance(radius_or_rad_plus_drag_coeffs, tuple):
            self.A = math.pi * self.r * self.r
            self.dragCoefficient = 0.5
        self.force_due_to_gravity = self.m * g

    def drag_override(self, A, drag_coefficient):
        self.A = A
        self.dragCoefficient = drag_coefficient

    def vel_override(self, v):
        self.v = v

    def mass_override(self, m):
        self.m = m
        self.force_due_to_gravity = m * g


    def wind(self, wind_speed: Vec = Vec()):
        self.wind_speed = wind_speed

    def add_force(self, *forces_lol):
        for force in forces_lol:
            self.forces.append(force)

    def stop(self):
        self.a = Vec()
        self.forces = []
        self.v = Vec()
        return

    def drag(self, mode = "racecar"):
        # Fd = -1/2(C{coefficient of drag}A{Front-facing area}p{densityofair}v{speed}v{v.norm}
        if self.does_drag:
            if mode == "skydiver":
                T = 15.04 - 0.00649*self.pos.y
                P = 101.29 * ((T+273.1)/288.08)**5.256
                p = P/(0.2869 * (T+273.1))
                return drag(self.dragCoefficient, self.A, p, self.vba)
            else:
                return drag(self.dragCoefficient, self.A, airdensity[mode], self.vba)

    def force(self):
        liste = [self.force_due_to_gravity, self.drag()]
        for f in self.forces:
            liste.append(f)
        return force_adder(liste)

    def step(self, dt: float, mode = False):
        # if self.pos.y >= self.floor:
        # if self.forces != [] and mode == "racecar":
        #     self.forces = (-g*self.m , Vec(1.54E4 - (self.v.x * 128)))
        self.pos += (self.v * dt)
        self.v += (self.a * dt)
        self.a = self.force() / self.m

        self.vba = self.v - self.wind_speed
        return

    def __repr__(self):
        return f"BALL:\n\tposition: {self.pos}\n\tvelocity: {self.v}\n\tacceleration {self.a}," \
               f"\n\tsize: {self.r} \n\tcolor: {self.color} \n\tradius: {self.r} \n\tforces: {self.forces} \n\t drag: {self.drag()}"


def ball_builder(number_of_balls: int, x: int | tuple[float, float], y: int | tuple[float, float], angle_range: tuple [float, float],
                 maximum_speed: int = 50, acceleration: Vec = Vec(0, 9.81), mass: float = 5, ball_size: int = 0.1, wind_speed: Vec = Vec(), color: tuple[int, int, int] = (255 * random(), 255 * random(), 255 * random())):
    balls = []
    for i in range(number_of_balls):
        if isinstance(x, tuple):
            x_value = randrange(x[0], x[1], 1)
        else:
            x_value = x
        if isinstance(y, tuple):
            y_value = randrange(x[0], x[1], 1)
        else:
            y_value = y
        ball = ball_from_angle(
            Vec(x_value, y_value, 0),
            maximum_speed * random(),
            randrange(angle_range[0]*100, angle_range[1]*100, 1)/100,
            acceleration,
            mass,
            ball_size,
            wind_speed,
            color)
        print(f"ball #{i} = {ball}")
        balls.append(ball)
    return balls


def multi_ball_stepper(balls: list, dt: float = 0.01):
    for i in range(len(balls)):
        balls[i].step(dt)
    return


def ball_from_angle(initial_position: Vec, velocity: float,
                    angle_degrees: float, acceleration: Vec, mass: float = 10, radius: float = 0.1,
                    wind_speed: Vec = Vec(0, 0, 0), color: tuple = (255 * random(), 255 * random(), 255 * random()),
                    force_list: list = [], floor:float = 0, does_drag: bool = True):
    return Ball(initial_position,
                vectors.vectorize(velocity, angle_degrees),
                acceleration,
                mass,
                radius,
                wind_speed,
                color,
                force_list,
                floor,
                does_drag)

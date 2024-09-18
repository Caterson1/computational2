from physics import *
from special_random import *


class GolfBall:
    def __init__(self, pos: Vec = Vec(), velocity: Vec = Vec(10, 10), spinvec: Vec = Vec(),
                 wind_speed: Vec = Vec(0, 0, 0), spin_attrition: float = 0,force_list: list = []):
        self.pos = pos
        self.v = velocity
        self.a = Vec()
        self.m = 0.045
        self.r = 0.021335
        self.magnus_coefficient = 5E-5
        self.attrition = spin_attrition
        self.spin = spinvec
        self.color = (255, 255, 255)
        self.forces = force_list
        self.vba = self.v - wind_speed
        self.wind_speed = wind_speed
        self.A = math.pi * self.r * self.r
        self.dragCoefficient = 0.2
        self.force_due_to_gravity = self.m * g
        self.printedend = False
        self.timer = 0
        self.angel = math.atan(self.v.y/self.v.x)
        self.initialv = mag(self.v)
        self.initial = f"INITIAL VALUES: \n" \
                       f"\tinitial velocity: {mag(self.v) } m/s\n" \
                       f"\tinitial angle: {math.degrees(self.angel) }, \n" \
                       f"\tinitial wind: {self.wind_speed}, \n" \
                       f"\tinitial spin: {self.spin}"
        self.range = False

    def addNormal(self):
        self.forces.append(-1 * self.force_due_to_gravity)

    def add_force(self, *forces):
        for force in forces:
            self.forces.append(force)

    def stop(self):
        if not self.printedend:
            print(f"landed at {self.pos} after {self.timer} seconds\n"
                  f"inital values: {self.initial}")
            self.range = self.pos.x
            self.printedend = True
        self.forces = []
        self.v = Vec()
        return

    def spin_update(self):
        self.spin -= self.attrition
        if self.spin < 0:
            self.spin = 0

    def spin_attrition(self):
        if mag(self.spin)  != 0:
            self.spin.z = (abs(self.spin.z) - self.attrition*dt) * (self.spin.z / abs(self.spin.z))
            if self.spin.z <= 0:
                self.spin.z = 0
        return

    def magnus(self):
        print(self.vba)
        return (self.spin.cross(self.vba))*self.magnus_coefficient

    def drag(self):
        # Fd = -1/2(C{coefficient of drag}A{Front-facing area}p{densityofair}v{speed}v{v.norm}
        return drag(self.dragCoefficient, self.A, self.vba)

    def step(self):
        if self.pos.y < 0:
            self.stop()
            return
        self.timer += dt
        self.pos += (self.v * dt)
        self.v += (self.a * dt)
        self.vba = self.v - self.wind_speed
        self.a = force_adder(self.force_due_to_gravity, self.drag(), self.magnus()) / self.m
        self.spin_attrition()
        return

    def __repr__(self):
        return f"BALL:\n\tposition: {self.pos}\n\tvelocity: {self.v}\n\tacceleration {self.a}," \
               f"\n\tsize: {self.r} \n\tcolor: {self.color} \n\tradius: {self.r} \n\tforces: {self.forces} \n\t drag: {self.drag()}"


def golf_ball_builder(number_of_balls: int,
                      x: int | tuple[float, float],
                      y: int | tuple[float, float],
                      angle: float | tuple[float, float],
                      speed: int | tuple[float, float],
                      spin: Vec = Vec(),
                      mass: float = 5,
                      wind_speed: Vec = Vec(),
                      spin_attrition: float = 0
                      ):
    balls = []
    for i in range(number_of_balls):
        dx = 0
        dy = 0
        dangle = 0
        ds = 0
        if isinstance(x, tuple):
            dx = 1/(x[1] - x[0])
            x = x[0]
        if isinstance(y, tuple):
            dy = 1/(y[1] - y[0])
            y = randrange(y[0], y[1], 1)
        if isinstance(angle, tuple):
            dangle = 1/(angle[1] - angle[0])
            angle = randrange(angle[0], angle[1], 1)
        if isinstance(speed, tuple):
            ds = 1/(speed[1] - speed[0])
            speed = randrange(speed[0], speed[1], 1)
        ball = golf_ball_from_angle(
            Vec(x+dx*i, y+dy*i, 0),
            speed+ds*i,
            angle+dangle*i,
            spin,
            wind_speed,
            mass,
            spin_attrition
            )
        print(f"ball #{i} = {ball}")
        balls.append(ball)
    return balls


def multi_ball_stepper(balls: list, dt: float = 0.01):
    for i in range(len(balls)):
        balls[i].step(dt)
    return


def golf_ball_from_angle(initial_position: Vec, velocity: float,
                         angle_degrees: float, spin: Vec = Vec(),
                         wind_speed: Vec = Vec(0, 0, 0), spin_attrition: float = 0,
                         force_list: list = []):
    return GolfBall(initial_position,
                    vectorize(velocity, angle_degrees),
                    spin,
                    wind_speed,
                    spin_attrition,
                    force_list
                    )


def spin(magnitude: int, direction: str = "backspin"):
    if direction == "backspin":
        return Vec(0, 0, magnitude)
    if direction == "forespin":
        return Vec(0, 0, -magnitude)
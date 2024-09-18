from globals import *


def drag(c, a, v):
    # print(f"{c}, {a}, {p}, {v}, drag force = {(c*a*p*mag(v)**2)*norm(v)}")
    return (c*a*rho*mag(v)**2) * -norm(v) * 1/2


def force_adder(*forces):
    total_force = Vec()
    for force in forces:
        if isinstance(force, Vec):
            total_force += force
        elif isinstance(force, list):
            for f in force:
                total_force += f
        else:
            raise TypeError("force must be type: Vec or List")
    return total_force

import random as rd
import math

import cst


def get_orbit_speed(obj, position_satelite):

    x_cord = position_satelite[0] - obj["position"][0]
    y_cord = position_satelite[1] - obj["position"][1]

    norm = math.sqrt(x_cord**2 + y_cord**2)

    unit_x = -y_cord / norm
    unit_y = x_cord / norm

    v = math.sqrt(cst.G * obj["mass"] / norm)

    vitesse_x = unit_x * v + obj["speed"][0]
    vitesse_y = unit_y * v + obj["speed"][1]
    return [vitesse_x, vitesse_y]


STAR = {
    "name": "Soleil",
    "position": [0, 0],
    "speed": [10, 0],
    "mass": 1.988 * 10**30,
    "radius": 10,
}

PLANETS_LIST = [
    {
        "name": "Terre",
        "position": [149_597_870_700, 0],
        "speed": get_orbit_speed(STAR, [149_597_870_700, 0]),
        "mass": 5.9722 * 10**24,
        "radius": 2,
    },
    {
        "name": "Mercure",
        "position": [0, 57_909_050_000],
        "speed": get_orbit_speed(STAR, [0, 57_909_050_000]),
        "mass": 3.301 * 10**23,
        "radius": 0.8,
    },
]

SATELITES_LIST = [
    {
        "name": "Moon",
        "position": [149_597_870_700 + 385_000_000, 0],
        "speed": get_orbit_speed(PLANETS_LIST[0], [149_597_870_700 + 385_000_000, 0]),
        "mass": 7.346 * 10**22,
        "radius": 0.5,
    },
]

ASTEROIDS_LIST = []
SMALL_ASTEROIDS_LIST = []

# Asteroid belt
asteroid_belt_radius = 1.5 * 149_597_870_700
center_entity = STAR
asteroid_nb = 100
belt_width = 2 * 149_597_870_700 * 0.1 * 0.3 * 0.2
asteroid_max_mass = 10**18
asteroid_min_mass = 10**19
asteroid_min_radius = 0.01
asteroid_max_radius = 0.1

for asteroid_i in range(asteroid_nb):
    circ = rd.uniform(
        asteroid_belt_radius - belt_width / 2, asteroid_belt_radius + belt_width / 2
    )

    x_cord = rd.uniform(-circ, circ)
    y_cord = math.sqrt(circ**2 - x_cord**2) * rd.choice([-1, 1])
    x_cord += center_entity["position"][0]
    y_cord += center_entity["position"][1]

    mass = rd.uniform(asteroid_min_mass, asteroid_max_mass)
    radius = rd.uniform(asteroid_min_radius, asteroid_max_radius)
    ASTEROIDS_LIST.append(
        {
            "position": [x_cord, y_cord],
            "speed": get_orbit_speed(center_entity, [x_cord, y_cord]),
            "mass": mass,
            "radius": radius,
        }
    )


asteroid_belt_radius = 1.5 * 149_597_870_700
center_entity = STAR
asteroid_nb = 750
belt_width = 2 * 149_597_870_700 * 0.1 * 0.3 * 0.2
asteroid_max_mass = 10**15
asteroid_min_mass = 10**16
asteroid_min_radius = 0.01 / 5
asteroid_max_radius = 0.1 / 5

for asteroid_i in range(asteroid_nb):
    circ = rd.uniform(
        asteroid_belt_radius - belt_width / 2, asteroid_belt_radius + belt_width / 2
    )

    x_cord = rd.uniform(-circ, circ)
    y_cord = math.sqrt(circ**2 - x_cord**2) * rd.choice([-1, 1])
    x_cord += center_entity["position"][0]
    y_cord += center_entity["position"][1]

    mass = rd.uniform(asteroid_min_mass, asteroid_max_mass)
    radius = rd.uniform(asteroid_min_radius, asteroid_max_radius)
    SMALL_ASTEROIDS_LIST.append(
        {
            "position": [x_cord, y_cord],
            "speed": get_orbit_speed(center_entity, [x_cord, y_cord]),
            "mass": mass,
            "radius": radius,
        }
    )


asteroid_belt_radius = 2 * 385_000_000
center_entity = PLANETS_LIST[0]
asteroid_nb = 35
belt_width = 2 * 385_000_000 * 0.1 * 0.4 * 0.2
asteroid_max_mass = 10**17
asteroid_min_mass = 10**18
asteroid_min_radius = 0.01 / 2
asteroid_max_radius = 0.1 / 2

for asteroid_i in range(asteroid_nb):
    circ = rd.uniform(
        asteroid_belt_radius - belt_width / 2, asteroid_belt_radius + belt_width / 2
    )

    x_cord = rd.uniform(-circ, circ)
    y_cord = math.sqrt(circ**2 - x_cord**2) * rd.choice([-1, 1])
    x_cord += center_entity["position"][0]
    y_cord += center_entity["position"][1]

    mass = rd.uniform(asteroid_min_mass, asteroid_max_mass)
    radius = rd.uniform(asteroid_min_radius, asteroid_max_radius)
    ASTEROIDS_LIST.append(
        {
            "position": [x_cord, y_cord],
            "speed": get_orbit_speed(center_entity, [x_cord, y_cord]),
            "mass": mass,
            "radius": radius,
        }
    )


asteroid_belt_radius = 2 * 385_000_000
center_entity = PLANETS_LIST[0]
asteroid_nb = 200
belt_width = 2 * 385_000_000 * 0.1 * 0.4 * 0.2
asteroid_max_mass = 10**15
asteroid_min_mass = 10**16
asteroid_min_radius = 0.01 / 5
asteroid_max_radius = 0.1 / 5

for asteroid_i in range(asteroid_nb):
    circ = rd.uniform(
        asteroid_belt_radius - belt_width / 2, asteroid_belt_radius + belt_width / 2
    )

    x_cord = rd.uniform(-circ, circ)
    y_cord = math.sqrt(circ**2 - x_cord**2) * rd.choice([-1, 1])
    x_cord += center_entity["position"][0]
    y_cord += center_entity["position"][1]

    mass = rd.uniform(asteroid_min_mass, asteroid_max_mass)
    radius = rd.uniform(asteroid_min_radius, asteroid_max_radius)
    SMALL_ASTEROIDS_LIST.append(
        {
            "position": [x_cord, y_cord],
            "speed": get_orbit_speed(center_entity, [x_cord, y_cord]),
            "mass": mass,
            "radius": radius,
        }
    )


asteroid_belt_radius = 2 * 385_000_000 / 10
center_entity = PLANETS_LIST[1]
asteroid_nb = 200
belt_width = 2 * 385_000_000 * 0.1 * 0.4 * 0.1 * 0.2
asteroid_max_mass = 10**15
asteroid_min_mass = 10**16
asteroid_min_radius = 0.01 / 5
asteroid_max_radius = 0.1 / 5

for asteroid_i in range(asteroid_nb):
    circ = rd.uniform(
        asteroid_belt_radius - belt_width / 2, asteroid_belt_radius + belt_width / 2
    )

    x_cord = rd.uniform(-circ, circ)
    y_cord = math.sqrt(circ**2 - x_cord**2) * rd.choice([-1, 1])
    x_cord += center_entity["position"][0]
    y_cord += center_entity["position"][1]

    mass = rd.uniform(asteroid_min_mass, asteroid_max_mass)
    radius = rd.uniform(asteroid_min_radius, asteroid_max_radius)
    SMALL_ASTEROIDS_LIST.append(
        {
            "position": [x_cord, y_cord],
            "speed": get_orbit_speed(center_entity, [x_cord, y_cord]),
            "mass": mass,
            "radius": radius,
        }
    )

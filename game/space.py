import math
import random
import uuid as uuidGEN
import numpy as np

from game.entity import Entity
from game.gravity_entities import Planet, Star, Satelite, Asteroid
from game.physics import Position, Vitesse, Force


from structb.bulle import BubbleTree, Bubble

import cst
from game.spatial_objects import (
    STAR,
    PLANETS_LIST,
    SATELITES_LIST,
    ASTEROIDS_LIST,
    SMALL_ASTEROIDS_LIST,
)


class Space:

    def __init__(self):

        self.entities = {}
        self.gravity_generators = []

        self.planets = []

        self.init_solar_system()

    def init_solar_system(self):
        # 4 niveau : Etoile (centre du système), planète (divisé une bubble étendue et une bubble proche, 2 niveaux), astéroïdes générant de la gravité
        self.star = Star(
            position=Position.from_list(STAR["position"]),
            vitesse=Vitesse.from_list(STAR["speed"]),
            mass=STAR["mass"],
            radius=STAR["radius"],
        )
        self.genesis_bubble = BubbleTree(
            self.star.position, cst.SOLAR_SYSTEM_BUBBLE_RADIUS
        )
        self.genesis_bubble.link_an_entity(self.star)
        self.register_new_entity(self.star)
        self.init_planets()
        self.init_satelites()
        self.init_asteroids()

    def init_planets(self):
        for planet in PLANETS_LIST:
            planetobj = Planet(
                position=Position.from_list(planet["position"]),
                vitesse=Vitesse.from_list(planet["speed"]),
                mass=planet["mass"],
                name=planet["name"],
                radius=planet["radius"],
            )
            planet_bubble_large = BubbleTree(
                planetobj.position, cst.PLANET_LARGE_BUBBLE_RADIUS
            )
            planet_bubble_small = BubbleTree(
                planetobj.position, cst.PLANET_SMALL_BUBBLE_RADIUS
            )
            planet_bubble_large.link_an_entity(planetobj)
            planet_bubble_small.link_an_entity(planetobj)
            self.genesis_bubble.add_bubble_to_bubble_tree(planet_bubble_large)
            self.genesis_bubble.add_bubble_to_bubble_tree(planet_bubble_small)

            self.planets.append(planetobj)
            self.register_new_entity(planetobj)

    def init_satelites(self):
        for satelite in SATELITES_LIST:
            sateliteobj = Satelite(
                position=Position.from_list(satelite["position"]),
                vitesse=Vitesse.from_list(satelite["speed"]),
                mass=satelite["mass"],
                radius=satelite["radius"],
            )
            satelite_bubble = BubbleTree(
                sateliteobj.position, cst.PLANET_SMALL_BUBBLE_RADIUS
            )
            satelite_bubble.link_an_entity(sateliteobj)
            self.genesis_bubble.add_bubble_to_bubble_tree(satelite_bubble)

            self.register_new_entity(sateliteobj)

    def init_asteroids(self):
        for asteroid in ASTEROIDS_LIST:
            asteroidobj = Asteroid(
                position=Position.from_list(asteroid["position"]),
                vitesse=Vitesse.from_list(asteroid["speed"]),
                mass=asteroid["mass"],
                radius=asteroid["radius"],
            )
            asteroid_bubble = BubbleTree(
                asteroidobj.position, cst.ASTEROID_BUBBLE_RADIUS
            )
            asteroid_bubble.link_an_entity(asteroidobj)
            self.genesis_bubble.add_bubble_to_bubble_tree(asteroid_bubble)

            self.register_new_entity(asteroidobj)

        for small_asteroid in SMALL_ASTEROIDS_LIST:
            small_asteroidobj = Asteroid(
                position=Position.from_list(small_asteroid["position"]),
                vitesse=Vitesse.from_list(small_asteroid["speed"]),
                mass=small_asteroid["mass"],
                radius=small_asteroid["radius"],
            )

            self.register_new_entity(small_asteroidobj)

    def get_distances_from_point(self, x, y):
        """Renvoie une liste de planètes avec leur distance par rapport à un point donné."""
        distances = [(planet.name, planet.distance_to(x, y)) for planet in self.planets]
        return sorted(distances, key=lambda item: item[1])

    def register_new_entity(self, entity: Entity, uuid=0):
        if not uuid:
            entity_id = str(uuidGEN.uuid4())
        else:
            entity_id = str(uuid)
        entity.set_uuid(entity_id)
        self.entities[entity_id] = entity
        if entity.generate_gravity:
            self.register_a_gravity_generator(entity)
        self.genesis_bubble.bubble_an_entity(entity)
        return entity_id

    def register_a_gravity_generator(self, entity):
        self.gravity_generators.append(entity)

    def compute_gravity_for_all(self):
        grav_array = []
        for grav_gen in self.gravity_generators:
            grav_array.append(grav_gen.position.listify())

        grav_array = np.array(grav_array)

        for entity_uuid in self.entities:
            self.compute_gravity(entity_uuid, grav_array.copy())

    def compute_gravity(self, entity_uuid, grav_array: np.array):
        entity = self.entities[entity_uuid]  # type: Entity
        dirarray = grav_array - np.array([entity.position.listify()])
        distarray = np.linalg.norm(dirarray, axis=1)
        distmask = distarray == 0
        distarray += distmask  # remplace les 0 par des 1, pas d'importance puisque si deux obj sont l'un dans l'autre on ne veut pas de gravité

        dirarray = dirarray / distarray[:, np.newaxis]
        distarray **= 2

        massarray = []
        for grav_gen in self.gravity_generators:
            massarray.append(grav_gen.mass)

        massarray = np.array(massarray)

        farray = ((massarray / distarray) * cst.G * entity.mass)[
            :, np.newaxis
        ] * dirarray
        final_force = Force.from_list(list(np.sum(farray, axis=0)))
        entity.add_for_next_acceleration_apply_forces(final_force)
        # print("Final Force on", entity.name, final_force)
        return True

    def draw_initial_bubble_tree(self):
        import matplotlib.pyplot as plt
        from matplotlib.patches import Circle

        fig, ax = plt.subplots()
        ax.set_xlim(-(149_597_870_700 * 10), 1149_597_870_700 * 10)
        ax.set_ylim(-(149_597_870_700 * 10), 149_597_870_700 * 10)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title("Space representation of the Star Bubble-Tree")
        ax.set_xlabel("X axis")
        ax.set_ylabel("Y axis")

        self.genesis_bubble.draw(ax)

        for entity in self.entities.values():
            circle = Circle(
                (entity.position.x, entity.position.y),
                1_000_000,
                fill=True,
                color="black",
            )
            ax.add_patch(circle)

        plt.show()

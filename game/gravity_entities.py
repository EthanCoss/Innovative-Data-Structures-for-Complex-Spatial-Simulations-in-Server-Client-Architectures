from game.entity import Entity
import math

from game.physics import Position, Vitesse, Force

import game.shape as shape

import cst


class Planet(Entity):

    def __init__(
        self,
        position: Position,
        vitesse: Vitesse,
        mass: float = 0,
        has_drag: bool = False,
        base_drag_force: Force = Force(0, 0),
        radius: float = 1,
        name: str = "Unnamed Planet",
    ):
        super().__init__(
            position=position,
            vitesse=vitesse,
            mass=mass,
            has_drag=has_drag,
            base_drag_force=base_drag_force,
            can_exceed_walls=False,
            can_move=True,
            generate_gravity=True,
        )
        self.name = name
        self.shape_init(radius)

    def shape_init(self, radius):
        self.set_shape(shape.Circle(radius=radius))

    def jsonify(self):
        dic = super().jsonify()
        dic[self.uuid].update(
            {
                cst.TYPE: cst.PLANET_TYPE,
                cst.PLANET_NAME: self.name,
                cst.RADIUS: self.shape.radius,
            }
        )

        return dic

    @staticmethod
    def create_from_json(planet_json):
        return Planet(
            position=Position.from_list(planet_json[cst.POSITION]),
            vitesse=Vitesse.from_list(planet_json[cst.SPEED]),
            mass=planet_json[cst.MASS],
            name=planet_json[cst.PLANET_NAME],
            radius=planet_json[cst.RADIUS],
        )

    def __str__(self):
        return f"Planète {self.name} à ({self.position.x}, {self.position.y}) ---- vitesse : ({self.vitesse.x}, {self.vitesse.y})"


class Star(Entity):

    def __init__(
        self,
        position: Position,
        vitesse: Vitesse,
        mass: float = 0,
        has_drag: bool = False,
        base_drag_force: Force = Force(0, 0),
        radius: float = 1,
    ):
        super().__init__(
            position=position,
            vitesse=vitesse,
            mass=mass,
            has_drag=has_drag,
            base_drag_force=base_drag_force,
            can_exceed_walls=False,
            can_move=True,
            generate_gravity=True,
        )
        self.shape_init(radius)

    def shape_init(self, radius):
        self.set_shape(shape.Circle(radius=radius))

    def jsonify(self):
        dic = super().jsonify()
        dic[self.uuid].update(
            {
                cst.TYPE: cst.STAR_TYPE,
                cst.RADIUS: self.shape.radius,
            }
        )

        return dic

    @staticmethod
    def create_from_json(star_json):
        return Star(
            position=Position.from_list(star_json[cst.POSITION]),
            vitesse=Vitesse.from_list(star_json[cst.SPEED]),
            mass=star_json[cst.MASS],
            radius=star_json[cst.RADIUS],
        )


class Satelite(Entity):

    def __init__(
        self,
        position: Position,
        vitesse: Vitesse,
        mass: float = 0,
        has_drag: bool = False,
        base_drag_force: Force = Force(0, 0),
        radius: float = 1,
    ):
        super().__init__(
            position=position,
            vitesse=vitesse,
            mass=mass,
            has_drag=has_drag,
            base_drag_force=base_drag_force,
            can_exceed_walls=False,
            can_move=True,
            generate_gravity=True,
        )
        self.shape_init(radius)

    def shape_init(self, radius):
        self.set_shape(shape.Circle(radius=radius))

    def jsonify(self):
        dic = super().jsonify()
        dic[self.uuid].update(
            {
                cst.TYPE: cst.SATELITE_TYPE,
                cst.RADIUS: self.shape.radius,
            }
        )

        return dic

    @staticmethod
    def create_from_json(satelite_json):
        return Satelite(
            position=Position.from_list(satelite_json[cst.POSITION]),
            vitesse=Vitesse.from_list(satelite_json[cst.SPEED]),
            mass=satelite_json[cst.MASS],
            radius=satelite_json[cst.RADIUS],
        )


class Asteroid(Entity):

    def __init__(
        self,
        position: Position,
        vitesse: Vitesse,
        mass: float = 0,
        has_drag: bool = False,
        base_drag_force: Force = Force(0, 0),
        radius: float = 1,
    ):
        super().__init__(
            position=position,
            vitesse=vitesse,
            mass=mass,
            has_drag=has_drag,
            base_drag_force=base_drag_force,
            can_exceed_walls=False,
            can_move=True,
            generate_gravity=True,
        )
        self.shape_init(radius)

    def shape_init(self, radius):
        self.set_shape(shape.Circle(radius=radius))

    def jsonify(self):
        dic = super().jsonify()
        dic[self.uuid].update(
            {
                cst.TYPE: cst.ASTEROID_TYPE,
                cst.RADIUS: self.shape.radius,
            }
        )

        return dic

    @staticmethod
    def create_from_json(asteroid_json):
        return Asteroid(
            position=Position.from_list(asteroid_json[cst.POSITION]),
            vitesse=Vitesse.from_list(asteroid_json[cst.SPEED]),
            mass=asteroid_json[cst.MASS],
            radius=asteroid_json[cst.RADIUS],
        )

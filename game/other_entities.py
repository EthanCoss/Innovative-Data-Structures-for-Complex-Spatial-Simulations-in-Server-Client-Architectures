from game.entity import Entity
import math

from game.physics import Position, Vitesse, Force

import game.shape as shape

import cst


class SmallAsteroid(Entity):

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
            generate_gravity=False,
        )
        self.shape_init(radius)

    def shape_init(self, radius):
        self.set_shape(shape.Circle(radius=radius))

    def jsonify(self):
        dic = super().jsonify()
        dic[self.uuid].update(
            {
                cst.TYPE: cst.SMALL_ASTEROID_TYPE,
                cst.RADIUS: self.shape.radius,
            }
        )

        return dic

    @staticmethod
    def create_from_json(small_asteroid_json):
        return SmallAsteroid(
            position=Position.from_list(small_asteroid_json[cst.POSITION]),
            vitesse=Vitesse.from_list(small_asteroid_json[cst.SPEED]),
            mass=small_asteroid_json[cst.MASS],
            radius=small_asteroid_json[cst.RADIUS],
        )

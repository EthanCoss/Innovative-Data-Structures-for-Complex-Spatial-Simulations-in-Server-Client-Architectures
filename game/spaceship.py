from game.entity import Entity
from game.physics import Vitesse, Position, Acceleration, Force
import game.shape as shape

from game.shape import Circle

import cst

import random


class Spaceship(Entity):

    def __init__(
        self,
        position: Position,
        vitesse: Vitesse,
        mass: float = cst.SPACESHIP_MASS,
        has_drag: bool = False,
        base_drag_force: Force = Force(0, 0),
    ):
        super().__init__(
            position, vitesse, mass, has_drag, base_drag_force, True, False
        )
        self.shape_init()

    def shape_init(self):
        self.set_shape(shape.Rectangle(width=cst.SPACE_WIDTH, height=cst.SPACE_HEIGHT))

    def jsonify(self):
        dic = super().jsonify()
        dic[self.uuid].update({"type": cst.SPACESHIP_TYPE})
        return dic

    def __str__(self):
        dic = super().jsonify()
        dic[self.uuid].update({"type": cst.SPACESHIP_TYPE})
        return str(dic)

    def booster_tick(self, force, dt):
        pass

    @staticmethod
    def create_from_json(spaceship_json):
        return Spaceship(
            position=Position.from_list(spaceship_json[cst.POSITION]),
            vitesse=Vitesse.from_list(spaceship_json[cst.SPEED]),
            mass=spaceship_json[cst.MASS],
        )

    @staticmethod
    def spawn_new_spaceship_at_random(
        mass: float = cst.SPACESHIP_MASS,
        has_drag: bool = False,
        base_drag_force: Force = Force(0, 0),
    ):
        return Spaceship(
            position=Position(
                random.randrange(
                    -cst.SPACESHIP_RANDOM_POS_RANGE_X, cst.SPACESHIP_RANDOM_POS_RANGE_X
                ),
                random.randrange(
                    -cst.SPACESHIP_RANDOM_POS_RANGE_Y, cst.SPACESHIP_RANDOM_POS_RANGE_Y
                ),
            ),
            vitesse=Vitesse(
                random.randrange(
                    -cst.SPACESHIP_RANDOM_SPEED_RANGE_X,
                    cst.SPACESHIP_RANDOM_SPEED_RANGE_X,
                ),
                random.randrange(
                    -cst.SPACESHIP_RANDOM_SPEED_RANGE_Y,
                    cst.SPACESHIP_RANDOM_SPEED_RANGE_Y,
                ),
            ),
            mass=mass,
            has_drag=has_drag,
            base_drag_force=base_drag_force,
        )

    def update_from_json(self, entity_json):
        return super().update_from_json(entity_json)

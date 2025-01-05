from game.physics import Vitesse, Position, Acceleration, Force
from game.shape import Circle, Rectangle

from master_variables import colision_counter

import cst


class Entity:
    def __init__(
        self,
        position: Position,
        vitesse: Vitesse,
        mass: float,
        has_drag: bool = False,
        base_drag_force: Force = Force(0, 0),
        can_move: bool = False,
        can_exceed_walls=False,
        generate_gravity=False,
    ):
        self.position = position
        self.vitesse = vitesse
        self.can_move = can_move
        self.can_exceed_walls = can_exceed_walls
        self.mass = mass
        self.has_drag = has_drag
        self.base_drag_force = base_drag_force
        self.for_next_acceleration_apply_forces = []
        self.generate_gravity = generate_gravity
        self.has_shape = False
        self.shape = None
        self.uuid = None
        self.bubble = None

    def move(self, dt, check_colision=False, colisions_list=[]):
        self.position.change_position(self.vitesse, dt)
        if check_colision:
            colision_counter["colisions_check_number"] += len(colisions_list)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def link_bubble(self, bubble):
        self.bubble = bubble

    def apply_forces(self, dt: float, reset_forces: bool = True):
        acceleration = Acceleration(self.for_next_acceleration_apply_forces, self.mass)
        self.vitesse.apply_acceleration(acceleration, dt)
        if reset_forces:
            self.for_next_acceleration_apply_forces = []

    def add_for_next_acceleration_apply_forces(self, force):
        self.for_next_acceleration_apply_forces.append(force)

    def set_shape(self, shape):
        self.shape = shape
        self.has_shape = True

    def remove_shape(self):
        self.shape = None
        self.has_shape = False

    def jsonify(self):
        return {
            self.uuid: {
                cst.POSITION: self.position.listify(),
                cst.SPEED: self.vitesse.listify(),
                cst.MASS: self.mass,
                cst.FORCES: [
                    force.listify() for force in self.for_next_acceleration_apply_forces
                ],
            }
        }

    def update_from_json(self, entity_json):
        self.position = Position.from_list(entity_json[cst.POSITION])
        self.vitesse = Vitesse.from_list(entity_json[cst.SPEED])
        self.mass = entity_json[cst.MASS]
        self.for_next_acceleration_apply_forces = [
            Force.from_list(force) for force in entity_json[cst.FORCES]
        ]
        return True

    def __str__(self):
        return str(self.jsonify)

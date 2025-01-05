import math
import game.fonctions as ft


class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def incr_x(self, x_add: float):
        self.x += x_add
        return self

    def incr_y(self, y_add: float):
        self.y += y_add
        return self

    def multi(self, scalar: float):
        self.x = self.x * scalar
        self.y = self.y * scalar
        return self

    def new_direction_from_coordinates(
        self, from_x: float, from_y: float, to_x: float, to_y: float
    ):
        norme = self.get_norme()
        self.x = to_x - from_x
        self.y = to_y - from_y
        self.set_new_norme(norme)
        return self

    def set_new_norme(self, new_norme: float):
        self.multi((1 / self.get_norme()) * new_norme)
        return self

    def get_norme(self):
        return ft.distance(self.x, self.y)

    def listify(self):
        return [self.x, self.y]

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Force(Vector2D):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def copy(self):
        return Force(self.x, self.y)

    @staticmethod
    def from_list(xy_list):
        return Force(xy_list[0], xy_list[1])


class Acceleration(Vector2D):
    def __init__(self, forces_list: list, mass: float):
        acc_x = 0
        acc_y = 0
        for force in forces_list:
            acc_x += force.x / mass
            acc_y += force.y / mass
        super().__init__(acc_x, acc_y)


class Vitesse(Vector2D):
    def __init__(self, v_x: float, v_y: float):
        super().__init__(v_x, v_y)

    def apply_acceleration(self, acceleration: Acceleration, dt):
        self.incr_x(acceleration.x * dt)
        self.incr_y(acceleration.y * dt)

    @staticmethod
    def from_list(xy_list):
        return Vitesse(xy_list[0], xy_list[1])


class Position(Vector2D):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    def change_position(self, vitesse: Vitesse, dt: float):
        self.incr_x(vitesse.x * dt)
        self.incr_y(vitesse.y * dt)

    def distance(self, position):
        return math.sqrt((self.x - position.x) ** 2 + (self.y - position.y) ** 2)

    @staticmethod
    def from_list(xy_list):
        return Position(xy_list[0], xy_list[1])

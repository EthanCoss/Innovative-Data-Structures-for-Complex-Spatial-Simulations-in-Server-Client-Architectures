import time
import threading

from game.spaceship import Spaceship
from game.physics import Position, Vitesse, Acceleration
from game.space import Space

from connexion.json_translate import JsonManCli

import cst


from master_variables import debug_mode


class Client:
    def __init__(self):
        self.space = Space()
        self.spaceship = None
        self.has_spawned = False
        self.last_update = time.time()
        self.json_manager = JsonManCli(self)
        self.uuid = None

    def start(self):
        self.update_loop()

    def update_loop(self):
        while True:
            start_time = time.time()
            self.update()
            time_till_next_update = start_time + 1 / cst.REFRESH_RATE - time.time()
            if time_till_next_update > 0:
                time.sleep(time_till_next_update)

    def init_my_spaceship_from_json(self, uuid, spaceship_json):
        self.spaceship = Spaceship.create_from_json(spaceship_json=spaceship_json)
        self.space.register_new_entity(self.spaceship, uuid)
        self.has_spawned = True
        if debug_mode:
            print("Spawned my spaceship :", self.spaceship.jsonify())

    def set_my_uuid(self, uuid):
        self.uuid = uuid
        self.json_manager.set_my_uuid(uuid)

    def update(self):
        dt, self.last_update = (
            time.time() - self.last_update
        ) * cst.DT_MULTIPLICATOR, time.time()
        for entity in self.space.entities.values():
            entity.apply_forces(dt, reset_forces=False)
            entity.move(dt)

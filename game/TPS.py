from game.space import Space
import time
import json

from master_variables import *

from game.spaceship import Spaceship
from connexion.client_con import Client_Con
from game.entity import Entity

import cst


class TPS:

    def __init__(self, space: Space):
        self.space = space
        self.last_tick_time = time.time()

    def TPS_loop(self):
        TPS_log_time = []
        sleepfor = []
        tick_count = 0
        start_time = time.time()
        while True:
            tick_count += 1
            if debug_TPS:
                TPS_log_time.append(time.time() - start_time)
                if tick_count % cst.TPS == 0 and len(TPS_log_time) > cst.TPS:
                    print(
                        "Average tick/s over the last",
                        cst.TPS,
                        " ticks :",
                        cst.TPS / sum(TPS_log_time[-cst.TPS :]),
                    )
            if debug_colisions:  # and tick_count % cst.TPS == 0:
                print(colision_counter["colisions_check_number"])
            start_time = time.time()
            self.do_a_tick()
            time_till_next_update = start_time + 1 / cst.TPS - time.time()
            sleepfor.append(time_till_next_update)
            if time_till_next_update > 0:
                time.sleep(time_till_next_update)

    def do_a_tick(self):
        current_time = time.time()
        dt = (time.time() - self.last_tick_time) * cst.DT_MULTIPLICATOR
        self.last_tick_time = current_time
        for client_con in client_dico.values():
            client_con.json_man_serv.new_round()
        self.treat_data()
        self.internal_tick(dt)
        if log_planets_trajectories:
            self.log_planets_trajectories()
        self.build_report_to_all()
        self.send_data_to_all()

    def treat_data(self):
        global client_last_data_dico_flash
        client_last_data_dico_flash = client_last_data_dico.copy()
        if debug_listen:
            print("Current client_last_data_dico :", client_last_data_dico_flash)
        for client_uuid in client_last_data_dico:
            client_last_data_dico[client_uuid] = ""
            client_dico[client_uuid].json_man_serv.json_base()

        for client_uuid in client_last_data_dico_flash.keys():
            if (
                client_last_data_dico_flash[client_uuid] is None
                or client_last_data_dico_flash[client_uuid] == ""
            ):
                client_con = client_dico[client_uuid]
                continue
            client_last_data_dico_flash[client_uuid] = json.loads(
                client_last_data_dico_flash[client_uuid]
            )
            try:
                self.update_client(
                    client_uuid, client_last_data_dico_flash[client_uuid]
                )
            except Exception as e:
                print(
                    "Error during the update of",
                    client_uuid,
                    ":",
                    Exception.with_traceback(e),
                )

    def update_client(self, uuid, client_flash_data):
        client_con = client_dico[uuid]  # type: Client_Con

        if not set([cst.ACTIONS, cst.ENTITIES, cst.QUERRIES]) <= set(
            client_flash_data.keys()
        ):
            return

        self.entities_on(client_con, client_flash_data[cst.ENTITIES])
        self.actions_on(client_con, client_flash_data[cst.ACTIONS])
        self.querries_on(client_con, client_flash_data[cst.QUERRIES])

    def entities_on(self, client_con: Client_Con, entities_data: dict):
        if client_con.has_spawned and client_con.spaceship.uuid in entities_data.keys():
            self.space.entities[client_con.spaceship.uuid].update_from_json(
                entities_data[client_con.spaceship.uuid]
            )

    def actions_on(self, client_con: Client_Con, actions_data):
        pass

    def querries_on(self, client_con: Client_Con, querries_data):

        for querry in querries_data.keys():
            match querry:
                case cst.SPAWN_NEW_SPACESHIP:
                    new_spaceship = Spaceship.spawn_new_spaceship_at_random(
                        cst.SPACESHIP_MASS
                    )
                    self.space.register_new_entity(new_spaceship)
                    client_con.set_spaceship(new_spaceship)
                    client_con.json_man_serv.spawned_spaceship_response(new_spaceship)

    def internal_tick(self, dt: float):
        for entity_uuid in self.space.entities:
            entity = self.space.entities[entity_uuid]  # type: Entity
            if debug_entities:
                print(entity)
            entity.apply_forces(dt)
            entity.move(dt, check_colision=True, colisions_list=entity.bubble.entities)

        self.space.compute_gravity_for_all()

    def build_report_to_all(self):
        entities_dic = {}
        for entity in self.space.entities.values():
            entities_dic.update(entity.jsonify())
        for client_con in client_dico.values():
            if not client_con.uuid in client_last_data_dico_flash.keys():
                continue
            if client_con.is_connexion_active:
                print(client_con.json_man_serv.current_json)
                client_con.json_man_serv.add_entities(entities_dic)

    def send_data_to_all(self):
        for client_con in client_dico.values():
            client_con.send_data()

    def log_planets_trajectories(self):
        for planet in self.space.gravity_generators:
            with open("trajectoires/" + planet.name + "/x.txt", "a") as file:
                file.write(str(planet.position.x) + "\n")
            with open("trajectoires/" + planet.name + "/y.txt", "a") as file:
                file.write(str(planet.position.y) + "\n")

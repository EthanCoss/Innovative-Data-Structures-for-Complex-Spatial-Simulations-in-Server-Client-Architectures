import socket
import time
import threading
import json
import cst

from game.spaceship import Spaceship
from client import Client
from game.entity import Entity
from game.gravity_entities import Star, Planet, Satelite, Asteroid

from master_variables import *


class ClientConnexionMan:
    def __init__(self, client):
        self.client = client  # type: Client
        self.sock = None
        self.uuid = None
        self.is_connected = False
        self.send_connexion = False
        self.receive_connexion = False
        self.sock_id = 0

    def initiate_connexion(self, host, port):
        self.host = host
        self.port = port
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, self.port))
                sock.send("new".encode())
                data = sock.recv(cst.MAX_RECV_BYTES).decode()
                if data != "new":
                    continue
                uuid = sock.recv(cst.MAX_RECV_BYTES).decode()
                if uuid:
                    self.sock = sock
                    self.set_my_uuid(uuid)

                print("Connexion established :", self.uuid)

                main_loop_thread = threading.Thread(target=self.main_loop)
                main_loop_thread.start()
                main_loop_thread.join()
            except:
                print("Unable to reach the server")
                time.sleep(1)

    def sock_send_loop(self, sock_id):

        while not self.client.has_spawned:
            try:
                self.send_connexion = True
                self.client.json_manager.new_round()
                if not self.client.has_spawned:
                    if debug_mode:
                        print("Asking to spawn")
                    self.client.json_manager.ask_spawn()
                self.sock.send(self.client.json_manager.stringify().encode())
            except Exception as e:
                print("Error sending")
                if debug_mode:
                    print(e)
                self.send_connexion = False
                return
            finally:
                time.sleep(2)

        while self.sock_id == sock_id:
            start_time = time.time()
            try:
                self.build_report_to_server()
                if debug_listen:
                    print("Sending to server :", self.client.json_manager.current_json)
                self.sock.send(self.client.json_manager.stringify().encode())
                self.send_connexion = True
            except:
                print("Error sending")
                self.send_connexion = False
                return
            time_till_next_send = start_time + 1 / cst.TPS - time.time()
            if time_till_next_send > 0:
                time.sleep(time_till_next_send)

    def sock_receive_loop(self, sock_id):
        while self.sock_id == sock_id:
            try:
                data = self.sock.recv(cst.MAX_RECV_BYTES).decode()
                if debug_listen:
                    print("Client Roger :", data)
                self.receive_connexion = True
                self.update_client(data)
            except Exception as e:
                print("Error receiving", e.with_traceback())
                self.receive_connexion = False
                return

    def main_loop(self):

        thread_send = threading.Thread(target=self.sock_send_loop, args=[self.sock_id])
        thread_receive = threading.Thread(
            target=self.sock_receive_loop, args=[self.sock_id]
        )
        self.send_connexion = True
        self.receive_connexion = True
        thread_send.start()
        thread_receive.start()

        while True:
            if (not self.send_connexion) or (not self.receive_connexion):

                try:
                    self.sock_id += 1
                    r = self.repair_connexion()
                    if r:
                        thread_send = threading.Thread(
                            target=self.sock_send_loop, args=[self.sock_id]
                        )
                        thread_receive = threading.Thread(
                            target=self.sock_receive_loop, args=[self.sock_id]
                        )
                        self.send_connexion = True
                        self.receive_connexion = True
                        thread_send.start()
                        thread_receive.start()
                        print("Tunnel running")
                    else:
                        print("Unexpected answer while repairing connexion")
                except:
                    print("Unable to repair connexion")

            time.sleep(1)

    def repair_connexion(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send(self.uuid.encode())
        data = sock.recv(cst.MAX_RECV_BYTES).decode()
        if data == "uuid not recognised":
            data = sock.recv(cst.MAX_RECV_BYTES).decode()
            self.set_my_uuid(data)
            print("Reseting uuid:", data)
            self.client.has_spawned = False
            return True
        if data == "uuid recognised":
            data = sock.recv(cst.MAX_RECV_BYTES).decode()
            if data != self.uuid:
                return False
            else:
                return True

    def set_my_uuid(self, uuid):
        self.uuid = str(uuid)
        self.client.set_my_uuid(uuid)

    def update_client(self, data):
        data = json.loads(data)

        self.client.json_manager.new_round()

        self.treat_responses(data[cst.RESPONSE])
        self.treat_entities(data[cst.ENTITIES])
        self.treat_action(data[cst.ACTIONS])
        self.treat_querries(data[cst.QUERRIES])
        print(self.client.spaceship)

    def treat_responses(self, responses_data):
        for response in responses_data.keys():
            match response:
                case cst.SPAWN_NEW_SPACESHIP:
                    self.client.init_my_spaceship_from_json(
                        list(responses_data[response].keys())[0],
                        responses_data[response][
                            list(responses_data[response].keys())[0]
                        ],
                    )

    def treat_entities(self, entities_data):
        for entity_uuid in entities_data:
            self.treat_entity_from_json(entity_uuid, entities_data[entity_uuid])

    def treat_action(self, actions_data):
        pass

    def treat_querries(self, querries_data):
        pass

    def build_report_to_server(self):
        self.client.json_manager.new_round()
        self.client.json_manager.add_spaceship(self.client.spaceship)

    def treat_entity_from_json(self, entity_uuid, entity_json):
        if not entity_uuid in self.client.space.entities:
            self.create_new_entity_from_json(entity_uuid, entity_json)
        else:
            self.update_entity_from_json(entity_uuid, entity_json)

    def create_new_entity_from_json(self, entity_uuid, entity_json):
        match entity_json[cst.TYPE]:
            case cst.SPACESHIP_TYPE:
                entity = Spaceship.create_from_json(entity_json)
            case cst.PLANET_TYPE:
                entity = Planet.create_from_json(entity_json)
            case cst.STAR_TYPE:
                entity = Star.create_from_json(entity_json)
            case cst.SATELITE_TYPE:
                entity = Satelite.create_from_json(entity_json)
            case cst.ASTEROID_TYPE:
                entity = Asteroid.create_from_json(entity_json)

        self.client.space.register_new_entity(entity, entity_uuid)

    def update_entity_from_json(self, entity_uuid, entity_json):
        entity = self.client.space.entities[entity_uuid]  # type: Entity
        entity.update_from_json(entity_json)

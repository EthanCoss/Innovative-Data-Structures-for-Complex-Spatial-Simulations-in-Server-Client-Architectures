import threading
import time
import socket

from connexion.json_translate import JsonManServ

from master_variables import *


class Client_Con:
    def __init__(self, uuid):
        self.uuid = uuid
        self.current_thread_id = 0
        self.is_connexion_active = False
        self.client_address = None
        self.client_socket = None
        self.last_update_time = None
        self.creation_time = time.time()
        self.last_connexion_time = time.time()
        self.last_update_time = None
        self.json_man_serv = JsonManServ(self)
        self.has_spawned = False
        self.spaceship = None

    def set_new_client_socket(self, client_socket, client_address):
        self.client_address = client_address
        self.client_socket = client_socket
        self.last_connexion_time = time.time()
        self.current_thread_id += 1
        loop_thread = threading.Thread(
            target=self.run_loop, args=[self.current_thread_id, client_socket]
        )
        loop_thread.start()

    def run_loop(self, thread_id, client_socket):

        while thread_id == self.current_thread_id:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    print("Connexion fermée par le client :", self.uuid)
                    client_socket.close()
                    self.is_connexion_active = False
                    return
                else:
                    self.last_update_time = time.time()
                    client_last_data_dico[self.uuid] = data
                    self.is_connexion_active = True
                    if debug_listen:
                        print("Roger", self.uuid, data)

            except Exception as e:
                print(f"Erreur : {e}")
                try:
                    client_socket.close()
                except:
                    pass
                self.is_connexion_active = False
                return
        self.is_connexion_active = False

    def send_data(self):
        if not self.is_connexion_active:
            return False
        try:
            if debug_listen:
                print(
                    "Sending to", self.uuid, self.json_man_serv.current_json
                )  # .stringify())
            self.client_socket.send(self.json_man_serv.stringify().encode())
        except:
            print("Error while sending last data to", self.uuid)
            print("Data :", self.json_man_serv.stringify())
        return True

    def set_spaceship(self, spaceship):
        self.spaceship = spaceship
        self.has_spawned = True

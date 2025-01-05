import threading
import time
import socket
import uuid

from game.space import Space
from connexion.client_con import Client_Con
import cst

from master_variables import *

host = cst.HOST
port = cst.PORT


def listener():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Liaison du socket à l'adresse et au port
        server_socket.bind((host, port))
        print(f"Serveur démarré sur {host}:{port}")

        # Le serveur écoute les connexions entrantes (1 connexion simultanée autorisée ici)
        server_socket.listen(2)
        print("En attente de connexion...")

        # Attente d'une connexion client
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connexion établie avec {client_address}")
            new_con(client_socket, client_address)

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        # Fermeture des sockets
        print("Fermeture du serveur.")
        server_socket.close()


def new_con(client_socket, client_address):
    try:
        data = client_socket.recv(cst.MAX_RECV_BYTES).decode()
        if not data:
            # Le client a fermé la connexion
            print("Connexion fermée par le client.")
            client_socket.close()
            return
        if data == "new":
            client_con = Client_Con(str(uuid.uuid4()))
            client_dico[client_con.uuid] = client_con
            client_socket.send("new".encode())
            client_socket.send(client_con.uuid.encode())
            client_con.set_new_client_socket(
                client_socket=client_socket, client_address=client_address
            )
        else:
            if data in client_dico.keys():
                print("Connexion retrouvée avec ", data)
                client_con = client_dico[data]
                client_socket.send("uuid recognised".encode())
                client_socket.send(data.encode())
                client_con.set_new_client_socket(
                    client_socket=client_socket, client_address=client_address
                )
            else:
                print("Connexion NON retrouvée avec ", data)
                client_socket.send("uuid not recognised".encode())
                client_con = Client_Con(str(uuid.uuid4()))
                client_dico[client_con.uuid] = client_con
                client_socket.send(client_con.uuid.encode())
                client_con.set_new_client_socket(
                    client_socket=client_socket, client_address=client_address
                )

    except Exception as e:
        print(f"Erreur : {e}")

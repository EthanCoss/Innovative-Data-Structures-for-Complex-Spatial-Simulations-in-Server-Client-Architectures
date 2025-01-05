import threading

from client import Client
from connexion.client_connexion_manager import ClientConnexionMan

import cst


def start_client():
    client = Client()
    client_con = ClientConnexionMan(client)

    client_con_thread = threading.Thread(
        target=client_con.initiate_connexion, args=[cst.HOST, cst.PORT]
    )
    client_thread = threading.Thread(target=client.start)

    client_con_thread.start()
    client_thread.start()

    client_con_thread.join()
    client_thread.join()


start_client()

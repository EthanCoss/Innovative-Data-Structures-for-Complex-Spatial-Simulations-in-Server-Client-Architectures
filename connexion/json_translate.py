import json

from game.physics import Force
from game.spaceship import Spaceship

import cst
import time


class JsonManCli:
    def __init__(self, client, uuid=0):
        self.client = client
        self.uuid = uuid
        self.current_json = {}
        self.last_round = None

    def set_my_uuid(self, uuid):
        self.uuid = uuid

    def ask_spawn(self):
        self.current_json[cst.QUERRIES][cst.SPAWN_NEW_SPACESHIP] = ""

    def json_base(self):
        self.current_json[cst.ID] = self.client.uuid
        self.current_json[cst.ENTITIES] = {}
        self.current_json[cst.ACTIONS] = {cst.BOOSTER: []}
        self.current_json[cst.QUERRIES] = {}

    def add_spaceship(self, spaceship: Spaceship):
        self.current_json[cst.ENTITIES].update(spaceship.jsonify())

    def new_round(self):
        self.last_round = json.loads(self.stringify())
        self.current_json = {}
        self.json_base()

    def booster_action(self, vector, dt):
        self.current_json[cst.ACTIONS][cst.BOOSTER].append([vector.stringify, dt])

    def stringify(self):
        self.current_json[cst.SENDTIME] = time.time()
        return json.dumps(self.current_json)


class JsonManServ:

    def __init__(self, client_con):
        self.client_con = client_con
        self.uuid = client_con.uuid
        self.current_json = {}
        self.last_round = None

    def new_round(self):
        self.last_round = json.loads(self.stringify())
        self.current_json = {}
        self.json_base()

    def json_base(self):
        self.current_json[cst.ID] = self.client_con.uuid
        self.current_json[cst.ENTITIES] = {}
        self.current_json[cst.ACTIONS] = {}
        self.current_json[cst.QUERRIES] = {}
        self.current_json[cst.RESPONSE] = {}

    def spawned_spaceship_response(self, spaceship: Spaceship):
        self.current_json[cst.RESPONSE][cst.SPAWN_NEW_SPACESHIP] = spaceship.jsonify()
        # self.current_json[cst.ENTITIES].update(spaceship.jsonify())

    def add_entity(self, entity):
        self.current_json[cst.ENTITIES].update(entity.jsonify())

    def add_entities(self, entities_dic):
        self.current_json[cst.ENTITIES].update(entities_dic)

    def stringify(self):
        self.current_json[cst.SENDTIME] = time.time()
        return json.dumps(self.current_json)

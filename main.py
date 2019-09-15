"""D."""
# import getpass
# import io
import json
import os
import select
import sys
import threading
from multiprocessing import Process
import time
import unittest
import random

import vk_api
from requests import exceptions
from vk_api import bot_longpoll
# import ancet
# import keyboards



my_id = 160500068
groupid = 171435747
main_chat_id = 144
Auts_main_chat_id = 1
in_menu = False
authed = False
chat_id = 151
chat_users = None
threads = {}
chats = []
chats_to_show = 50

ancets = {}

command = ''
main_session = None
session = None
running_menu = True
# main_log = open('mainlog.log', 'w+', 1)
vk = None



class Anceteur():

    def __init__(self):
        self.authed = False
        self.longpollServer = None
        self.cup = 1
        self.token = open('token.token', 'r').readline()
        self.currentAncetOnVoting = None
        self.idToInvite = None
        self.ancetsToSendStack = []

# https://vk.com/im?media=&sel=-172301854
    def auth(self):
        """Authentificate bot as group."""
        try:
            print("You are going to log in as Полигон")
            os.system('clear')
            self.session = vk_api.VkApi(token=self.token)
            self.session._auth_token()
            print("authred")
            vk = self.session.get_api()
            global authed
            self.authed = True
            print('gAut Online')
            self.longpollserver = bot_longpoll.VkBotLongPoll(self.session, 172301854)
            print('gAut Online')
            self.gLPS = threading.Thread(target=self.lps, args=(self.session, ), daemon=True)
            # self.gLPS.start()
            print('gAut Online')
            self.lps(session = self.session)
            return True
        except Exception as e:
            print(e)
            pass
# https://vk.com/gim172301854?sel=35608541

    def lps(self, session):
        for event in bot_longpoll.VkBotLongPoll.listen(self.longpollserver):
            payload = event.raw.get("object").get("payload")
            sender_id = event.raw.get("object").get("from_id")

            if (event.raw.get("object").get("text") == "!ancet" or payload == '{\"command\":\"start\"}'):
                # check if human send an initializing message
                print("Got ank rec")
                self.Dialog(sender_id, "Какой у вас вопрос?")#, keybaord=keyboards.ancetKB)
                
            else:
                self.Dialog(usrId = sender_id, message = "Какой у вас вопрос?")#, keybaord=keyboards.ancetKB)
                pass
            time.sleep(0.1)

    def Dialog(self, usrId: int, message: str, keybaord=None):
        r"""
        Dialog is method to send messges to users.
        usrId: Id to send message
        messge: message to send
        keyboard(not obligatory): keyboard from \'keyboards\' module
        """
        if keybaord:
            self.session.method("messages.send",
                                                {
                                                    "peer_id": usrId,
                                                    "keyboard": keybaord,
                                                    "message": message
                                                })
        else:
            self.session.method("messages.send",
                                                {
                                                    "peer_id": usrId,
                                                    "random_id" : random.randint(1, 1000),
                                                    "message": message
                                                })
      


a = Anceteur()
a.auth()


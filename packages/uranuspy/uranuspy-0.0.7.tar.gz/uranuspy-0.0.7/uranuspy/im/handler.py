import json
from functools import wraps
from paho import mqtt
from paho.mqtt import client as mqtt_client
import random
import platform
import os
import uuid
from .topicgen import (
    get_archives_messages_topic,
    get_archives_myid_topic,
    get_archives_rooms_topic,
    get_chatting_topic,
    get_events_topic,
    get_personal_events_topic,
    get_presence_topic,
)
from loguru import logger
from .models import (
    ChatMessage,
    ContactChat,
    Invitation,
    InvitationMessage,
    InvitationMessageType,
    PresenceMessage,
    User,
    MessageType,
)
import jsons
import time
import requests
import pickle
from ..utils import get_device_uuid

MQTT_URL = "manaai.cn"
PORT = 1883

TOKEN_FILE = 'token.pkl'
DATA_FILE = 'cache_data.pkl'

class SirenClient:
    def __init__(self, user_acc, user_password, log_level="info") -> None:
        self.uranus_login_url = "https://db.manaai.cn/api/v2/users_login"
        self.user_acc = user_acc
        self.user_password = user_password
        self.user_addr = ""
        self.client_id = None
        self.data = None
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'rb') as f:
                self.data = pickle.load(f)
                self.client_id = self.data['client_id']

        self.request_uranus_token()
        
        self.user = None
        self.contacts = None
        self.connected = False
        self.client_ready = False

        self._connect()
        self.on_received_msg_func = None
        self.on_received_invitation_func = None        

        if log_level == "info":
            logger.remove(handler_id=None)
    
    def store_cache_data(self, k, v):
        with open(DATA_FILE, 'wb') as f:
            if self.data is not None:
                self.data[k] = v
            else:
                self.data = {}
                self.data[k] = v
                pickle.dump(self.data, f)

    def request_uranus_token(self):
        data = {"user_acc": self.user_acc, "user_password": self.user_password}
        # data = {"user_acc": 'jintian', "user_password": '1195889656'}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        rep = requests.post(url=self.uranus_login_url, headers=headers, data=data)
        rep = json.loads(rep.text)
        if rep["status"] == "error":
            pass
        else:
            token = rep["data"]["token"]
            self.user_addr = rep['data']['user_addr']
            if self.client_id is None:
                self.client_id = f"{get_device_uuid()}_{self.user_addr}"
                self.store_cache_data('client_id', self.client_id)

            logger.info(f'logged as: {self.user_addr} {self.client_id}')
            with open(TOKEN_FILE, "wb") as f:
                pickle.dump(token, f)
                logger.info(f"requested uranus token for robot: {token}")

    def _connect(self):
        logger.info('start connect MQTT server')
        self.client = mqtt_client.Client(self.client_id, True, None, mqtt_client.MQTTv31)
        self.client.username_pw_set(self.user_acc, self.user_password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_URL, PORT)
        self.client.loop_start()

        time.sleep(4)
        while True:
            if not self.connected or not self.client_ready:
                logger.info("still not client ready? wait more 1 seconds.")
                time.sleep(4)
                continue
            else:
                logger.info("Seems connected and client_ready, close loop thread")
                self.client.loop_stop()
                break

    def loop_forever(self):
        self.client.loop_forever()
        # pass

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f"connected.. status: {rc} {userdata}")
        if rc == 0:
            self.connected = True
            logger.info(f"loop start... connected? {self.connected}, clientId: {self.client_id}")
            self.client.loop_start()
            self.subscribe_topics()

    def on_disconnected(self, client, userdata, flags, rc=0):
        logger.error("disconnected...")

    def subscribe_topics(self):
        logger.info('subscribing topics...')
        self.client.subscribe(get_archives_rooms_topic(self.client_id))
        self.client.subscribe(get_archives_messages_topic(self.client_id))
        self.client.subscribe(get_archives_myid_topic(self.client_id))
        logger.info('my topics subscribed.')

    def join_room(self, room_id):
        self.client.subscribe(get_chatting_topic(room_id))
        self.client.subscribe(get_events_topic(room_id))

    def join_contact_presence(self, contact_id):
        self.client.subscribe(get_presence_topic(contact_id))

    def join_my_events(self, myid):
        self.client.subscribe(get_personal_events_topic(myid))

    def on_message(self, client, userdata, msg):
        j = json.loads(msg.payload.decode("utf-8"))
        logger.info("[Msg arrived] topic: {}, payload: {}".format(msg.topic, j))
        if msg.topic.startswith("archivesrooms/"):
            # join room
            if j != None:
                self.contacts = [jsons.load(i, ContactChat) for i in j]
                for c in self.contacts:
                    self.join_room(c.roomId)
                    self.join_contact_presence(c.id)
                logger.info(f"[Synced all contacts] {len(self.contacts)}")
                self.client_ready = True
        elif msg.topic.startswith("archivesmyid/"):
            # get my id
            self.user = jsons.load(j, User)
            self.join_my_events(self.user.user_addr)
            logger.info(f"Welcome: {self.user.user_nick_name}")
        elif msg.topic.startswith("personalevents/"):
            # invitation auto agree
            invit = jsons.load(j, InvitationMessage)
            logger.info(f"Received invitation: {invit.fromName}")
            self.response_to_invitation(invit.id, invit.fromId)
            self.on_received_invitation(invit)
        elif msg.topic.startswith("messages/"):
            m = jsons.load(j, ChatMessage)
            logger.info(
                f"Received ChatMessage: {m.type} {m.text} {m.fromName} {m.roomId}"
            )
            if m.fromId != self.user.user_addr:
                if self.on_received_msg_func:
                    time.sleep(0.5)
                    self.on_received_msg_func(m)
        elif msg.topic.startswith("presence/"):
            m = jsons.load(j, PresenceMessage)
            logger.info(f"[presence] user {m.fromName} is {m.presenceType}.")
        else:
            logger.info(f"unsupported msg: {j}")

    def response_to_invitation(self, invi_id, sender_id):
        invit = InvitationMessage()
        invit.id = invi_id
        invit.fromId = sender_id
        invit.type = MessageType.EventInvitationResponseAccept
        invit.sendTime = int(round(time.time() * 1000))
        invit.text = "我同意了你的好友请求"
        invit.invitationMessageType = InvitationMessageType.REQUEST_RESPONSE
        j = jsons.dumps(invit)
        if sender_id != None:
            logger.info(f"publish: {sender_id}, {j}")
            self.client.publish(get_personal_events_topic(sender_id), j)

    def on_received_invitation(self, func):
        self.on_received_invitation_func = func

    def on_received_chat_message(self, func):
        self.on_received_msg_func = func

    def publish_txt_msg(self, txt, room_id):
        msg = ChatMessage()
        msg.id = uuid.uuid4()
        msg.roomId = room_id
        msg.fromId = self.user.user_addr
        msg.fromName = self.user.user_nick_name
        msg.text = txt
        msg.sendTime = int(round(time.time() * 1000))
        msg.type = MessageType.ChatText
        j = jsons.dumps(msg)
        t = get_chatting_topic(room_id)
        logger.info(f"publishing: {j}, -> {t}")
        self.client.publish(t, j)

    def publish_img_msg(self, img_url, room_id):
        msg = ChatMessage()
        msg.id = uuid.uuid4()
        msg.roomId = room_id
        msg.fromId = self.user.user_addr
        msg.fromName = self.user.user_nick_name
        msg.text = img_url
        msg.sendTime = int(round(time.time() * 1000))
        msg.type = MessageType.ChatImage
        msg.attachment = img_url
        msg.mime = "jpg"
        j = jsons.dumps(msg)
        t = get_chatting_topic(room_id)
        logger.info(f"publishing: {j}, -> {t}")
        self.client.publish(t, j)

    """
    For compatible with Uranus old API
    
    """

    def send_txt_msg(self, target_addr, txt):
        contact = [c for c in self.contacts if c.id == target_addr]
        if len(contact) < 1:
            logger.error(f"can not send to target since {target_addr} not in contacts.")
        else:
            self.publish_txt_msg(txt, contact[0].roomId)

    def send_img_msg(self, target_addr, img_url):
        contact = [c for c in self.contacts if c.id == target_addr]
        if len(contact) < 1:
            logger.error(f"can not send to target since {target_addr} not in contacts.")
        else:
            self.publish_img_msg(img_url, contact[0].roomId)

    def send_msg_to_subscribers(self, txt):
        logger.info(
            f"----- start broadcast msg to subscribers... {self.client_ready} {self.contacts}"
        )
        if self.client_ready and self.contacts is not None:
            logger.info(f"send msg to subscribers, {len(self.contacts)} to go.")
            for c in self.contacts:
                self.publish_txt_msg(txt, c.roomId)

    def send_img_msg_to_subscribers(self, img_url):
        logger.info(
            f"----- start broadcast msg to subscribers... {self.client_ready} {self.contacts}"
        )
        if self.client_ready and self.contacts is not None:
            logger.info(f"send msg to subscribers, {len(self.contacts)} to go.")
            for c in self.contacts:
                self.publish_img_msg(img_url, c.roomId)

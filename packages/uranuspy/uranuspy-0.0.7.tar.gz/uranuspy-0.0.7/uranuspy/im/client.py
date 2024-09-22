from functools import wraps
import json
import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from paho.mqtt.enums import CallbackAPIVersion
import uuid
from uranuspy.im.archive_handler import ArchiveHanlder
from uranuspy.im.mesage_handler import MessageHandler
from uranuspy.im.models import ChatMessage, MessageType, UpdateMessage, User
from uranuspy.im.topicgen import (
    get_archives_myid_topic,
    get_chatting_topic,
    get_events_topic,
    get_personal_events_topic,
    get_presence_topic,
    get_update_archives_rooms_topic,
)
from uranuspy.im.topicgen import get_archives_rooms_topic
from uranuspy.utils import get_device_uuid
from loguru import logger
from .base import BaseClient


class ChatClient(BaseClient):
    def __init__(
        self,
        username,
        password,
        broker_address="manaai.cn",
        port=1883,
    ):
        self.broker_address = broker_address
        self.port = port
        self.username = username
        self.password = password

        # Create an MQTT client instance
        self.cid = self.generate_client_id() + f"_{self.username}"
        self.client = mqtt.Client(
            callback_api_version=CallbackAPIVersion.VERSION2, client_id=self.cid
        )
        print(f"client ID: ", self.cid)

        # Set username and password
        self.client.username_pw_set(username, password)

        # Set callback functions
        self.client.on_connect = self._on_connect
        self.client.on_message = self.on_message

        self.user = None

        # message handlers
        self.archive_handler = ArchiveHanlder()
        self.message_handler = MessageHandler()

        # func callbacks
        self.handle_invitation_func = None
        self.handle_txt_msg_func = None
        self.handle_on_connect_func = None

        self.ready = False
        super().__init__(user_acc=username)

    def publish_standalone(self, topic, msg, qos=2, retain=False):
        # public msg to topic by connect broker and disconnect immiediately
        publish.single(
            topic,
            msg,
            qos=qos,
            retain=retain,
            hostname=self.broker_address,
            port=self.port,
            auth={"username": self.username, "password": self.password},
            client_id=self.cid + "_standalone",
        )

    def _on_connect(self, client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker")
            # Subscribe to a topic if needed
            client.subscribe(get_archives_rooms_topic(self.cid))
            client.subscribe(get_archives_myid_topic(self.cid))
            if self.handle_on_connect_func is not None:
                self.handle_on_connect_func(self)
        else:
            print(f"Connection failed with code {rc}")

    def send_update_archive_msg(self):
        msg = UpdateMessage(
            type=MessageType.UpdateArchive,
            id=str(uuid.uuid4()),
            content="",
            fromId=self.user.user_addr,
            fromName=self.user.user_nick_name,
        )
        payload = msg.model_dump_json()
        topic = get_update_archives_rooms_topic(self.cid)
        self.client.publish(topic, payload)
        logger.info(f"send update archive msg: {payload}, topic: {topic}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        logger.info(f"-->> Received [{msg.topic}]")
        if msg.topic.startswith("archivesmyid/"):
            self.archive_handler.handle_myid(payload)
            self.user = self.archive_handler.user
            logger.info(f"-->> User: {self.user.user_nick_name}")
            self.send_update_archive_msg()
            self.message_handler.init_client(self.user, self.client)
        elif msg.topic.startswith("archivesrooms/"):
            self.archive_handler.handle_contacts(payload)
            self.archive_handler.subscribe_contacts(self.client)
            self.ready = True
        elif msg.topic.startswith("messages/"):
            try:
                msg = ChatMessage(**json.loads(payload))
                if (
                    msg.type == MessageType.ChatText
                    or msg.type == MessageType.ChatImage
                    or msg.type == MessageType.ChatDocument
                    or msg.type == MessageType.ChatAudio
                    or msg.type == MessageType.ChatVideo
                    or msg.type == MessageType.ChatLocation
                ):
                    if msg.fromId == self.user.user_addr:
                        logger.info(f"got myself msg: {msg.text}")
                    else:
                        res = self.handle_txt_msg_func(
                            msg,
                            self.archive_handler.get_contact_by_room_id(msg.roomId),
                            self.user,
                            self,
                        )
                        logger.info(f"**** res for response: {res}")
                        if isinstance(res, tuple):
                            rply, identity = res
                            if identity != None:
                                logger.info(f"sending via custom identity: {identity}")
                                self.message_handler.send_txt_msg(
                                    rply, msg.roomId, identity
                                )
                            elif rply != None:
                                logger.info(f"try send rply: {rply}")
                                self.message_handler.send_txt_msg(rply, msg.roomId)
                        elif res is not None and res != "":
                            self.message_handler.send_txt_msg(res, msg.roomId)
                else:
                    logger.info(f"got msg: {msg.type}, passing...")
            except Exception as e:
                logger.info(f"got error: {e}")
                import traceback

                print("--------------- error start -----------------")
                print(traceback.format_exc())
                print("--------------- error end -----------------")
                # self.message_handler.send_txt_msg(e, msg.roomId)
        elif msg.topic.startswith("events/"):
            logger.info(f"-->> event: {msg.topic}")
        else:
            logger.info(f"-->> unresolved topic: {msg.topic}")

    def join_room(self, room_id):
        self.client.subscribe(get_chatting_topic(room_id))
        self.client.subscribe(get_events_topic(room_id))

    def join_contact_presence(self, contact_id):
        self.client.subscribe(get_presence_topic(contact_id))

    def join_my_events(self, myid):
        self.client.subscribe(get_personal_events_topic(myid))

    def connect(self):
        # Connect to the broker
        self.client.connect(self.broker_address, self.port, keepalive=60)
        # Run the client loop
        self.client.loop_start()

    def publish(self, topic, message):
        # Publish a message
        self.client.publish(topic, message)

    def subscribe(self, topic):
        # Subscribe to a topic
        self.client.subscribe(topic)

    def disconnect(self):
        # Disconnect from the broker
        self.client.disconnect()
        self.client.loop_stop()

    def generate_client_id(self):
        # Generate a client ID based on MAC address
        uid = get_device_uuid()
        return f"pybot-{uid}"

    def handle_invitation(self, func):
        self.handle_invitation_func = func

    def on_txt_msg(self, func):
        self.handle_txt_msg_func = func

    def on_connect(self, func):
        self.handle_on_connect_func = func

    def run_forever(self):
        self.connect()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.client.disconnect()

    def send_msg_to_subscribers(self, txt):
        logger.info(f"---> start broadcast msg to subscribers... {self.cid}")
        for c in self.subscribers_users:
            contact = self.archive_handler.get_room_id_by_user_addr(c["user_addr"])
            self.message_handler.send_txt_msg(txt, contact.roomId)
            logger.info(f"done broadcast: {contact.id} {contact.firstName}")

    def send_img_msg_to_subscribers(self, img_url):
        logger.info(f"----- start broadcast img msg to subscribers... {self.cid}")
        for c in self.subscribers_users:
            contact = self.archive_handler.get_room_id_by_user_addr(c["user_addr"])
            self.message_handler.send_img_msg(img_url, contact.roomId)
            logger.info(f"done broadcast: {contact.id} {contact.firstName}")

    def send_txt_msg_by_user_addr(self, txt, user_addr, standalone=True):
        contact = self.archive_handler.get_room_id_by_user_addr(user_addr)
        if not standalone:
            self.message_handler.send_txt_msg(txt, contact.roomId)
        else:
            pl, topic = self.message_handler.get_txt_msg_payload(txt, contact.roomId)
            self.publish_standalone(topic, pl)

    def send_txt_msg_to_room(self, txt, room_id, standalone=True):
        if not standalone:
            self.message_handler.send_txt_msg(txt, room_id)
        else:
            pl, topic = self.message_handler.get_txt_msg_payload(txt, room_id)
            self.publish_standalone(topic, pl)

    def send_rss_news_msg_to_room(self, txt, room_id, standalone=True):
        pl, topic = self.message_handler.get_rss_news_msg_payload(txt, room_id)
        self.publish_standalone(topic, pl)

    def broadcast_txt_msg(self, txt):
        logger.info(f"---> start broadcast msg to subscribers... {self.cid}")
        for c in self.archive_handler.contacts:
            self.message_handler.send_txt_msg(txt, c.roomId)
            logger.info(f"done broadcast: {c.id} {c.firstName}")


def run_forever_in_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


@run_forever_in_thread
def run_client_forever(client):
    try:
        client.run_forever()
    except KeyboardInterrupt:
        logger.info(f"Stopping {client.cid} {client.user_nick_name}...")


# Example usage:
if __name__ == "__main__":
    mqtt_client = MqttClient("manaai.cn", 1883, "friday", "1195889656")

    # Connect to the broker
    mqtt_client.connect()

    # Publish a message (optional)
    # mqtt_client.publish("your_topic", "Hello, MQTT!")

    @mqtt_client.handle_txt_msg
    def on_txt_msg(msg: ChatMessage):
        print(f"Received chat message: {msg}")
        return "你好啊"

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Disconnected. Exiting...")
        mqtt_client.disconnect()

import json
import threading
import time
import uuid

from loguru import logger
from uranuspy.im.models import ChatMessage, MessageType, User
from uranuspy.im.topicgen import get_chatting_topic
import requests
from PIL import ImageFile
import json


def get_img_wh_from_url(url):
    resume_header = {
        "Range": "bytes=0-2000000"
    }  ## the amount of bytes you will download
    data = requests.get(url, stream=True, headers=resume_header).content

    p = ImageFile.Parser()
    p.feed(data)  ## feed the data to image parser to get photo info from data headers
    if p.image:
        return p.image.size
    return None


class MessageHandler:
    def __init__(self) -> None:
        self.user = None
        self.client = None
        self.send_lock = threading.Lock()

    def init_client(self, user, client):
        self.user = user
        self.client = client

    def send_payload(self, topic, payload):
        self.client.publish(topic, payload, qos=2)

    def get_txt_msg_payload(self, txt, room_id, identity: User = None):
        if self.user is None or self.client is None:
            raise ValueError("user or client not initiated!")
        msg = ChatMessage(
            id=str(uuid.uuid4()),
            roomId=room_id,
            fromId=self.user.user_addr,
            fromName=(
                identity.user_nick_name
                if identity is not None
                else self.user.user_nick_name
            ),
            imgUrl=(
                identity.user_avatar_url
                if identity is not None
                else self.user.user_avatar_url
            ),
            text=txt,
            sendTime=int(round(time.time() * 1000)),
            type=MessageType.ChatText,
        )

        t = get_chatting_topic(room_id)
        pl = msg.model_dump_json()
        logger.info(f"publishing: {pl}, -> {t}")
        return pl, t

    def get_rss_news_msg_payload(self, txt, room_id, identity: User = None):
        if self.user is None or self.client is None:
            raise ValueError("user or client not initiated!")
        try:
            a = json.loads(txt)
        except Exception as e:
            ValueError(
                f"json load error for text, you should make sure text is a json serializable str."
                "error: {e}"
            )
        msg = ChatMessage(
            id=str(uuid.uuid4()),
            roomId=room_id,
            fromId=self.user.user_addr,
            fromName=(
                identity.user_nick_name
                if identity is not None
                else self.user.user_nick_name
            ),
            imgUrl=(
                identity.user_avatar_url
                if identity is not None
                else self.user.user_avatar_url
            ),
            text=txt,
            sendTime=int(round(time.time() * 1000)),
            type=MessageType.ChatRssNews,
        )

        t = get_chatting_topic(room_id)
        pl = msg.model_dump_json()
        logger.info(f"publishing: {pl}, -> {t}")
        return pl, t

    def send_txt_msg(self, txt, room_id, identity=None):
        if identity is not None:
            pl, t = self.get_txt_msg_payload(txt, room_id, identity)
        else:
            pl, t = self.get_txt_msg_payload(txt, room_id)
        self.send_payload(t, pl)

    def send_img_msg(self, txt, room_id):
        if self.user is None or self.client is None:
            raise ValueError("user or client not initiated!")

        img_wh = get_img_wh_from_url(txt)

        # get image width and height here
        msg = ChatMessage(
            id=str(uuid.uuid4()),
            roomId=room_id,
            fromId=self.user.user_addr,
            fromName=self.user.user_nick_name,
            text=txt,
            attachment=txt,
            sendTime=int(round(time.time() * 1000)),
            type=MessageType.ChatImage,
            longitude=img_wh[0] if img_wh is not None else 0,
            latitude=img_wh[1] if img_wh is not None else 0,
        )

        t = get_chatting_topic(room_id)
        logger.info(f"publishing: {msg.model_dump_json()}, -> {t}")
        self.send_payload(t, msg.model_dump_json())

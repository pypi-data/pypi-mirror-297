import json
from typing import List
from uranuspy.im.models import ContactChat, User
from loguru import logger

from uranuspy.im.topicgen import get_chatting_topic, get_events_topic


class ArchiveHanlder:
    def __init__(self) -> None:
        self.user = User()
        self.contacts: List[ContactChat] = []

    def handle_myid(self, data):
        logger.info(f"got myid: {data}")
        if isinstance(data, str):
            data = json.loads(data)
        self.user = User(**data)
        # self.user = User.from
        logger.info(f"got user: {self.user}")

    def handle_contacts(self, data):
        logger.info(f"got contacts: ")
        if isinstance(data, str):
            data = json.loads(data)
        for d in data:
            c = ContactChat(**d)
            self.contacts.append(c)
        logger.info(f"got contacs: {len(self.contacts)}")

    def get_contact_by_room_id(self, room_id):
        a = [i for i in self.contacts if i.roomId == room_id]
        if len(a) > 0:
            return a[0]
        else:
            return None
    
    def get_room_id_by_user_addr(self, user_addr):
        a = [i for i in self.contacts if not i.isGroup and i.id == user_addr]
        if len(a) > 0:
            return a[0]
        else:
            return None

    def subscribe_contacts(self, client):
        if len(self.contacts) > 0:
            for c in self.contacts:
                # subscribe roomMsg
                client.subscribe(get_chatting_topic(c.roomId))
                client.subscribe(get_events_topic(c.roomId))
            logger.info(f"done subscribe contacts: {len(self.contacts)}")

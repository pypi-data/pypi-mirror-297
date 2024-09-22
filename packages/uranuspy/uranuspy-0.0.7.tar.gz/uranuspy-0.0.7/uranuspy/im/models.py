"""

contains all models used in Siren chatbot API

"""

import json
import jsons
from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class MessageType(str, Enum):
    ChatText: str = "ChatText"
    ChatImage: str = "ChatImage"
    ChatVideo: str = "ChatVideo"
    ChatAudio: str = "ChatAudio"
    ChatDocument: str = "ChatDocument"
    ChatLocation: str = "ChatLocation"
    ChatContact: str = "ChatContact"
    EventInvitationRequest: str = "EventInvitationRequest"
    EventInvitationResponseAccept: str = "EventInvitationResponseAccept"
    EventInvitationResponseReject: str = "EventInvitationResponseReject"
    Presence: str = "Presence"
    ChatMarker: str = "ChatMarker"
    Typing: str = "Typing"
    CreateGroup: str = "CreateGroup"
    RemoveGroup: str = "RemoveGroup"
    AddUsersToGroup: str = "AddUsersToGroup"
    RemoveGroupMembers: str = "RemoveGroupMembers"
    UpdateArchive: str = "UpdateArchive"
    EnterGroup: str = "EnterGroup"
    ChatShake: str = "ChatShake"
    ChatRssNews: str = "ChatRssNews"


class InvitationMessageType(str, Enum):
    REQUEST_RESPONSE: str = "REQUEST_RESPONSE"
    ERROR: str = "ERROR"
    INFO: str = "INFO"


class PresenceType(str, Enum):
    Available: str = "Available"
    Away: str = "Away"
    Unavailable: str = "Unavailable"


class MessageOriginality(str, Enum):
    Original: str = "Original"
    Reply: str = "Reply"
    Forward: str = "Forward"


class PresenceSession:
    id: str = None
    user_id: str = None
    presence: str = None
    last_presence: str = None


class BaseMessage(BaseModel):
    id: str = None
    type: MessageType = MessageType.ChatText
    fromId: str = None
    fromName: Optional[str] = None


class UpdateMessage(BaseMessage):
    content: str = ""


class PresenceMessage(BaseMessage):
    presenceType: PresenceType = PresenceType.Available


class ChatMessage(BaseMessage):
    toId: Optional[str] = None
    toName: Optional[str] = None
    text: Optional[str] = None
    attachment: Optional[str] = None
    imgUrl: Optional[str] = None
    thumbnail: Optional[str] = None
    originalId: Optional[str] = None
    originalMessage: Optional[str] = None
    roomId: Optional[str] = None
    originality: MessageOriginality = MessageOriginality.Original
    size: Optional[int] = 0
    mime: Optional[str] = None
    sendTime: Optional[int] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    isRevoked: Optional[bool] = False


class Invitation(BaseMessage):
    id: Optional[str] = None
    from_id: Optional[str] = None
    to_id: Optional[str] = None
    state: Optional[str] = None
    sent_date: Optional[str] = None


class Room:
    id: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    is_group: Optional[bool] = None


class RoomMembership:
    room_id = None
    user_id = None
    role = None


class InvitationMessage:
    id = None
    type: MessageType = MessageType.EventInvitationRequest
    invitationMessageType: InvitationMessageType = InvitationMessageType.INFO
    text = None
    sendTime = None
    fromId = None
    toId = None
    fromName = None
    fromAvatar = None


class ContactChat(BaseModel):
    firstName: str = None
    lastName: str = None
    id: str = None
    avatar: str = None
    roomId: str = None
    presence: PresenceType = PresenceType.Available
    isGroup: bool = None


class User(BaseModel):
    user_addr: Optional[str] = None
    user_acc: Optional[str] = None
    user_sign: Optional[str] = None
    user_gender: Optional[str] = None
    user_nick_name: Optional[str] = None
    user_avatar_url: Optional[str] = None

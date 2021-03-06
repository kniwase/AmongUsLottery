from pydantic import BaseModel
from typing import Optional, List


class RoomReq(BaseModel):
    room_name: Optional[str]
    user_name: str


class Room(BaseModel):
    room_name: str
    members: List[str]
    admin: str
    winner: Optional[str]
    allow_god_mode: bool

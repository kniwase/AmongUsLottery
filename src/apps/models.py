from pydantic import BaseModel
from typing import Optional, List


class RoomReq(BaseModel):
    room_name: Optional[str]
    user_name: str


class Role(BaseModel):
    id: str
    name: str
    count: int


class RoleMembers(BaseModel):
    name: str
    members: List[str]


class Room(BaseModel):
    room_name: str
    members: List[str]
    admin: str
    roles: List[Role]
    role_members: List[RoleMembers]
    allow_god_mode: bool

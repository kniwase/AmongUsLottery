from settings import INDEX_PATH
import models
import asyncio
import uuid
import json
import random
from datetime import datetime
from typing import List
import logging

logging.basicConfig(level=logging.INFO)

with open(INDEX_PATH, encoding="utf8") as f:
    INDEX_HTML = f.read()

ROLE_TERUTERU = {"id": "teruteru", "name": "てるてる", "count": 1}
ROLE_MADMAN = {"id": "madman", "name": "狂人", "count": 1}


rooms = {}
subscribers = {}


async def read_room_props(room_name):
    if room_name in rooms.keys():
        room_props = rooms[room_name]
    else:
        room_props = {}
    return room_props


async def send_notification(room_name, payload):
    if room_name in subscribers.keys():
        for queue_id in subscribers[room_name].keys():
            subscribers[room_name][queue_id] = payload


async def update_room_props(room_name, room_props):
    rooms[room_name] = room_props
    await send_notification(room_name, room_props)


async def delete_room_props(room_name):
    if room_name in rooms.keys():
        rooms.pop(room_name)
    await send_notification(room_name, {})


async def get_all_rooms():
    return list(rooms.values())


async def create_room(room_req: models.RoomReq):
    if room_req.room_name not in rooms.keys():
        roles = [ROLE_TERUTERU, ROLE_MADMAN]
        room_props = {
            "room_name": room_req.room_name,
            "members": [room_req.user_name],
            "admin": room_req.user_name,
            "roles": roles,
            "role_members": [],
            "lot_timestamp": None,
            "allow_god_mode": True
        }
        subscribers[room_req.room_name] = {}
        await update_room_props(room_req.room_name, room_props)
        logging.info(
            f'Room "{room_req.room_name}" was created by {room_req.user_name}.')
        res = {
            "isSucceeded": True,
            "ret": rooms[room_req.room_name]
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋名はすでに使用されています"
        }
    return res


async def get_room_props(room_name: str):
    room_props = await read_room_props(room_name)
    if room_props:
        res = {
            "isSucceeded": True,
            "ret": room_props
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def draw_lot(room_name: str):
    room_props = await read_room_props(room_name)
    if room_props:
        members = room_props["members"]
        members_randomized = random.sample(members, len(members))
        role_members = []
        for role in room_props["roles"]:
            role_name = role["name"]
            role_count = role["count"]
            role_members.append({
                "name": role_name,
                "members": members_randomized[:role_count]
            })
            members_randomized = members_randomized[role_count:]
        room_props["role_members"] = role_members
        room_props["lot_timestamp"] = datetime.now().isoformat()
        await update_room_props(room_name, room_props)
        logging.info(f'Role Memebers of Room "{room_name}" are changed')
        res = {
            "isSucceeded": True,
            "ret": room_props
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def delete_room(room_name: str):
    if await read_room_props(room_name):
        await delete_room_props(room_name)
        logging.info(f'Room "{room_name}" was deleted.')
        res = {
            "isSucceeded": True,
            "ret": {}
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def join_to_room(room_name: str, user_name: str):
    room_props = await read_room_props(room_name)
    if room_props:
        if user_name not in room_props["members"]:
            room_props["members"].append(user_name)
            await update_room_props(room_name, room_props)
            logging.info(f'"{user_name}" joined to {room_name}.')
            res = {
                "isSucceeded": True,
                "ret": room_props
            }
        else:
            res = {
                "isSucceeded": False,
                "ret": "指定したユーザー名はすでに使用されています"
            }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def delete_member(room_name: str, user_name: str):
    room_props = await read_room_props(room_name)
    if room_props:
        if user_name in room_props["members"]:
            room_props["members"].remove(user_name)
            if room_props["members"]:
                if room_props["admin"] == user_name:
                    room_props["admin"] = room_props["members"][0]
                await update_room_props(room_name, room_props)
                logging.info(f'"{user_name}" left from {room_name}.')
                res = {
                    "isSucceeded": True,
                    "ret": room_props
                }
            else:
                rooms.pop(room_name)
                logging.info(f'Room "{room_name}" was deleted.')
                res = {
                    "isSucceeded": True,
                    "ret": {}
                }
        else:
            res = {
                "isSucceeded": False,
                "ret": "指定したユーザーは存在しません"
            }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def change_admin_user(room_name: str, user_name: str):
    room_props = await read_room_props(room_name)
    if room_props:
        if user_name in room_props["members"]:
            room_props["admin"] = user_name
            await update_room_props(room_name, room_props)
            logging.info(
                f'Admin user of "{room_name}" was changed to "{user_name}".')
            res = {
                "isSucceeded": True,
                "ret": room_props
            }
        else:
            res = {
                "isSucceeded": False,
                "ret": "指定したユーザー名は存在しません"
            }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def change_role_settings(room_name: str, roles: List[models.Role]):
    room_props = await read_room_props(room_name)
    if room_props:
        roles_dict = [r.dict() for r in roles]
        room_props["roles"] = roles_dict
        room_props["role_members"] = []
        room_props["lot_timestamp"] = None
        await update_room_props(room_name, room_props)
        logging.info(f'Role settings of "{room_name}" was changed.')
        res = {
            "isSucceeded": True,
            "ret": room_props
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def toggle_god_mode(room_name: str):
    room_props = await read_room_props(room_name)
    if room_props:
        allow_god_mode = not room_props["allow_god_mode"]
        room_props["allow_god_mode"] = allow_god_mode
        await update_room_props(room_name, room_props)
        logging.info(
            f'GodMode of "{room_name}" was set to {allow_god_mode}.')
        res = {
            "isSucceeded": True,
            "ret": room_props
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def room_props_event_generator(request, room_name: str):
    queue_id = str(uuid.uuid4())
    subscribers[room_name][queue_id] = None
    while True:
        if await request.is_disconnected():
            if queue_id in subscribers[room_name].keys():
                subscribers[room_name].pop(queue_id)
            if not subscribers[room_name]:
                subscribers.pop(room_name)
            break
        if subscribers[room_name][queue_id] is not None:
            room_props = subscribers[room_name][queue_id]
            subscribers[room_name][queue_id] = None
            yield json.dumps(room_props, ensure_ascii=False)
        asyncio.sleep(1)


async def create_subscription(request, room_name: str):
    if room_name in rooms.keys():
        res = {
            "isSucceeded": True,
            "ret": room_props_event_generator(request, room_name)
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res

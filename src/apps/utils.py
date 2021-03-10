from settings import INDEX_PATH
import models
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


async def get_all_rooms():
    return list(rooms.values())


async def create_room(room_req: models.RoomReq):
    if room_req.room_name not in rooms.keys():
        roles = [ROLE_TERUTERU, ROLE_MADMAN]
        rooms[room_req.room_name] = {
            "room_name": room_req.room_name,
            "members": [room_req.user_name],
            "admin": room_req.user_name,
            "roles": roles,
            "role_members": [],
            "lot_timestamp": None,
            "allow_god_mode": True
        }
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
    if room_name in rooms.keys():
        res = {
            "isSucceeded": True,
            "ret": rooms[room_name]
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def draw_lot(room_name: str):
    if room_name in rooms.keys():
        members = rooms[room_name]["members"]
        members_randomized = random.sample(members, len(members))
        role_members = []
        for role in rooms[room_name]["roles"]:
            role_name = role["name"]
            role_count = role["count"]
            role_members.append({
                "name": role_name,
                "members": members_randomized[:role_count]
            })
            members_randomized = members_randomized[role_count:]
        rooms[room_name]["role_members"] = role_members
        rooms[room_name]["lot_timestamp"] = datetime.now().isoformat()
        logging.info(f'Role Memebers of Room "{room_name}" are changed')
        res = {
            "isSucceeded": True,
            "ret": rooms[room_name]
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def delete_room(room_name: str):
    if room_name in rooms.keys():
        rooms.pop(room_name)
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
    if room_name in rooms.keys():
        if user_name not in rooms[room_name]["members"]:
            rooms[room_name]["members"].append(user_name)
            logging.info(f'"{user_name}" joined to {room_name}.')
            res = {
                "isSucceeded": True,
                "ret": rooms[room_name]
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
    if room_name in rooms.keys():
        if user_name in rooms[room_name]["members"]:
            rooms[room_name]["members"].remove(user_name)
            if rooms[room_name]["members"]:
                if rooms[room_name]["admin"] == user_name:
                    rooms[room_name]["admin"] = rooms[room_name]["members"][0]
                logging.info(f'"{user_name}" left from {room_name}.')
                res = {
                    "isSucceeded": True,
                    "ret": rooms[room_name]
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
    if room_name in rooms.keys():
        if user_name in rooms[room_name]["members"]:
            rooms[room_name]["admin"] = user_name
            logging.info(
                f'Admin user of "{room_name}" was changed to "{user_name}".')
            res = {
                "isSucceeded": True,
                "ret": rooms[room_name]
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
    if room_name in rooms.keys():
        roles_dict = [r.dict() for r in roles]
        rooms[room_name]["roles"] = roles_dict
        rooms[room_name]["role_members"] = []
        rooms[room_name]["lot_timestamp"] = None
        logging.info(f'Role settings of "{room_name}" was changed.')
        res = {
            "isSucceeded": True,
            "ret": rooms[room_name]
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res


async def toggle_god_mode(room_name: str):
    if room_name in rooms.keys():
        allow_god_mode = not rooms[room_name]["allow_god_mode"]
        rooms[room_name]["allow_god_mode"] = allow_god_mode
        logging.info(
            f'GodMode of "{room_name}" was set to {allow_god_mode}.')
        res = {
            "isSucceeded": True,
            "ret": rooms[room_name]
        }
    else:
        res = {
            "isSucceeded": False,
            "ret": "指定した部屋は存在しません"
        }
    return res

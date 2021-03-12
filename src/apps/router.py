from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sse_starlette.sse import EventSourceResponse
from typing import List
import utils
import models
import logging

logging.basicConfig(level=logging.INFO)

router_view = APIRouter()
router_api = APIRouter()


@router_view.get("/")
async def get_index_html():
    return HTMLResponse(utils.INDEX_HTML)


@router_api.get("/rooms", response_model=List[models.Room])
async def get_all_rooms():
    res = await utils.get_all_rooms()
    return JSONResponse(res, status_code=200)


@router_api.post("/rooms", response_model=models.Room)
async def create_room(room_req: models.RoomReq):
    res = await utils.create_room(room_req)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=201)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.get("/rooms/{room_name}", response_model=models.Room)
async def get_room_props(room_name: str):
    res = await utils.get_room_props(room_name)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=200)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.put("/rooms/{room_name}/lot", response_model=models.Room)
async def draw_lot(room_name: str):
    res = await utils.draw_lot(room_name)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=200)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.delete("/rooms/{room_name}")
async def delete_room(room_name: str):
    res = await utils.delete_room(room_name)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=200)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.post("/rooms/{room_name}/members")
async def join_to_room(room_name: str, room_req: models.RoomReq):
    res = await utils.join_to_room(room_name, room_req.user_name)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=201)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.delete("/rooms/{room_name}/members/{user_name}")
async def delete_member(room_name: str, user_name: str):
    res = await utils.delete_member(room_name, user_name)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=200)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.put("/rooms/{room_name}/roles", response_model=models.Room)
async def change_role_settings(room_name: str, roles: List[models.Role]):
    res = await utils.change_role_settings(room_name, roles)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=200)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.put("/rooms/{room_name}/admin")
async def change_admin_user(room_name: str, room_req: models.RoomReq):
    res = await utils.change_admin_user(room_name, room_req.user_name)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=202)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.put("/rooms/{room_name}/godmode")
async def toggle_god_mode(room_name: str):
    res = await utils.toggle_god_mode(room_name)
    if res["isSucceeded"]:
        return JSONResponse(res["ret"], status_code=202)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)


@router_api.get("/rooms/{room_name}/subscription")
async def create_subscription(room_name: str, request: Request):
    res = await utils.create_subscription(request, room_name)
    if res["isSucceeded"]:
        return EventSourceResponse(res["ret"], status_code=200)
    else:
        return JSONResponse({"error": res["ret"]}, status_code=400)

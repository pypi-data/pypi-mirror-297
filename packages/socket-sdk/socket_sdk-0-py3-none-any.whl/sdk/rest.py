import requests
from .models import (
    User, Lobby, FindLobbyInput, SaveLobbyInput,
    Tag, Place
)
from .logger import logger

API_BASE_URL = "https://dishdash.ru/api/v1"
SOCKETIO_HOST = "https://dishdash.ru"

def find_lobby(find_lobby_input: FindLobbyInput) -> Lobby:
    try:
        logger.info(f"[REST] [POST] /lobbies/find {find_lobby_input.to_dict()} -> ", extra={"type": "rest"})
        response = requests.post(f"{API_BASE_URL}/lobbies/find", json=find_lobby_input.to_dict())
        response.raise_for_status()
        lobby = Lobby.from_dict(response.json())
        logger.info(f"[REST] [POST] /lobbies/find -> {response.json()}", extra={"type": "rest"})
        return lobby
    except requests.RequestException as e:
        logger.error(f"[REST] [POST] /lobbies/find {find_lobby_input.to_dict()} -> Error: {e}", extra={"type": "rest"})
        raise


def create_user(user: User) -> User:
    try:
        logger.info(f"[REST] [POST] /users {user.to_dict()} -> ", extra={"type": "rest"})
        response = requests.post(f"{API_BASE_URL}/users", json=user.to_dict())
        response.raise_for_status()
        user = User.from_dict(response.json())
        logger.info(f"[REST] [POST] /users -> {response.json()}", extra={"type": "rest"})
        return user
    except requests.RequestException as e:
        logger.error(f"[REST] [POST] /users {user.to_dict()} -> Error: {e}", extra={"type": "rest"})
        raise


def create_lobby(lobby_input: SaveLobbyInput) -> Lobby:
    try:
        logger.info(f"[REST] [POST] /lobbies {lobby_input.to_dict()} -> ", extra={"type": "rest"})
        response = requests.post(f"{API_BASE_URL}/lobbies", json=lobby_input.to_dict())
        response.raise_for_status()
        lobby = Lobby.from_dict(response.json())
        logger.info(f"[REST] [POST] /lobbies -> {response.json()}", extra={"type": "rest"})
        return lobby
    except requests.RequestException as e:
        logger.error(f"[REST] [POST] /lobbies {lobby_input.to_dict()} -> Error: {e}", extra={"type": "rest"})
        raise


def get_lobby(lobby_id: str) -> Lobby:
    try:
        logger.info(f"[REST] [GET] /lobbies/{lobby_id} -> ", extra={"type": "rest"})
        response = requests.get(f"{API_BASE_URL}/lobbies/{lobby_id}")
        response.raise_for_status()
        lobby = Lobby.from_dict(response.json())
        logger.info(f"[REST] [GET] /lobbies/{lobby_id} -> {response.json()}", extra={"type": "rest"})
        return lobby
    except requests.RequestException as e:
        logger.error(f"[REST] [GET] /lobbies/{lobby_id} -> Error: {e}", extra={"type": "rest"})
        raise


def delete_lobby(lobby_id: str) -> None:
    try:
        logger.info(f"[REST] [DELETE] /lobbies/{lobby_id} -> ", extra={"type": "rest"})
        response = requests.delete(f"{API_BASE_URL}/lobbies/{lobby_id}")
        response.raise_for_status()
        logger.info(f"[REST] [DELETE] /lobbies/{lobby_id} -> {response.status_code}", extra={"type": "rest"})
    except requests.RequestException as e:
        logger.error(f"[REST] [DELETE] /lobbies/{lobby_id} -> Error: {e}", extra={"type": "rest"})
        raise


def get_users() -> list[User]:
    try:
        logger.info(f"[REST] [GET] /users -> ", extra={"type": "rest"})
        response = requests.get(f"{API_BASE_URL}/users")
        response.raise_for_status()
        users = [User.from_dict(user_data) for user_data in response.json()]
        logger.info(f"[REST] [GET] /users -> {response.json()}", extra={"type": "rest"})
        return users
    except requests.RequestException as e:
        logger.error(f"[REST] [GET] /users -> Error: {e}", extra={"type": "rest"})
        raise


def update_user(user: User) -> User:
    try:
        logger.info(f"[REST] [PUT] /users/{user.id} {user.to_dict()} -> ", extra={"type": "rest"})
        response = requests.put(f"{API_BASE_URL}/users/{user.id}", json=user.to_dict())
        response.raise_for_status()
        updated_user = User.from_dict(response.json())
        logger.info(f"[REST] [PUT] /users/{user.id} -> {response.json()}", extra={"type": "rest"})
        return updated_user
    except requests.RequestException as e:
        logger.error(f"[REST] [PUT] /users/{user.id} -> Error: {e}", extra={"type": "rest"})
        raise


def save_user(user: User) -> User:
    try:
        logger.info(f"[REST] [POST] /users {user.to_dict()} -> ", extra={"type": "rest"})
        response = requests.post(f"{API_BASE_URL}/users", json=user.to_dict())
        response.raise_for_status()
        saved_user = User.from_dict(response.json())
        logger.info(f"[REST] [POST] /users -> {response.json()}", extra={"type": "rest"})
        return saved_user
    except requests.RequestException as e:
        logger.error(f"[REST] [POST] /users {user.to_dict()} -> Error: {e}", extra={"type": "rest"})
        raise


def get_user(user_id: str) -> User:
    try:
        logger.info(f"[REST] [GET] /users/{user_id} -> ", extra={"type": "rest"})
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        response.raise_for_status()
        user = User.from_dict(response.json())
        logger.info(f"[REST] [GET] /users/{user_id} -> {response.json()}", extra={"type": "rest"})
        return user
    except requests.RequestException as e:
        logger.error(f"[REST] [GET] /users/{user_id} -> Error: {e}", extra={"type": "rest"})
        raise


def get_user_by_telegram(telegram_id: int) -> User:
    try:
        logger.info(f"[REST] [GET] /users/telegram/{telegram_id} -> ", extra={"type": "rest"})
        response = requests.get(f"{API_BASE_URL}/users/telegram/{telegram_id}")
        response.raise_for_status()
        user = User.from_dict(response.json())
        logger.info(f"[REST] [GET] /users/telegram/{telegram_id} -> {response.json()}", extra={"type": "rest"})
        return user
    except requests.RequestException as e:
        logger.error(f"[REST] [GET] /users/telegram/{telegram_id} -> Error: {e}", extra={"type": "rest"})
        raise


def get_places() -> list[Place]:
    try:
        logger.info(f"[REST] [GET] /places -> ", extra={"type": "rest"})
        response = requests.get(f"{API_BASE_URL}/places")
        response.raise_for_status()
        places = [Place.from_dict(place_data) for place_data in response.json()]
        logger.info(f"[REST] [GET] /places -> {response.json()}", extra={"type": "rest"})
        return places
    except requests.RequestException as e:
        logger.error(f"[REST] [GET] /places -> Error: {e}", extra={"type": "rest"})
        raise


def create_place(place: Place) -> Place:
    try:
        logger.info(f"[REST] [POST] /places {place.to_dict()} -> ", extra={"type": "rest"})
        response = requests.post(f"{API_BASE_URL}/places", json=place.to_dict())
        response.raise_for_status()
        created_place = Place.from_dict(response.json())
        logger.info(f"[REST] [POST] /places -> {response.json()}", extra={"type": "rest"})
        return created_place
    except requests.RequestException as e:
        logger.error(f"[REST] [POST] /places {place.to_dict()} -> Error: {e}", extra={"type": "rest"})
        raise


def update_tag(tag_id: str, tag: Tag) -> Tag:
    try:
        logger.info(f"[REST] [PUT] /places/tag/{tag_id} {tag.to_dict()} -> ", extra={"type": "rest"})
        response = requests.put(f"{API_BASE_URL}/places/tag/{tag_id}", json=tag.to_dict())
        response.raise_for_status()
        updated_tag = Tag.from_dict(response.json())
        logger.info(f"[REST] [PUT] /places/tag/{tag_id} -> {response.json()}", extra={"type": "rest"})
        return updated_tag
    except requests.RequestException as e:
        logger.error(f"[REST] [PUT] /places/tag/{tag_id} -> Error: {e}", extra={"type": "rest"})
        raise


def delete_tag(tag_id: str) -> None:
    try:
        logger.info(f"[REST] [DELETE] /places/tag/{tag_id} -> ", extra={"type": "rest"})
        response = requests.delete(f"{API_BASE_URL}/places/tag/{tag_id}")
        response.raise_for_status()
        logger.info(f"[REST] [DELETE] /places/tag/{tag_id} -> {response.status_code}", extra={"type": "rest"})
    except requests.RequestException as e:
        logger.error(f"[REST] [DELETE] /places/tag/{tag_id} -> Error: {e}", extra={"type": "rest"})
        raise


def get_tags() -> list[Tag]:
    try:
        logger.info(f"[REST] [GET] /places/tags -> ", extra={"type": "rest"})
        response = requests.get(f"{API_BASE_URL}/places/tags")
        response.raise_for_status()
        tags = [Tag.from_dict(tag_data) for tag_data in response.json()]
        logger.info(f"[REST] [GET] /places/tags -> {response.json()}", extra={"type": "rest"})
        return tags
    except requests.RequestException as e:
        logger.error(f"[REST] [GET] /places/tags -> Error: {e}", extra={"type": "rest"})
        raise


def create_tag(tag: Tag) -> Tag:
    try:
        logger.info(f"[REST] [POST] /places/tags {tag.to_dict()} -> ", extra={"type": "rest"})
        response = requests.post(f"{API_BASE_URL}/places/tags", json=tag.to_dict())
        response.raise_for_status()
        created_tag = Tag.from_dict(response.json())
        logger.info(f"[REST] [POST] /places/tags -> {response.json()}", extra={"type": "rest"})
        return created_tag
    except requests.RequestException as e:
        logger.error(f"[REST] [POST] /places/tags {tag.to_dict()} -> Error: {e}", extra={"type": "rest"})
        raise

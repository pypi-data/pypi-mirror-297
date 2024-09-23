from dataclasses import dataclass
from typing import List, Dict
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Coordinate:
    lat: float
    lon: float


@dataclass_json
@dataclass
class Tag:
    icon: str
    id: int
    name: str


@dataclass_json
@dataclass
class Place:
    address: str
    description: str
    id: int
    image: List[str]
    location: Coordinate
    priceAvg: int
    reviewCount: int
    reviewRating: float
    shortDescription: str
    tags: List[Tag]
    title: str
    updatedAt: str


@dataclass_json
@dataclass
class Swipe:
    cardID: int
    id: int
    lobbyID: str
    type: str
    userID: str


@dataclass_json
@dataclass
class User:
    id: str
    name: str
    avatar: str
    telegram: int


@dataclass_json
@dataclass
class Lobby:
    createdAt: str
    id: str
    location: Coordinate
    places: List[Place]
    priceAvg: int
    state: str
    swipes: List[Swipe]
    tags: List[Tag]
    users: List[User]


@dataclass_json
@dataclass
class NearestLobbyOutput:
    distance: float
    lobby: Lobby


@dataclass_json
@dataclass
class FindLobbyInput:
    dist: float
    location: Coordinate


@dataclass_json
@dataclass
class SaveLobbyInput:
    location: Coordinate
    priceAvg: int


@dataclass_json
@dataclass
class SavePlaceInput:
    address: str
    description: str
    images: List[str]
    location: Coordinate
    priceMin: int
    reviewCount: int
    reviewRating: float
    shortDescription: str
    tags: List[int]
    title: str

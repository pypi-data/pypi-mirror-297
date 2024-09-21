from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


class Response:
    def __init__(
        self, status_code: int, message: str = "", data: list[dict] | None = None
    ) -> None:
        """Result returned from low-level api wrapper.

        Args:
            status_code (int): Standard HTTP status code
            message (str, optional): Human readable result. Defaults to "".
            data (list[dict] | None, optional): Python List of Dictionaries. Defaults to None.
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


@dataclass
class Recommendations:
    id: int
    ping: int
    download: float
    upload: float


@dataclass
class Version:
    local: str
    remote: str


@dataclass
class Interface:
    name: str
    ip_address: str


@dataclass
class SpeedTestStatus:
    paused: bool
    running: bool


@dataclass
class SpeedTest:
    id: int
    server_id: int
    ping: int
    download: float
    upload: float
    type: str
    result_id: UUID
    time: int
    created: datetime

    def __init__(self, id: int, serverId: int, ping: int, download: float, upload: float, type: str, resultId: UUID, time: int, created: datetime):
        self.id = id
        self.server_id = serverId
        self.ping = ping
        self.download = download
        self.upload = upload
        self.type = type
        self.result_id = resultId
        self.time = time
        self.created = created


@dataclass
class SpeedTestAverageElement:
    ping: int
    download: float
    upload: float
    type: str
    amount: int
    created: datetime


@dataclass
class SpeedTestData:
    ping: list[int]
    download: list[float]
    upload: list[float]
    time: list[int]


@dataclass
class Statistic:
    min: float
    max: float
    avg: float


@dataclass
class Tests:
    total: int
    failed: int
    custom: int


@dataclass
class SpeedTestStatistics:
    tests: Tests
    ping: Statistic
    download: Statistic
    upload: Statistic
    time: Statistic
    data: SpeedTestData
    labels: list[datetime]


@dataclass
class Server:
    id: int
    name: str


@dataclass()
class Config:
    ping: int
    download: str
    upload: str
    cron: str
    provider: str
    ookla_id: int
    libre_id: str
    password_level: str
    interface: str
    view_mode: bool
    preview_mode: bool

    def __init__(self, ping: int, download: str, upload: str, cron: str, provider: str, ooklaId: int, libreId: str, passwordLevel: str, interface:str, viewMode: bool, previewMode: bool):
        self.ping = ping
        self.download = download
        self.upload = upload
        self.cron = cron
        self.provider = provider
        self.ookla_id = ooklaId
        self.libre_id = libreId
        self.password_level = passwordLevel
        self.interface = interface
        self.view_mode = viewMode
        self.preview_mode = previewMode

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class FileRepr:
    url: str
    directory_id: int
    type: str
    name: str | None

    time_added: datetime | None = None
    id: UUID | None = None

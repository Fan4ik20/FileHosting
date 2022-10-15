from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class FileRepr:
    url: str
    time_added: datetime
    directory_id: int

    id: UUID | None = None

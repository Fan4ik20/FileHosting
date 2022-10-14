from dataclasses import dataclass


@dataclass
class DirectoryRepr:
    name: str
    user_id: int

    id: int | None = None

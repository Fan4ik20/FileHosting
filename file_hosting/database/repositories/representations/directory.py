from dataclasses import dataclass


@dataclass
class DirectoryRepr:
    name: str
    user_id: int

    directory_id: int | None = None
    inner_dirs: list | None = None
    id: int | None = None

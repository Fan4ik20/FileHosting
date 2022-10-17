from enum import Enum


class FileTypeEnum(str, Enum):
    file = 'file'
    image = 'image'
    video = 'video'
    music = 'music'

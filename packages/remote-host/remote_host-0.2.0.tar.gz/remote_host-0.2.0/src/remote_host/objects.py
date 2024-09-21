from dataclasses import dataclass


@dataclass
class DirectoryObject:
    name: str
    path: str


@dataclass
class FileObject:
    name: str
    path: str
    size: int

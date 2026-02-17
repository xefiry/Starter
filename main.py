from __future__ import annotations

import tomllib
from enum import Enum


class EntryType(Enum):
    Unknown = 0
    StartOne = 1
    StartMany = 2
    Stop = 3

    @staticmethod
    def from_str(input_type: str) -> EntryType:
        type = input_type.lower()

        if type == "startone":
            return EntryType.StartOne
        elif type == "startmany":
            return EntryType.StartMany
        elif type == "stop":
            return EntryType.Stop
        else:
            return EntryType.Unknown

    def __str__(self) -> str:
        if self == EntryType.Unknown:
            return "Unknown"
        elif self == EntryType.StartOne:
            return "StartOne"
        elif self == EntryType.StartMany:
            return "StartMany"
        elif self == EntryType.Stop:
            return "Stop"
        else:
            return "???"


class Entry:
    def __init__(
        self,
        type: EntryType,
        name: str | None,
        path: str | None,
        exe: str,
        args: list | None,
        cwd: str | None,
    ) -> None:
        self.type: EntryType = type  # Mandatory
        self.name: str | None = name  # Optionnal
        self.path: str | None = path  # Optionnal ?
        self.exe: str = exe  # Mandatory
        self.args: list | None = args  # Mandatory for StartOne/StartMany
        self.cwd: str | None = cwd  # Optionnal

    @staticmethod
    def from_toml(data: dict) -> Entry:
        type_str = data.get("type")
        if type_str is None:
            raise Exception("type cannot be empty")
        type = EntryType.from_str(type_str)
        if type == EntryType.Unknown:
            raise Exception(f"Unknown type : {type_str}")

        name = data.get("name")

        path = data.get("path")

        exe = data.get("exe")
        if exe is None:
            raise Exception("exe cannot be empty")

        # TODO: check if empty for StartOne/StartMany
        args = data.get("args")

        cwd = data.get("cwd")

        return Entry(type, name, path, exe, args, cwd)

    def __str__(self) -> str:
        return f"""type = {self.type}
name = {self.name}
path = {self.path}
exe  = {self.exe}
args = {self.args}
cwd  = {self.cwd}
"""


def main():
    with open("config.toml", "rb") as f:
        toml_data = tomllib.load(f)

    for nb, data in enumerate(toml_data["entry"]):
        try:
            entry = Entry.from_toml(data)
            print(entry)
        except Exception as e:
            print(f"Error in rule {nb} : {e}")


if __name__ == "__main__":
    main()

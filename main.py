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


class Entry:
    def __init__(
        self,
        type: EntryType,
        name: str,
    ) -> None:
        self.type = type  # Mandatory
        self.name = name  # Optionnal
        self.path = None  # Mandatory ?
        self.exe = None  # Mandatory
        self.args = None  # Mandatory
        self.cwd = None  # Optionnal

    @staticmethod
    def from_toml(data: dict) -> Entry:
        return Entry(EntryType.from_str(data.get("type")), data.get("name"))

    def __str__(self) -> str:
        return f"{self.type} - {self.name}"


def main():
    with open("config.toml", "rb") as f:
        toml_data = tomllib.load(f)

    for data in toml_data["entry"]:
        entry = Entry.from_toml(data)
        print(entry)


if __name__ == "__main__":
    main()

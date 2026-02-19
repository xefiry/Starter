from __future__ import annotations

import tomllib
from enum import Enum

import utils


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
        exe: str,
        path: str | None,
        args: list | None,
        cwd: str | None,
    ) -> None:
        self.type: EntryType = type  # Mandatory
        self.exe: str = exe  # Mandatory
        self.path: str | None = path  # Optionnal ?
        self.args: list | None = args  # Mandatory for StartMany
        self.cwd: str | None = cwd  # Optionnal

    @staticmethod
    def from_toml(data: dict) -> Entry:
        type_str = str(utils.get_key(data, "type", str, True))
        type = EntryType.from_str(type_str)
        if type == EntryType.Unknown:
            raise Exception(f"Unknown type : {type_str}")

        exe = utils.get_key(data, "exe", str, True)

        path = utils.get_key(data, "path", str)
        path = utils.norm_path(path)  # type: ignore

        args = data.get("args")
        if type == EntryType.StartOne:
            args = utils.process_args(args)
        elif type == EntryType.StartMany:
            args = utils.process_args_list(args)

        cwd = utils.get_key(data, "cwd", str)
        cwd = utils.norm_path(cwd)  # type: ignore

        return Entry(type, exe, path, args, cwd)  # type: ignore

    def __str__(self) -> str:
        return f"""type = {self.type}
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

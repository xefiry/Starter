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
        threshold: int,
        wait_before: int,
        wait_after: int,
    ) -> None:
        self.type: EntryType = type  # Mandatory
        self.exe: str = exe  # Mandatory
        self.path: str | None = path  # Optionnal ?
        self.args: list | None = args  # Mandatory for StartMany
        self.cwd: str | None = cwd  # Optionnal
        self.threshold: int = threshold
        self.wait_before: float = wait_before
        self.wait_after: float = wait_after

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

        threshold = utils.get_key(data, "threshold", int, default_value=0)
        wait_before = utils.get_key(data, "wait_before", float, default_value=0.0)
        wait_after = utils.get_key(data, "wait_after", float, default_value=0.0)

        return Entry(type, exe, path, args, cwd, threshold, wait_before, wait_after)  # type: ignore

    def __str__(self) -> str:
        result = f"type = {self.type}\n"
        result += f"exe  = {self.exe}\n"

        if self.path is not None:
            result += f"path = {self.path}\n"
        if self.args is not None:
            result += f"args = {self.args}\n"
        if self.cwd is not None:
            result += f"cwd  = {self.cwd}\n"

        if self.threshold != 0:
            result += f"threshold = {self.threshold}\n"
        if self.wait_before != 0:
            result += f"wait_before = {self.wait_before}\n"
        if self.wait_after != 0:
            result += f"wait_after = {self.wait_after}\n"

        return result


def main():
    with open("config.toml", "rb") as f:
        toml_data = tomllib.load(f)

    for nb, data in enumerate(toml_data["entry"]):
        try:
            entry = Entry.from_toml(data)
            print(entry)
        except Exception as e:
            print(f"Error in rule {nb} : {e}\n")


if __name__ == "__main__":
    main()

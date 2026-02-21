from __future__ import annotations

import time
from enum import Enum

import arguments
import utils

VERBOSE = arguments.cli_args.verbose
DRY_RUN = arguments.cli_args.dry_run


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
        args: list,
        cwd: str | None,
        threshold: int,
        wait_before: float,
        wait_after: float,
    ) -> None:
        self.type: EntryType = type
        self.exe: str = exe
        self.path: str | None = path
        self.args: list = args
        self.cwd: str | None = cwd
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
        # if not defined, use the same as path
        if cwd is None:
            cwd = path
        else:
            cwd = utils.norm_path(cwd)  # type: ignore

        threshold = utils.get_key(data, "threshold", int, default_value=0)
        wait_before = utils.get_key(data, "wait_before", float, default_value=0.0)
        wait_after = utils.get_key(data, "wait_after", float, default_value=0.0)

        return Entry(type, exe, path, args, cwd, threshold, wait_before, wait_after)  # type: ignore

    def run(self):
        if self.type in [EntryType.StartOne, EntryType.StartMany]:
            self.start_it()
        elif self.type == EntryType.Stop:
            self.stop_it()

    def stop_it(self):
        proc_list = utils.get_proc_list(self.exe)

        if len(proc_list) == 0:
            print(f"{self.exe:20} -> not running")
        else:
            for proc in proc_list:
                if VERBOSE:
                    info = f" (PID {proc.pid:5})"
                else:
                    info = ""
                print(f"{proc.name():20} -> terminated{info}")

                if not DRY_RUN:
                    proc.terminate()

    def start_it(self):
        nb_proc = len(utils.get_proc_list(self.exe))

        if nb_proc > self.threshold:
            if VERBOSE:
                info = f" {nb_proc} time(s)"
            else:
                info = ""
            print(f"{self.exe:20} -> already running{info}")

        else:
            if self.wait_before > 0 and not DRY_RUN:
                time.sleep(self.wait_before)

            if self.type == EntryType.StartOne:
                if VERBOSE:
                    print(self.path, self.exe, self.args)
                if not DRY_RUN:
                    utils.do_run(self.exe, self.path, self.args, self.cwd)
                print(f"{self.exe:20} -> started")

            elif self.type == EntryType.StartMany:
                for nb, args in enumerate(self.args):
                    if VERBOSE:
                        print(self.path, self.exe, args)
                    if not DRY_RUN:
                        utils.do_run(self.exe, self.path, args, self.cwd)
                    print(f"{self.exe:20} -> started (args {nb + 1})")

            if self.wait_after > 0 and not DRY_RUN:
                time.sleep(self.wait_after)

    def __str__(self) -> str:
        result = f"type = {self.type}"
        result += f"\nexe  = {self.exe}"

        if self.path is not None:
            result += f"\npath = {self.path}"
        if self.args is not None:
            result += f"\nargs = {self.args}"
        if self.cwd is not None:
            result += f"\ncwd  = {self.cwd}"
        if self.threshold != 0:
            result += f"\nthreshold = {self.threshold}"
        if self.wait_before != 0:
            result += f"\nwait_before = {self.wait_before}"
        if self.wait_after != 0:
            result += f"\nwait_after = {self.wait_after}"

        return result

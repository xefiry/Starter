from __future__ import annotations

import time
from enum import Enum

import arguments
import utils

VERBOSE: bool = arguments.cli_args.verbose
DRY_RUN: bool = arguments.cli_args.dry_run
FORCE: bool = arguments.cli_args.force


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
    MAX_LENGTH: int = 0

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
        cli_mode: bool,
    ) -> None:
        self.type: EntryType = type
        self.exe: str = exe
        self.path: str | None = path
        self.args: list = args
        self.cwd: str | None = cwd
        self.threshold: int = threshold
        self.wait_before: float = wait_before
        self.wait_after: float = wait_after
        self.cli_mode: bool = cli_mode

        # update max exe length for later printing
        if Entry.MAX_LENGTH < len(self.exe):
            Entry.MAX_LENGTH = len(self.exe)

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
            args = [utils.process_args(args)]
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
        cli_mode = utils.get_key(data, "cli_mode", bool, default_value=False)

        return Entry(
            type,
            exe,
            path,
            args,  # type: ignore
            cwd,
            threshold,
            wait_before,
            wait_after,
            cli_mode,
        )

    def run(self):
        if self.type in [EntryType.StartOne, EntryType.StartMany]:
            self.start()
        elif self.type == EntryType.Stop:
            self.stop()

    def stop(self):
        proc_list = utils.get_proc_list(self.exe)

        if len(proc_list) == 0:
            print(f"{self.exe.ljust(Entry.MAX_LENGTH, ' ')} -> not running")
        else:
            for proc in proc_list:
                exe_name = proc.name().ljust(Entry.MAX_LENGTH, " ")
                if VERBOSE:
                    info = f" (PID {proc.pid})"
                else:
                    info = ""

                result = "terminated"
                if not DRY_RUN:
                    try:
                        proc.terminate()
                    except Exception:
                        result = "ERROR: could not terminate"

                print(f"{exe_name} -> {result}{info}")

    def start(self):
        nb_proc = len(utils.get_proc_list(self.exe))
        exe_name = self.exe.ljust(Entry.MAX_LENGTH, " ")

        if nb_proc > self.threshold and not FORCE:
            if VERBOSE:
                info = f" {nb_proc} time(s)"
            else:
                info = ""
            print(f"{exe_name} -> already running{info}")

        else:
            if self.wait_before > 0 and not DRY_RUN:
                time.sleep(self.wait_before)

            for args in self.args:
                result = "done" if self.cli_mode else "started"

                if VERBOSE:
                    print(self.path, self.exe, args)
                if not DRY_RUN:
                    try:
                        utils.do_run(self.exe, self.path, args, self.cwd, self.cli_mode)
                    except Exception as e:
                        result = f"ERROR: {e}"
                print(f"{exe_name} -> {result}")

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
        if self.cli_mode != 0:
            result += f"\ncli_mode = {self.cli_mode}"

        return result

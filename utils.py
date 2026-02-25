import os
import subprocess
import tomllib
from typing import Any

import psutil


def load_toml(filepath: str) -> dict[str, Any]:
    try:
        with open(filepath, "rb") as f:
            toml_data = tomllib.load(f)
    except FileNotFoundError:
        print(f"toml file not found : {filepath}")
        exit(-1)

    return toml_data


def print_version():
    toml_data = load_toml("pyproject.toml")
    print(f"starter version {toml_data['project']['version']}")


def norm_path(path: str | None) -> str | None:
    """Expand variables and normalize path. If Null is given, null will be returned."""

    if path is None:
        return None
    else:
        return os.path.normpath(os.path.expandvars(path))


def get_proc_list(exe: str) -> list[psutil.Process]:
    return [x for x in psutil.process_iter(["name"]) if x.info["name"] == exe]


def do_run(
    exe: str, path: str | None, args: list[str], cwd: str | None, cli_mode: bool
):
    if path is not None:
        exe_path = os.path.join(path, exe)
    else:
        exe_path = exe

    arg_list = [exe_path] + args

    if cli_mode:
        subprocess.run(args=arg_list, cwd=cwd)
    else:
        subprocess.Popen(args=arg_list, cwd=cwd, stdout=subprocess.DEVNULL)


def get_key(
    data: dict,
    key: str,
    expected_type: type,
    mandatory: bool = False,
    default_value: Any = None,
) -> Any:
    """Get key from a dict.

    Args:
        data (dict): The dict to retrieve from.
        key (str): The key to retrieve.
        expected_type (type): The expected type for the result.
        mandatory (bool, optional): Is the value mandator. Defaults to False.\n
            If true, raises exception in case of value not found.\n
            If false, allows return of None.
        default_value (Any, optional): If set, and result is None, replace it with default_value.\n
            Makes mandatory param redundant. Defaults to None.

    Raises:
        KeyError: If the key is not found (and mandatory is True).
        TypeError: If the value found is not of expected_type.

    Returns:
        Any: The value found.
    """
    result = data.get(key)

    # If key has no value
    if result is None:
        # if we ask for a default value, we use it
        if default_value is not None:
            result = default_value

        # if a value is mandatory, error
        elif mandatory:
            raise KeyError(f"Key {key} was not found")

    # if result is not of expected type (and not None)
    if result is not None and not isinstance(result, expected_type):
        raise TypeError(f"Key {key} is not {expected_type}")

    return result


def is_str_list(input_list: list) -> bool:
    """Check if the given list is a string list.

    Args:
        input_list (list): A list to check.

    Returns:
        bool: True if the list contains only strings (str) or is empty.
    """
    for item in input_list:
        if not isinstance(item, str):
            return False
    return True


def process_args(input: list[str] | str | None) -> list[str]:
    """Processes an input into a list of arguments usable by subprocess.run/subprocess.Popen.

    Args:
        input (list[str] | str | None): The input to be processed.

    Raises:
        TypeError: If the input contains invalid type.

    Returns:
        list[str]: The processed list, ready to be used by subprocess.run/subprocess.Popen.

    Examples:
        process_args(null) = []
        process_args([]) = []
        process_args("arg") = ["arg"]
        process_args(["arg"]) = ["arg"]
        process_args(["arg1", "arg2"]) = ["arg1", "arg2"]
    """
    result = []

    if input is None:
        result = []
    elif isinstance(input, str):
        result.append(os.path.expandvars(input))
    elif isinstance(input, list) and is_str_list(input):
        for i in input:
            result.append(os.path.expandvars(i))
    else:
        raise TypeError("Invalid args")

    return result


def process_args_list(input) -> list[list[str]]:
    """Processes an input into a list of list of arguments usable to loop
    and call by subprocess.run/subprocess.Popen.

    Returns:
        list[list[str]]: The processed list, ready to be looped to use by subprocess.run/subprocess.Popen.

    Examples:
    process_args_list(["argA1", "argB1"]) = [["argA1"], ["argB1"]]
    process_args_list([["argA1"], ["argB1"]]) = [["argA1"], ["argB1"]]
    process_args_list([["argA1", "argA2"], ["argB1", "argB2"]]) = [["argA1", "argA2"], ["argB1", "argB2"]]
    process_args_list([["argA1", "argA2"], ["argB1"], "argC1"]) = [["argA1", "argA2"], ["argB1"], ["argC1"]]
    """
    result = []

    if not isinstance(input, list):
        raise TypeError("Invalid args")

    for item in input:
        result.append(process_args(item))

    return result

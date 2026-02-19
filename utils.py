def get_key(
    data: dict, key: str, expected_type: type, mandatory: bool = False
) -> object:
    result = data.get(key)

    # if result is mandatory, it can't be None
    if result is None and mandatory:
        raise KeyError(f"Key {key} was not found")

    # if result is not of expected type (and not None)
    if result is not None and not isinstance(result, expected_type):
        raise TypeError(f"Key {key} is not {expected_type}")

    return result


def is_str_list(input_list: list) -> bool:
    """Check if the given list is a string list

    Args:
        input_list (list): A list to check

    Returns:
        bool: True if the list contains only strings (str) or is empty
    """
    for item in input_list:
        if not isinstance(item, str):
            return False
    return True


def process_args(input: list[str] | str | None) -> list[str]:
    """Processes an input into a list of arguments usable by subprocess.run/subprocess.Popen

    Args:
        input (list[str] | str | None): the input to be processed

    Raises:
        TypeError: if the input contains invalid type

    Returns:
        list[str]: the processed list, ready to be used by subprocess.run/subprocess.Popen

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
        result = [input]
    elif isinstance(input, list) and is_str_list(input):
        result = input
    else:
        raise TypeError("Invalid args")

    return result


def process_args_list(input) -> list[list[str]]:
    """Processes an input into a list of list of arguments usable to loop
    and call by subprocess.run/subprocess.Popen

    Returns:
        list[list[str]]: the processed list, ready to be looped to use by subprocess.run/subprocess.Popen

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

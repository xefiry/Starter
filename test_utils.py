import pytest

import utils


@pytest.mark.parametrize(
    "input,expected",
    [
        ([], True),
        (["arg"], True),
        (["arg1", "arg2"], True),
        (["arg1", 3], False),
        ([3], False),
        ([False], False),
        ([6.5, "Ok ?"], False),
        ([["Ok ?"]], False),
    ],
)
def test_is_str_list(input, expected):
    assert utils.is_str_list(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        (None, []),
        ([], []),
        ("arg", ["arg"]),
        (["arg"], ["arg"]),
        (["arg1", "arg2"], ["arg1", "arg2"]),
    ],
)
def test_process_args(input, expected):
    assert utils.process_args(input) == expected


@pytest.mark.parametrize("input", [[3], 3, False])
def test_process_args_exceptions(input):
    with pytest.raises(TypeError):
        utils.process_args(input)


@pytest.mark.parametrize(
    "input,expected",
    [
        (["argA1", "argB1"], [["argA1"], ["argB1"]]),
        ([["argA1"], ["argB1"]], [["argA1"], ["argB1"]]),
        (
            [["argA1", "argA2"], ["argB1", "argB2"]],
            [["argA1", "argA2"], ["argB1", "argB2"]],
        ),
        (
            [["argA1", "argA2"], ["argB1"], "argC1"],
            [["argA1", "argA2"], ["argB1"], ["argC1"]],
        ),
    ],
)
def test_process_args_list(input, expected):
    assert utils.process_args_list(input) == expected


@pytest.mark.parametrize("input", [[3], 3, False, ["ok", 3]])
def test_process_args_list_exception(input):
    with pytest.raises(TypeError):
        utils.process_args_list(input)

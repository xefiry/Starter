import argparse

_parser = argparse.ArgumentParser()

_parser.add_argument(
    "config_file",
    nargs="?",  # optionnal argument
    default="config.toml",
    help="config file to use (default: config.toml)",
)

_parser.add_argument(
    "-V",
    "--version",
    action="store_true",
    help="show version number and exit",
)

_parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="verbose mode",
)

_parser.add_argument(
    "-d",
    "--dry_run",
    action="store_true",
    help="dry run (nothing done, only printing)",
)

_parser.add_argument(
    "-f",
    "--force",
    action="store_true",
    help="do not check if executables are already running",
)

_parser.add_argument(
    "-s",
    "--sleep",
    help="sleep for N seconds at the end",
    type=int,
    metavar=("N"),
)

cli_args = _parser.parse_args()

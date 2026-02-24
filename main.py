import time

import arguments
import utils
from entry import Entry

CONFIG_FILE: str = arguments.cli_args.config_file
DRY_RUN: bool = arguments.cli_args.dry_run
SLEEP: int = arguments.cli_args.sleep
VERSION: bool = arguments.cli_args.version


def main():
    if VERSION:
        utils.print_version()
        exit(0)

    toml_data = utils.load_toml(CONFIG_FILE)

    if DRY_RUN:
        print("Dry run. Print only.")

    entries = []

    # First, load all entries.
    # It will ensure Entry.MAX_LENGTH to be set for later printing.
    for nb, data in enumerate(toml_data["entry"]):
        try:
            entries.append(Entry.from_toml(data))
        except Exception as e:
            print(f"Error loading entry {nb} : {e}")

    # Then execute all entries
    for entry in entries:
        entry.run()

    if SLEEP is not None and SLEEP > 0:
        print(f"sleeping for {SLEEP} s")
        time.sleep(SLEEP)

    print("done")


if __name__ == "__main__":
    main()

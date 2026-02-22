import time

import arguments
import utils
from entry import Entry

CONFIG_FILE = arguments.cli_args.config_file
DRY_RUN = arguments.cli_args.dry_run
SLEEP = arguments.cli_args.sleep
VERSION = arguments.cli_args.version


def main():
    if VERSION:
        utils.print_version()
        exit(0)

    toml_data = utils.load_toml(CONFIG_FILE)

    if DRY_RUN:
        print("Dry run. Print only.")

    for nb, data in enumerate(toml_data["entry"]):
        try:
            entry = Entry.from_toml(data)
            entry.run()
        except Exception as e:
            print(f"Error in rule {nb} : {e}")

    if SLEEP is not None and SLEEP > 0:
        print(f"sleeping for {SLEEP} s")
        time.sleep(SLEEP)

    print("done")


if __name__ == "__main__":
    main()

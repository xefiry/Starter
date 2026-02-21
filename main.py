import time
import tomllib

import arguments
from entry import Entry

CONFIG_FILE = arguments.cli_args.config_file
DRY_RUN = arguments.cli_args.dry_run
SLEEP = arguments.cli_args.sleep


def main():
    try:
        with open(CONFIG_FILE, "rb") as f:
            toml_data = tomllib.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found : {CONFIG_FILE}")
        exit(-1)

    if DRY_RUN:
        print("Dry run. Print only.")

    for nb, data in enumerate(toml_data["entry"]):
        try:
            entry = Entry.from_toml(data)
            entry.run()
        except Exception as e:
            print(f"Error in rule {nb} : {e}\n")

    if SLEEP is not None and SLEEP > 0:
        print(f"sleeping for {SLEEP} s")
        time.sleep(SLEEP)

    print("done")


if __name__ == "__main__":
    main()

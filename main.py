import tomllib

from entry import Entry


def main():
    try:
        with open("config.toml", "rb") as f:
            toml_data = tomllib.load(f)
    except FileNotFoundError:
        print("config.toml not found")
        exit(-1)

    for nb, data in enumerate(toml_data["entry"]):
        try:
            entry = Entry.from_toml(data)
            entry.run()
        except Exception as e:
            print(f"Error in rule {nb} : {e}\n")


if __name__ == "__main__":
    main()

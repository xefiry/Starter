import tomllib


def main():
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)

    print(data)
    for entry in data["entry"]:
        print(entry)
        args = entry.get("args")
        print(args)
        if len(args) > 0:
            print(type(args[0]))
        print()


if __name__ == "__main__":
    main()

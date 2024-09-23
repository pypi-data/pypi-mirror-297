import sys
import docker
from functools import partial


def search_sorter(search_term: str, container) -> int:
    try:
        return f"{container.id} {container.name}".index(search_term)
    except ValueError:
        return -1


def help() -> None:
    print("Usage:")
    print("aliased : docker-nuke <search-term>")
    print("python  : python -m docker-nuke <search-term>")
    print("\t<search-term>: partial or whole, name or id")


def main() -> None:
    args = sys.argv[1::]

    if len(args) < 1:
        help()
        return

    search_term = "".join(args)
    client = docker.from_env()

    containers: list = client.containers.list()

    search_key = partial(search_sorter, search_term)
    containers.sort(key=search_key, reverse=True)

    lock = containers[0]

    print(f"Target Locked: {lock.id} {lock.name}")
    user_input = input("Fire? (y/N) ")
    if user_input.lower() != "y":
        print("X Cancelling launch sequence")
        return

    print("Launching")

    lock.kill()
    lock.remove()

    print("All splash")

    # print(", ".join(list(map(lambda c: c.name, containers))))


if __name__ == "__main__":
    main()

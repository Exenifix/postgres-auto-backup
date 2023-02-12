import json
from typing import Callable, Type, TypeVar

from exencolor import Color, Decoration, colored

T = TypeVar("T")


def get_input(
    txt: str | None = None, f: Callable[[str], T] | Type[T] | None = None, *, error_txt: str | None = None
) -> T:
    if f is None:
        return input(txt)
    error_txt = colored(error_txt or "Bad input, please try again", foreground=Color.BRIGHT_RED)
    while True:
        # noinspection PyBroadException
        try:
            return f(input(txt))
        except Exception:
            print(error_txt)


print(
    colored(
        "Welcome to PostgresAutoBackup setup!",
        foreground=Color.BRIGHT_CYAN,
        decoration=Decoration.BOLD,
    )
)
instance_name = input(colored("Please specify instance name: ", foreground=Color.BRIGHT_YELLOW)).strip()
dbs: list[str] = get_input(
    colored(
        "Please input the list of databases you would like to backup, comma-separated: ",
        foreground=Color.BRIGHT_YELLOW,
    ),
    lambda x: [s.strip() for s in x.split(",")],
)
url = input(colored("Please provide Discord webhook URL: ", foreground=Color.BRIGHT_YELLOW)).strip()
if "?wait=" not in url:
    url += "?wait=true"
with open("config.json", "w") as f:
    json.dump({"name": instance_name, "dbs": dbs, "webhook": url, "last_backup": None}, f)
    print(colored("Setup complete! Use `sudo ./run.sh` to start the script"))

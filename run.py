import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

import requests
from exencolorlogs import Logger

log = Logger("APP")
log.info("Loading config...")

with open("./config.json", "r") as f:
    config: dict[str, str | list[str] | int | None] = json.load(f)


instance_name: str = config["name"]
dbs: list[str] = config["dbs"]
webhook: str = config["webhook"]
last_backup: int | None = config["last_backup"]

log.ok("Config loaded successfully!")

while True:
    time.sleep(1)
    ctime = int(time.time())
    if not (last_backup is None or ctime - last_backup >= 24 * 60 * 60):
        continue
    last_backup = config["last_backup"] = ctime
    with open("./config.json", "w") as f:
        json.dump(config, f)
    log.info("Creating backup for %d databases...", len(dbs))
    names = []
    for db in dbs:
        try:
            start = time.perf_counter()
            subprocess.run(
                [
                    "pg_dump",
                    db,
                    "-f",
                    fname := f"{instance_name}-{db}-{datetime.now().date()}.sql",
                ],
                check=True,
            )
            names.append(fname)
            file = Path(fname)
            t = time.perf_counter() - start
            log.ok(
                "%s backup successful. File size: %fKB, time taken: %fs",
                db,
                file.stat().st_size / 1024,
                t,
            )
        except Exception as e:
            log.error("Unexpected exception during backup of %s", db, exc_info=e)
    log.info("Uploading files to discord...")
    r = requests.post(
        webhook,
        json={"content": f"Backup for {datetime.now().date()} from {instance_name}"},
        files={n: Path(n).read_bytes() for n in names},
    )
    if r.status_code != 200:
        log.error(
            "Error occurred when attempting to send webhook: %d %s",
            r.status_code,
            r.json()["message"],
        )
    else:
        log.ok("Files uploaded to webhook successfully!")
    subprocess.run(["rm"] + names, check=True)
    log.ok("Files were removed")

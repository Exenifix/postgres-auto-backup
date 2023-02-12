#!/bin/bash
set -e

export POETRY_VIRTUALENVS_PATH=./venv

printf "Configuring virtual environment...\n"
python3 -m venv ./venv
poetry install --only main
printf "Virtual environment configured successfully!\n\n"

printf "Setting up service...\n"
WORKDIR=$(pwd)
TEXT="[Unit]
Description=Automatic Postgres databases backup to Discord

[Service]
ExecStart=/bin/bash -c \"poetry run python3 ./run.py\"
WorkingDirectory=$WORKDIR
Restart=always
User=root

[Install]
WantedBy=multi-user.target

[Service]
Environment=POETRY_VIRTUALENVS_PATH=$WORKDIR/venv"
echo "$TEXT" | sudo tee /etc/systemd/system/postgres-auto-backup.service
sudo systemctl daemon-reload
printf "Service setup successfully!\n\n"

printf "Now please configure program...\n"
poetry run python3 ./install.py

#!/bin/bash
set -e

if [ ! -f ./config.json ]; then
  printf "install.sh has not been completed"
  exit 1
fi

printf "Starting service...\n"
sudo systemctl enable postgres-auto-backup.service
sudo systemctl start postgres-auto-backup.service
printf "Service started successfully!\n"

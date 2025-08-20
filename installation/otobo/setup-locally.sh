#!/bin/bash

# region Script initialization
set -o errtrace

trap 'echo "Error at line ${LINENO}: Command \"${BASH_COMMAND}\" failed." >&2' ERR
# region Helper functions

usage() {
    echo "Usage: $(basename "$0") [--overwrite] [--help]" >&2
    exit 1
}

help_message() {6
    echo "Usage: $(basename "$0") [--overwrite] [--help]"
    echo ""
    echo "--overwrite   Remove existing OTOBO installation and all data before running updates."
    echo "              Otherwise, only perform database updates and performance settings."
    echo ""
    echo "-y            Auto accept overwriting"
    echo "--help        Display this help message."
    exit 0
}

# endregion

# region Parse command line arguments
OTOBO_WEB_VOLUME="/var/lib/docker/volumes/otobo_opt_otobo/_data"
LOCAL_DIR="/tmp/installation"
OTOBO_DIR="/opt/otobo-docker"

export OTOBO_WEB_VOLUME
export LOCAL_DIR
export OTOBO_DIR

OVERWRITE=0
ALWAYS_YES=0
for arg in "$@"; do
    case "$arg" in
        --help)
            help_message
            ;;
        --overwrite)
            OVERWRITE=1
            ;;
        -y)
            ALWAYS_YES=1
            ;;
        *)
            echo "Unknown option: $arg" >&2
            usage
            ;;
    esac
done

# endregion

# region Check for elevated privileges

if [ "$EUID" -ne 0 ]; then
    echo "Error: This script requires elevated privileges. Please run as root (or with sudo)." >&2
    exit 1
fi

# endregion

# region Warning and confirmation (only if --overwrite is set)

if [ "$OVERWRITE" -eq 1 ]; then
    if [ "$ALWAYS_YES" -ne 1 ]; then
        echo "WARNING: Running with --overwrite will remove the current OTOBO installation and all data."
        read -rp "Are you sure you want to continue? (y/N): " confirm
        [[ "$confirm" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 1; }
    else
        echo "WARNING: Running with --overwrite and -y flag; proceeding without confirmation."
    fi
else
    echo "Running without '--overwrite' flag; will only update the database and performance settings."
fi

# endregion


# shellcheck disable=SC1090
source ~/.bashrc || true
# region setting DB root password
if [ -z "${OTOBO_DB_ROOT_PASSWORD:-}" ]; then
    if [ "$OVERWRITE" -eq 1 ]; then
        # 8 characters out of 62 possible characters, 3,2e14 possible combinations
        OTOBO_DB_ROOT_PASSWORD=$(openssl rand -base64 32 | tr -dc 'A-Za-z0-9\*' | head -c8)
        echo "export OTOBO_DB_ROOT_PASSWORD=${OTOBO_DB_ROOT_PASSWORD}" >> ~/.bashrc
        echo "DB Root Password: ${OTOBO_DB_ROOT_PASSWORD}"
        # shellcheck disable=SC1090
        source ~/.bashrc || true
    else
        echo "Warning: OTOBO_DB_ROOT_PASSWORD is not set and --overwrite flag was not given." >&2
        exit 1
    fi
fi
# endregion

./installing-docker.sh
./installing-docker-images.sh
docker compose up --detach
docker compose stop daemon
docker compose exec web bash -c "rm -f Kernel/Config/Files/ZZZAAuto.pm ; bin/docker/quick_setup.pl --db-password ${OTOBO_DB_ROOT_PASSWORD}"
docker compose exec web bash -c "bin/docker/run_test_suite.sh"
docker compose start daemon

# region copying docker compose file to /opt
mkdir -p /opt
cp -r "$LOCAL_DIR/otobo-docker" /opt/
# endregion

# region pruning docker if --overwrite is set, removes old containers and volumes! Be careful
if [ "$OVERWRITE" -eq 1 ]; then
    docker compose -f "$OTOBO_DIR/compose.yml" down -v
    docker system prune -a --volumes -f
fi
# endregion

# region starting docker compose
cd "$OTOBO_DIR" || exit 1
docker compose up -d --build
# endregion


# region upgrading MariaDB and restarting containers; updates db to latest version
echo "Upgrading MariaDB and restarting containers..."
docker compose up -d --build
docker exec otobo-db-1 mariadb-upgrade --password="${OTOBO_DB_ROOT_PASSWORD}"
docker compose down && docker compose up -d --build
# endregion

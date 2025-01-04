#!/bin/bash
set -e

USER=odoo
ODDO_DEBUGPY_PORT=5678
#DEBUG_FILE = "/var/debug/shell_server.log"

function log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> /odoo/var/debug/shell_server.log
}

log "Starting entrypoint.sh"

function run_command() {
    if ! [ $(id -u) = 0 ]; then
        log "Running command as root: $1"
        sudo -ES su -c "$1"
    else
        log "Running command as $USER: $1"
        $1
    fi
}

if [ -n "$UID" ] && [ -n "$GID" ]; then
    if ! [ $(id -u) = 0 ]; then
        log "Changing UID to $UID and GID to $GID for user $USER"
        run_command "usermod -u $UID $USER && groupmod -g $GID $USER"
        run_command "chown $USER:$USER /var/lib/odoo"
    fi
fi

log "pip install -r requirements.txt"
pip install -r requirements.txt

DB_ARGS=()
if [ -n "$DEV_FEATURES" ]; then
    DB_ARGS+=("--dev")
    DB_ARGS+=("${DEV_FEATURES}")
fi

if [ -n "$DEBUGPY_PORT" ]; then
    ODDO_DEBUGPY_PORT=$DEBUGPY_PORT
fi
# Log DB ARGS
log "DB_ARGS: ${DB_ARGS[@]}"

case "$1" in
    -- | odoo-bin)
        shift
        if [[ "$1" == "scaffold" ]] ; then
            log "Running scaffold with arguments: $@"
            python odoo-bin "$@"
        else
            if [ -n "$DEBUGPY_ENABLE" ]; then
                log "Starting Odoo with debugpy on port ${ODDO_DEBUGPY_PORT}"
                python -m debugpy --listen 0.0.0.0:${ODDO_DEBUGPY_PORT} odoo-bin "$@" "${DB_ARGS[@]}"
            else
                log "Starting Odoo"
                python odoo-bin "$@" "${DB_ARGS[@]}"
            fi
        fi
        ;;
    -*)
        if [ -n "$DEBUGPY_ENABLE" ]; then
              log "Starting Odoo with debugpy on port ${ODDO_DEBUGPY_PORT} with arguments: $@"
              log "if DB_ARGS: ${DB_ARGS[@]}"
              python -m debugpy --listen 0.0.0.0:${ODDO_DEBUGPY_PORT} odoo-bin "$@" "${DB_ARGS[@]}"
          else
              log "Starting Odoo with arguments: $@"
              log "else DB_ARGS: ${DB_ARGS[@]}"
              python odoo-bin "$@" "${DB_ARGS[@]}"
          fi
        ;;
    *)
        log "Executing command: $@"
        exec "$@"
esac

exit 1

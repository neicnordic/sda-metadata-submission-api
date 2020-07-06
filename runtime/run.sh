#!/bin/bash

# Runner script for alq-api.


# Resolve directories and paths.

DIR="$(realpath "$(dirname "$0")")"
WAITER=${DIR}/wait-for-it.sh
CONFIG=${DIR}/gunicorn.conf

TIMEOUT=${CGE_QUERY_API_TIMEOUT:-60}

# Broker host and port.
MONGODB_HOST=${CGE_QUERY_API_MONGODB_HOST:-localhost}
MONGODB_PORT=${CGE_QUERY_API_MONGODB_PORT:-27017}

# Do the actual waiting.
${WAITER} \
    "${MONGODB_HOST}:${MONGODB_PORT}" \
    -t "${TIMEOUT}"


# Run the service.
exec gunicorn '--config' "${CONFIG}" '-b' '0.0.0.0:8000' 'app:create_app()'
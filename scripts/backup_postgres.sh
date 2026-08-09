#!/usr/bin/env bash
set -euo pipefail

: "${PGDATABASE:?PGDATABASE must be set}"
: "${PGUSER:?PGUSER must be set}"
: "${PGHOST:?PGHOST must be set}"

backup_dir="${1:-backups}"
mkdir -p -- "$backup_dir"
umask 077
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_path="$backup_dir/${PGDATABASE}_${timestamp}.dump"

pg_dump --format=custom --file="$backup_path"
printf 'Created PostgreSQL backup: %s\n' "$backup_path"

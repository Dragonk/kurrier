#!/bin/sh
set -eu

: "${DAV_POSTGRES_USER:?DAV_POSTGRES_USER is required}"
: "${DAV_POSTGRES_PASSWORD:?DAV_POSTGRES_PASSWORD is required}"
: "${DAV_POSTGRES_DB:?DAV_POSTGRES_DB is required}"
: "${DAV_CONFIG_ENCRYPTION_KEY:?DAV_CONFIG_ENCRYPTION_KEY is required}"
: "${DAV_ADMIN_PASSWORD_HASH:?DAV_ADMIN_PASSWORD_HASH is required}"

config_path=/var/www/baikal/config/baikal.yaml

if [ ! -s "$config_path" ]; then
  mkdir -p "$(dirname "$config_path")"
  umask 077
  cat >"$config_path" <<EOF
system:
  configured_version: 0.10.1
  timezone: UTC
  card_enabled: true
  cal_enabled: true
  dav_auth_type: Digest
  admin_passwordhash: "$DAV_ADMIN_PASSWORD_HASH"
  failed_access_message: "user %u authentication failure for Baikal"
  auth_realm: BaikalDAV
  base_uri: ""
  invite_from: noreply@_
database:
  sqlite_file: /var/www/baikal/Specific/db/db.sqlite
  backend: pgsql
  mysql_host: ""
  mysql_dbname: ""
  mysql_username: ""
  mysql_password: ""
  encryption_key: "$DAV_CONFIG_ENCRYPTION_KEY"
  pgsql_host: baikal-postgres
  pgsql_dbname: "$DAV_POSTGRES_DB"
  pgsql_username: "$DAV_POSTGRES_USER"
  pgsql_password: "$DAV_POSTGRES_PASSWORD"
EOF
fi

exec /docker-entrypoint.sh "$@"

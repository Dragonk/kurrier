FROM postgres:18-bookworm

COPY db/init/baikal-init /docker-entrypoint-initdb.d

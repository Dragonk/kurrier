FROM postgres:18-bookworm

COPY db/init/migrations /scripts/migrations
COPY db/init/db-bootstrap.sh /bootstrap/db-bootstrap.sh

RUN chmod 0555 /bootstrap/db-bootstrap.sh

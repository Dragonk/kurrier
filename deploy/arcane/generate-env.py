#!/usr/bin/env python3
"""Generate a local, private .env for the Kurrier Arcane deployment."""

import base64
import hashlib
import os
import secrets
import sys
from pathlib import Path

output_path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(".env")
if len(sys.argv) > 2:
    raise SystemExit("Usage: generate-env.py [output-path]")

postgres_password = secrets.token_urlsafe(32)
dav_postgres_password = secrets.token_urlsafe(32)
app_encryption_key = base64.b64encode(secrets.token_bytes(32)).decode()
dav_admin_password = secrets.token_urlsafe(24)
dav_admin_password_hash = hashlib.sha256(
    f"admin:BaikalDAV:{dav_admin_password}".encode()
).hexdigest()

content = f"""WEB_URL=https://kurrier.kmms.ovh
ZORAXY_PROXY_NETWORK=proxy-network
KURRIER_DATA_DIR=/mnt/Dane/kurrier
KURRIER_IMAGE_TAG=pr-616
NODE_ENV=production
WEB_PORT=3000
DISABLE_DRIVE=false
DISABLE_LOCAL_LOGIN=false
POSTGRES_USER=kurrier
POSTGRES_PASSWORD={postgres_password}
POSTGRES_DB=kurrier
POSTGRES_PORT=5432
POSTGRES_HOST=postgres
DATABASE_URL=postgresql://kurrier:{postgres_password}@postgres:5432/kurrier
DATABASE_RLS_URL=postgresql://kurrier:{postgres_password}@postgres:5432/kurrier
REDIS_PASSWORD={secrets.token_urlsafe(32)}
REDIS_HOST=redis
REDIS_PORT=6379
TYPESENSE_API_KEY={secrets.token_urlsafe(32)}
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
SEARCH_REBUILD_ON_BOOT=false
JWT_SECRET={secrets.token_urlsafe(48)}
APP_SECRET_ENCRYPTION_KEY={app_encryption_key}
S3_REGION=garage
S3_BUCKET=kurrier
S3_ENDPOINT=http://garage:3900
S3_ACCESS_KEY={secrets.token_urlsafe(20)}
S3_SECRET_KEY={secrets.token_urlsafe(32)}
S3_FORCE_PATH_STYLE=true
GARAGE_RPC_SECRET={base64.b64encode(secrets.token_bytes(32)).decode()}
WORKER_URL=http://worker
DAV_URL=http://dav
WEB_DAV_URL=http://dav
DAV_POSTGRES_USER=baikal
DAV_POSTGRES_PASSWORD={dav_postgres_password}
DAV_POSTGRES_DB=baikal
DAV_DATABASE_URL=postgresql://baikal:{dav_postgres_password}@baikal-postgres:5432/baikal
DAV_CONFIG_ENCRYPTION_KEY={secrets.token_hex(16)}
DAV_ADMIN_PASSWORD={dav_admin_password}
DAV_ADMIN_PASSWORD_HASH={dav_admin_password_hash}
OIDC_ISSUER_URL=https://auth.kmms.ovh
OIDC_CLIENT_ID=
OIDC_CLIENT_SECRET=
OIDC_PROVIDER_NAME=Canaille
OIDC_SCOPES=openid email profile
OIDC_TOKEN_AUTH_METHOD=client_secret_basic
OIDC_REQUIRE_VERIFIED_EMAIL=true
API_ADMIN_KEY=
CUSTOM_EMAIL_PROVIDERS=[]
"""

temporary_path = output_path.with_name(f".{output_path.name}.{secrets.token_hex(8)}.tmp")
try:
    file_descriptor = os.open(temporary_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(file_descriptor, "w") as output_file:
        output_file.write(content)
    os.replace(temporary_path, output_path)
finally:
    temporary_path.unlink(missing_ok=True)

print(f"Generated {output_path} with mode 0600. Add only OIDC_CLIENT_ID and OIDC_CLIENT_SECRET.")

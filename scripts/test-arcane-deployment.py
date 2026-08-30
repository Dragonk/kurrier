#!/usr/bin/env python3
"""Static contract checks for the repository-free Arcane deployment bundle."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = (ROOT / "deploy/arcane/compose.yml").read_text()
WORKFLOW = (ROOT / ".github/workflows/pr-test-images.yml").read_text()
BOOTSTRAP = (ROOT / "deploy/images/kurrier-bootstrap.Dockerfile").read_text()
BAIKAL = (ROOT / "deploy/images/kurrier-baikal.Dockerfile").read_text()
ENTRYPOINT = (ROOT / "deploy/images/baikal/entrypoint.sh").read_text()
GENERATOR = (ROOT / "deploy/arcane/generate-env.py").read_text()
GENERIC_OIDC_CALLBACK = (
    ROOT / "apps/web/app/api/auth/oidc/generic/callback/route.ts"
).read_text()

assert "KURRIER_REPO_DIR" not in COMPOSE
assert "/db/init" not in COMPOSE
assert "ports:" not in COMPOSE
assert "ghcr.io/dragonk/kurrier-baikal:${KURRIER_IMAGE_TAG:-pr-616}" in COMPOSE
assert "HOSTNAME: 0.0.0.0" in COMPOSE
assert "DAV_CONFIG_ENCRYPTION_KEY" in COMPOSE
assert "DAV_ADMIN_PASSWORD_HASH" in COMPOSE
assert "- ${KURRIER_DATA_DIR:-/mnt/Dane/kurrier}/dav/config:/var/www/baikal/config" in COMPOSE
assert "- ${KURRIER_DATA_DIR:-/mnt/Dane/kurrier}/dav/data:/var/www/baikal/Specific" in COMPOSE
assert "- service: baikal" in WORKFLOW
assert "deploy/images/kurrier-baikal.Dockerfile" in WORKFLOW
for service, dockerfile in {
    "web": "apps/web/Dockerfile",
    "worker": "apps/worker/Dockerfile",
    "bootstrap": "deploy/images/kurrier-bootstrap.Dockerfile",
    "baikal-postgres": "deploy/images/kurrier-baikal-postgres.Dockerfile",
    "baikal": "deploy/images/kurrier-baikal.Dockerfile",
    "garage": "deploy/images/kurrier-garage.Dockerfile",
}.items():
    assert f"- service: {service}\n            dockerfile: {dockerfile}" in WORKFLOW
assert "COPY db/init/migrations /scripts/migrations" in BOOTSTRAP
assert "COPY db/init/init.sql" not in BOOTSTRAP
assert "COPY deploy/images/baikal/entrypoint.sh /usr/local/bin/kurrier-baikal-entrypoint.sh" in BAIKAL
assert "exec /docker-entrypoint.sh \"$@\"" in ENTRYPOINT
assert "DAV_CONFIG_ENCRYPTION_KEY" in GENERATOR
assert "DAV_ADMIN_PASSWORD_HASH" in GENERATOR
assert "GARAGE_RPC_SECRET={secrets.token_hex(32)}" in GENERATOR
assert "os.open(temporary_path" in GENERATOR
assert "os.replace(temporary_path, output_path)" in GENERATOR
assert "await connection();" in GENERIC_OIDC_CALLBACK

print("Repository-free Arcane deployment contract passed.")

# Kurrier PR #616 — test deployment on Arcane

This Compose project runs the images published from `fix/i18n-locale-validation` by
`.github/workflows/pr-test-images.yml`. It is **testing-only**: it creates a
separate state directory at `/mnt/Dane/kurrier-test` and must never reuse a
production Kurrier database, Redis data, Garage data, or Baikal data.

No host ports are published. The `web` container is attached to the existing
Arcane reverse-proxy Docker network; configure the proxy separately to route the
test hostname to `web:3000` on that network. Do not add a direct host-port
mapping.

## Prerequisites

1. The GitHub Actions job **pr-test-images** must have completed successfully.
   The default testing tag is `pr-616`:
   - `ghcr.io/dragonk/kurrier-web:pr-616`
   - `ghcr.io/dragonk/kurrier-worker:pr-616`
2. The host must be able to pull those images. If GHCR packages are private,
   authenticate Docker using a token with `read:packages`; do not place the token
   in this repository or `.env`.
3. Clone this branch on the deployment host. `migrate` and Garage use the
   repository's `db/init` files as read-only bootstrap sources.
4. Create a dedicated Canaille OIDC client for the testing hostname, with this
   callback URL:
   `https://<test-host>/api/auth/oidc/generic/callback`

## Configure

```bash
cd deploy/arcane
cp .env.example .env
chmod 600 .env
```

Set all `REPLACE_...` values to generated secrets. Connection strings must use
the exact passwords configured for the corresponding services. Set:

- `WEB_URL` to the real HTTPS test hostname;
- `ARCANE_PROXY_NETWORK` to the existing reverse-proxy Docker network;
- `KURRIER_REPO_DIR` to the absolute path of the checked-out repository;
- `OIDC_ISSUER_URL`, `OIDC_CLIENT_ID`, and `OIDC_CLIENT_SECRET` for the dedicated
  Canaille client.

Validate without starting containers:

```bash
docker compose --env-file .env -f compose.test.yml config -q
```

## Start and bootstrap

```bash
docker compose --env-file .env -f compose.test.yml pull
docker compose --env-file .env -f compose.test.yml up -d
docker compose --env-file .env -f compose.test.yml --profile bootstrap run --rm migrate
```

Inspect health and errors without exposing secrets:

```bash
docker compose --env-file .env -f compose.test.yml ps
docker compose --env-file .env -f compose.test.yml logs --tail=100 web worker
```

Then add the test-host route in the existing Arcane reverse proxy and verify:

1. HTTPS and a normal OIDC sign-in;
2. login callback and logout;
3. PL and EN calendar day/week/month views;
4. timed and all-day events, create/edit, guests, RSVP and recurrence;
5. calendar timezone `Europe/Warsaw` while the browser is in a different zone,
   e.g. `America/New_York`.

## Upgrade and rollback

Use the immutable SHA tag printed by the GitHub Actions run for a reproducible
upgrade. Change `KURRIER_IMAGE_TAG`, pull, then recreate only web and worker:

```bash
docker compose --env-file .env -f compose.test.yml pull web worker
docker compose --env-file .env -f compose.test.yml up -d --no-deps web worker
```

To roll back, set `KURRIER_IMAGE_TAG` to the previous verified `sha-<commit>`
tag and run the same two commands. Do not delete `/mnt/Dane/kurrier-test` until
the test data is no longer needed.

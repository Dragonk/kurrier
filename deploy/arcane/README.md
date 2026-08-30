# Kurrier PR #616 — test deployment on Arcane

This Compose project runs the images published from `fix/i18n-locale-validation` by
`.github/workflows/pr-test-images.yml`. It is **testing-only**: it creates a
separate state directory at `/mnt/Dane/kurrier` and must never reuse a
production Kurrier database, Redis data, Garage data, or Baikal data.

No host ports are published. The `kurrier-web` container is attached to Zoraxy's
existing Docker network. Configure a Zoraxy proxy route for the test hostname to
the Docker upstream `kurrier-web:3000` on that network; do not use a server IP or add a
direct host-port mapping.

## Prerequisites

1. The GitHub Actions job **pr-test-images** must have completed successfully.
   The default testing tag is `pr-616`:
   - `ghcr.io/dragonk/kurrier-web:pr-616`
   - `ghcr.io/dragonk/kurrier-worker:pr-616`
2. The host must be able to pull those images. If GHCR packages are private,
   authenticate Docker using a token with `read:packages`; do not place the token
   in this repository or `.env`.
3. The GitHub Actions workflow publishes the bootstrap, Baikal Postgres, and
   Garage images. No repository checkout is required on the deployment host.
4. Create a dedicated Canaille OIDC client for the testing hostname, with this
   callback URL:
   `https://kurrier.kmms.ovh/api/auth/oidc/generic/callback`

## Configure

Use `generate-env.py` in Arcane's file/terminal action to generate `.env`
locally. It writes a mode-`0600` file and creates every secret without printing
it to output. Then set only the Canaille client credentials. Connection strings
are generated from their matching service passwords.

- `WEB_URL` to `https://kurrier.kmms.ovh`;
- `ZORAXY_PROXY_NETWORK` to `zoraxy`;
- `OIDC_CLIENT_ID` and `OIDC_CLIENT_SECRET` for the dedicated Canaille client.

Validate without starting containers:

```bash
docker compose --env-file .env -f compose.yml config -q
```

## Start and bootstrap

```bash
docker compose --env-file .env -f compose.yml pull
docker compose --env-file .env -f compose.yml up -d
docker compose --env-file .env -f compose.yml --profile bootstrap run --rm migrate
```

Inspect health and errors without exposing secrets:

```bash
docker compose --env-file .env -f compose.yml ps
docker compose --env-file .env -f compose.yml logs --tail=100 kurrier-web worker
```

Then add the test-host route in Zoraxy and verify:

1. HTTPS and a normal OIDC sign-in;
2. login callback and logout;
3. PL and EN calendar day/week/month views;
4. timed and all-day events, create/edit, guests, RSVP and recurrence;
5. calendar timezone `Europe/Warsaw` while the browser is in a different zone,
   e.g. `America/New_York`.

## Upgrade and rollback

Use the immutable SHA tag printed by the GitHub Actions run for a reproducible
upgrade. Change `KURRIER_IMAGE_TAG`, pull, then recreate only kurrier-web and worker:

```bash
docker compose --env-file .env -f compose.yml pull kurrier-web worker
docker compose --env-file .env -f compose.yml up -d --no-deps kurrier-web worker
```

To roll back, set `KURRIER_IMAGE_TAG` to the previous verified `sha-<commit>`
tag and run the same two commands. Do not delete `/mnt/Dane/kurrier` until
the test data is no longer needed.

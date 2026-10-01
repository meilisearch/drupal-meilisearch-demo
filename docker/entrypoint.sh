#!/usr/bin/env bash
# Installs the demo on first start, then hands over to Apache.
set -euo pipefail
cd /opt/drupal
drush=vendor/bin/drush
site=web/sites/default
marker="$site/files/.demo-installed"

# Settings come from the image on every start; the database and the hash salt
# are in the files volume.
mkdir -p "$site/files" config/sync
[ -s "$site/files/.hash_salt" ] || head -c 48 /dev/urandom | base64 | tr -d '\n/+=' > "$site/files/.hash_salt"
cp docker/settings.php "$site/settings.php"
chown -R www-data:www-data "$site/files" config

if [ ! -f "$marker" ]; then
  echo "[demo] Waiting for Meilisearch at ${MEILISEARCH_URL}..."
  for _ in $(seq 1 60); do
    curl -sf "${MEILISEARCH_URL}/health" >/dev/null && break
    sleep 1
  done

  echo "[demo] Installing Drupal..."
  $drush site:install standard -y \
    --site-name="Meili Kitchen" \
    --account-name=admin --account-pass=admin

  echo "[demo] Setting up recipes, search and facets..."
  $drush pm:install meilisearch_demo -y
  $drush cache:rebuild

  touch "$marker"
  chown -R www-data:www-data "$site/files" config
  echo "[demo] Ready: search at http://localhost:${DEMO_PORT:-8080}/recipes (admin / admin)"
fi

# Warm Drupal's caches in the background once Apache is up, so the first
# searches of a demo are as quick as the next ones.
(
  for _ in $(seq 1 30); do
    curl -sf -o /dev/null http://localhost/ && break
    sleep 1
  done
  for keys in "" chiken tirami "%22coconut+milk%22" "curry+-chicken" "vegan+dessert"; do
    curl -s -o /dev/null "http://localhost/recipes?search=${keys}"
  done
) &

exec "$@"

#!/usr/bin/env bash
# Installs the demo on first start, then hands over to Apache.
set -euo pipefail
cd /opt/drupal
drush=vendor/bin/drush
site=web/sites/default
marker="$site/files/.demo-installed"

if [ ! -f "$marker" ]; then
  echo "[demo] Waiting for Meilisearch at ${MEILISEARCH_URL}..."
  for _ in $(seq 1 60); do
    curl -sf "${MEILISEARCH_URL}/health" >/dev/null && break
    sleep 1
  done

  echo "[demo] Installing Drupal..."
  mkdir -p "$site/files" config/sync
  $drush site:install standard -y \
    --db-url="sqlite://localhost//opt/drupal/web/sites/default/files/.ht.sqlite" \
    --site-name="Meili Kitchen" \
    --account-name=admin --account-pass=admin
  chmod u+w "$site" "$site/settings.php"
  echo "include '/opt/drupal/docker/settings.demo.php';" >> "$site/settings.php"

  echo "[demo] Setting up recipes, search and facets..."
  $drush pm:install meilisearch_demo -y
  $drush cache:rebuild

  touch "$marker"
  chown -R www-data:www-data "$site/files" config
  echo "[demo] Ready: search at http://localhost:${DEMO_PORT:-8080}/recipes (admin / admin)"
fi

exec "$@"

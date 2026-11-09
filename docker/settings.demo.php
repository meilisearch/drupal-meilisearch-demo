<?php

/**
 * @file
 * Demo settings, included from settings.php.
 *
 * The Meilisearch URL and key come from the environment, as the module
 * recommends: they never end up in exported configuration.
 */

$config['search_api.server.meilisearch']['backend_config']['url'] = getenv('MEILISEARCH_URL') ?: 'http://meilisearch:7700';
$config['search_api.server.meilisearch']['backend_config']['api_key'] = getenv('MEILISEARCH_API_KEY') ?: '';
if (getenv('MEILISEARCH_INDEX_PREFIX') !== FALSE) {
  $config['search_api.server.meilisearch']['backend_config']['index_prefix'] = getenv('MEILISEARCH_INDEX_PREFIX');
}

// Locally any host name works (localhost, OrbStack domains...). A deployed
// demo lists its own, for example "^meili-kitchen\.fly\.dev$".
$settings['trusted_host_patterns'] = getenv('TRUSTED_HOST_PATTERNS')
  ? explode(',', getenv('TRUSTED_HOST_PATTERNS'))
  : ['.*'];
$settings['config_sync_directory'] = '../config/sync';

// The login form is off unless DRUPAL_LOGIN_FORM is set, so a deployed demo
// shows no login panel (see LoginFormSubscriber). compose.yaml turns it on.
$settings['meilisearch_demo_login_form'] = filter_var(getenv('DRUPAL_LOGIN_FORM') ?: FALSE, FILTER_VALIDATE_BOOL);

// No mail server in the demo: keep outgoing mail in the state store.
$config['system.mail']['interface']['default'] = 'test_mail_collector';

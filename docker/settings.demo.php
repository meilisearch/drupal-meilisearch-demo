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

// A local demo: accept any host name (localhost, OrbStack domains...).
$settings['trusted_host_patterns'] = ['.*'];
$settings['config_sync_directory'] = '../config/sync';

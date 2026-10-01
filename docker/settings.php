<?php

/**
 * @file
 * Drupal settings of the demo, copied into the site on every start.
 *
 * The database and the hash salt live in the files volume, so rebuilding the
 * image keeps the installed site.
 */

$databases['default']['default'] = [
  'driver' => 'sqlite',
  'database' => '/opt/drupal/web/sites/default/files/.ht.sqlite',
  'namespace' => 'Drupal\\sqlite\\Driver\\Database\\sqlite',
  'autoload' => 'core/modules/sqlite/src/Driver/Database/sqlite/',
];
$settings['hash_salt'] = trim((string) @file_get_contents('/opt/drupal/web/sites/default/files/.hash_salt'));
$settings['file_scan_ignore_directories'] = ['node_modules', 'bower_components'];
$settings['entity_update_batch_size'] = 50;

include '/opt/drupal/docker/settings.demo.php';

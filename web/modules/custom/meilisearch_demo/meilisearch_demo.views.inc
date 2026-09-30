<?php

/**
 * @file
 * Views integration of the Meilisearch demo.
 */

declare(strict_types=1);

/**
 * Implements hook_views_data().
 */
function meilisearch_demo_views_data(): array {
  $data['views']['meilisearch_demo_stats'] = [
    'title' => t('Meilisearch result count and time'),
    'help' => t('Shows how many results Meilisearch found and how long it took.'),
    'area' => ['id' => 'meilisearch_demo_stats'],
  ];
  return $data;
}

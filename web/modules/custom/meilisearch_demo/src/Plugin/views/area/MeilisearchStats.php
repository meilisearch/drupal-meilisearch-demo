<?php

declare(strict_types=1);

namespace Drupal\meilisearch_demo\Plugin\views\area;

use Drupal\search_api\Plugin\views\query\SearchApiQuery;
use Drupal\views\Attribute\ViewsArea;
use Drupal\views\Plugin\views\area\AreaPluginBase;

/**
 * Shows the result count and Meilisearch's processing time.
 */
#[ViewsArea('meilisearch_demo_stats')]
class MeilisearchStats extends AreaPluginBase {

  /**
   * {@inheritdoc}
   */
  public function render($empty = FALSE): array {
    $query = $this->view->query;
    $results = $query instanceof SearchApiQuery ? $query->getSearchApiResults() : NULL;
    if (!$results) {
      return [];
    }
    $count = $this->formatPlural($results->getResultCount(), '1 recipe', '@count recipes');
    $time = $results->getExtraData('meilisearch_processing_time_ms');
    return [
      '#type' => 'html_tag',
      '#tag' => 'p',
      '#attributes' => ['class' => ['meili-stats']],
      '#value' => $time === NULL
        ? '<strong>' . $count . '</strong>'
        : $this->t('<strong>@count</strong>, found by Meilisearch in @time ms', ['@count' => $count, '@time' => $time]),
    ];
  }

}

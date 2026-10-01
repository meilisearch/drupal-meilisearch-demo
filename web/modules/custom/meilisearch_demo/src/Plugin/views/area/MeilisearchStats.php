<?php

declare(strict_types=1);

namespace Drupal\meilisearch_demo\Plugin\views\area;

use Drupal\Component\Utility\Html;
use Drupal\Core\Render\Markup;
use Drupal\search_api\Plugin\views\query\SearchApiQuery;
use Drupal\views\Attribute\ViewsArea;
use Drupal\views\Plugin\views\area\AreaPluginBase;

/**
 * Shows the result count, Meilisearch's processing time and the request.
 *
 * The request is recorded by meilisearch_demo_meilisearch_search_params_alter()
 * and shown in the "Under the hood" panel.
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
    $time = $results->getExtraData('meilisearch_processing_time_ms');
    $requests = $results->getExtraData('meilisearch_demo_requests', []);
    $main = $requests[0]['params'] ?? NULL;

    return [
      '#type' => 'inline_template',
      '#template' => '<div class="meili-stats">
          <p class="meili-stats__count"><strong>{{ count }}</strong>{% if time is not null %} <span class="speed" title="{{ \'Processing time reported by Meilisearch\'|t }}">{{ time }}</span> <span class="meili-stats__by">{{ \'in Meilisearch\'|t }}</span>{% endif %}</p>
          {% if main %}<button type="button" class="hood-toggle" aria-controls="kitchen-hood" aria-expanded="false"><span aria-hidden="true">{&nbsp;}</span> {{ \'Under the hood\'|t }}</button>{% endif %}
        </div>
        {% if main %}
        <section class="hood" id="kitchen-hood" aria-label="{{ \'Request sent to Meilisearch\'|t }}">
          <p class="hood__lead">{{ \'Views and Search API built this search; drupal/meilisearch sent it as:\'|t }}</p>
          <p class="hood__route"><span class="hood__verb">POST</span> {{ route }}</p>
          <pre class="hood__json"><code>{{ main }}</code></pre>
          {% if notes %}<ul class="hood__notes">{% for note in notes %}<li>{{ note }}</li>{% endfor %}</ul>{% endif %}
        </section>
        {% endif %}',
      '#context' => [
        'count' => $this->formatPlural($results->getResultCount(), '1 recipe', '@count recipes'),
        'time' => $time === NULL ? NULL : ($time < 1 ? '<1 ms' : $time . ' ms'),
        'main' => $main === NULL ? NULL : Markup::create($this->highlightJson($main)),
        'route' => count($requests) > 1
          ? $this->t('/multi-search · @count queries', ['@count' => count($requests)])
          : '/indexes/' . $results->getExtraData('meilisearch_index_uid', '…') . '/search',
        'notes' => array_map([$this, 'describe'], array_slice($requests, 1)),
      ],
    ];
  }

  /**
   * Describes one of the extra facet queries.
   */
  protected function describe(array $request): string {
    $facet = str_replace('_', ' ', (string) ($request['context']['facet'] ?? ''));
    $filter = $request['params']['filter'] ?? '';
    $args = [
      '@Facet' => ucfirst($facet),
      '@facet' => $facet,
      '@filter' => is_string($filter) ? $filter : '',
    ];
    $note = match ($request['context']['query'] ?? '') {
      'facet_values' => $this->t('+ @Facet counts for the OR facet: the same search without the @facet filter, so the other values keep their counts.', $args),
      'facet_all_values' => $this->t('+ Every @facet value, for zero counts.', $args),
      'facet_missing' => $this->t('+ How many results have no @facet.', $args),
      default => $this->t('+ One more query.'),
    };
    return (string) $note . ($args['@filter'] !== '' ? ' ' . $this->t('Filter: @filter', $args) : '');
  }

  /**
   * Pretty-prints parameters as escaped, colored JSON.
   */
  protected function highlightJson(array $params): string {
    // What the search does first, then how results come back.
    $first = array_flip(['q', 'filter', 'sort', 'facets', 'page', 'hitsPerPage']);
    $params = array_intersect_key(array_replace($first, $params), $params);
    $json = json_encode($params, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    // Lists of values on one line.
    $json = preg_replace_callback('/\[\s+([^\[\]{}]*?)\s+\]/', static fn(array $m): string => '[' . preg_replace('/,\s+/', ', ', $m[1]) . ']', $json);
    // The highlighting processor marks matches with private-use characters;
    // show them as JSON escapes.
    $json = str_replace(["\u{E000}", "\u{E001}"], ['\\ue000', '\\ue001'], $json);
    return preg_replace_callback(
      '/("(?:[^"\\\\]|\\\\.)*")(\s*:)?|\b(?:true|false|null)\b|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/',
      static function (array $m): string {
        if (($m[1] ?? '') !== '') {
          $class = empty($m[2]) ? 'j-string' : 'j-key';
          return '<span class="' . $class . '">' . Html::escape($m[1]) . '</span>' . ($m[2] ?? '');
        }
        return '<span class="j-literal">' . Html::escape($m[0]) . '</span>';
      },
      // Outside the tokens, JSON only has brackets, commas and whitespace.
      $json,
    );
  }

}

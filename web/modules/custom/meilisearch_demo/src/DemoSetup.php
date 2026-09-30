<?php

declare(strict_types=1);

namespace Drupal\meilisearch_demo;

use Drupal\block\Entity\Block;
use Drupal\Component\Serialization\Yaml;
use Drupal\Core\Extension\ThemeInstallerInterface;
use Drupal\facets\Entity\Facet;
use Drupal\field\Entity\FieldConfig;
use Drupal\field\Entity\FieldStorageConfig;
use Drupal\node\Entity\Node;
use Drupal\node\Entity\NodeType;
use Drupal\search_api\Entity\Index;
use Drupal\search_api\Entity\Server;
use Drupal\search_api\Item\Field;
use Drupal\taxonomy\Entity\Term;
use Drupal\taxonomy\Entity\Vocabulary;
use Drupal\views\Entity\View;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\DependencyInjection\ContainerInjectionInterface;

/**
 * Builds the demo: content model, search configuration, blocks and recipes.
 */
class DemoSetup implements ContainerInjectionInterface {

  /**
   * The demo theme.
   */
  protected const THEME = 'meili_kitchen';

  /**
   * Term IDs, keyed by vocabulary and name.
   */
  protected array $terms = [];

  /**
   * Constructs a DemoSetup.
   */
  public function __construct(protected ThemeInstallerInterface $themeInstaller) {}

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container): static {
    return new static($container->get('theme_installer'));
  }

  /**
   * Runs the whole setup.
   */
  public function run(): void {
    $this->createContentModel();
    $this->createSearch();
    $this->createView();
    $this->createFacets();
    $this->installTheme();
    $this->createContent();
  }

  /**
   * Creates the vocabularies, the recipe type and its fields.
   */
  protected function createContentModel(): void {
    foreach (['cuisine' => 'Cuisine', 'meal_type' => 'Meal type', 'diet' => 'Diet'] as $vid => $name) {
      Vocabulary::create(['vid' => $vid, 'name' => $name])->save();
    }
    NodeType::create(['type' => 'recipe', 'name' => 'Recipe'])->save();

    FieldConfig::create([
      'field_name' => 'body',
      'entity_type' => 'node',
      'bundle' => 'recipe',
      'label' => 'Description',
    ])->save();

    $fields = [
      'field_ingredients' => ['string', 'Ingredients', -1, []],
      'field_cuisine' => ['entity_reference', 'Cuisine', 1, ['target_type' => 'taxonomy_term']],
      'field_meal_type' => ['entity_reference', 'Meal type', -1, ['target_type' => 'taxonomy_term']],
      'field_diet' => ['entity_reference', 'Diet', -1, ['target_type' => 'taxonomy_term']],
      'field_total_time' => ['integer', 'Total time (minutes)', 1, []],
      'field_rating' => ['decimal', 'Rating', 1, ['precision' => 3, 'scale' => 1]],
      'field_emoji' => ['string', 'Emoji', 1, []],
    ];
    $vocabularies = ['field_cuisine' => 'cuisine', 'field_meal_type' => 'meal_type', 'field_diet' => 'diet'];
    foreach ($fields as $name => [$type, $label, $cardinality, $settings]) {
      FieldStorageConfig::create([
        'field_name' => $name,
        'entity_type' => 'node',
        'type' => $type,
        'cardinality' => $cardinality,
        'settings' => $settings,
      ])->save();
      $field = [
        'field_name' => $name,
        'entity_type' => 'node',
        'bundle' => 'recipe',
        'label' => $label,
      ];
      if (isset($vocabularies[$name])) {
        $field['settings'] = [
          'handler' => 'default:taxonomy_term',
          'handler_settings' => ['target_bundles' => [$vocabularies[$name] => $vocabularies[$name]], 'auto_create' => TRUE],
        ];
      }
      FieldConfig::create($field)->save();
    }
  }

  /**
   * Creates the Meilisearch server and the recipes index.
   *
   * The server URL and API key are overridden from the environment in
   * settings.php, the way the module recommends.
   */
  protected function createSearch(): void {
    Server::create([
      'id' => 'meilisearch',
      'name' => 'Meilisearch',
      'backend' => 'meilisearch',
      'backend_config' => [
        'url' => 'http://meilisearch:7700',
        'api_key' => '',
        'index_prefix' => 'demo_',
        'search_mode' => 'keyword',
        'semantic_ratio' => 0.5,
        'embedder' => '',
        'matching_strategy' => 'last',
        'max_total_hits' => 10000,
      ],
    ])->save();

    $index = Index::create([
      'id' => 'recipes',
      'name' => 'Recipes',
      'server' => 'meilisearch',
      'datasource_settings' => [
        'entity:node' => [
          'bundles' => ['default' => FALSE, 'selected' => ['recipe']],
          'languages' => ['default' => TRUE, 'selected' => []],
        ],
      ],
      'tracker_settings' => ['default' => ['indexing_order' => 'fifo']],
      'options' => ['index_directly' => FALSE, 'cron_limit' => 50],
    ]);
    $fields = [
      'title' => ['Title', 'title', 'text', 8.0],
      'body' => ['Description', 'body', 'text', 2.0],
      'ingredients' => ['Ingredients', 'field_ingredients', 'text', 1.0],
      'cuisine' => ['Cuisine', 'field_cuisine:entity:name', 'string', NULL],
      'meal_type' => ['Meal type', 'field_meal_type:entity:name', 'string', NULL],
      'diet' => ['Diet', 'field_diet:entity:name', 'string', NULL],
      'total_time' => ['Total time', 'field_total_time', 'integer', NULL],
      'rating' => ['Rating', 'field_rating', 'decimal', NULL],
      'emoji' => ['Emoji', 'field_emoji', 'string', NULL],
      'created' => ['Created', 'created', 'date', NULL],
    ];
    foreach ($fields as $id => [$label, $path, $type, $boost]) {
      $field = (new Field($index, $id))
        ->setLabel($label)
        ->setDatasourceId('entity:node')
        ->setPropertyPath($path)
        ->setType($type);
      if ($boost !== NULL) {
        $field->setBoost($boost);
      }
      $index->addField($field);
    }
    // Lets people search "vegan dessert" or "thai": the facet values are
    // searchable too.
    $index->addField((new Field($index, 'tags'))
      ->setLabel('Cuisine, meal and diet')
      ->setPropertyPath('aggregated_field')
      ->setType('text')
      ->setBoost(3.0)
      ->setConfiguration([
        'type' => 'union',
        'fields' => [
          'entity:node/field_cuisine:entity:name',
          'entity:node/field_meal_type:entity:name',
          'entity:node/field_diet:entity:name',
        ],
      ]));
    $plugins = \Drupal::service('search_api.plugin_helper');
    $index->addProcessor($plugins->createProcessorPlugin($index, 'entity_status'));
    $index->addProcessor($plugins->createProcessorPlugin($index, 'meilisearch_highlighting', [
      'fields' => ['body', 'ingredients'],
      'pre_tag' => '<strong>',
      'post_tag' => '</strong>',
      'crop_length' => 18,
      'crop_marker' => '…',
    ]));
    $index->save();
  }

  /**
   * Imports the search view.
   */
  protected function createView(): void {
    $path = \Drupal::service('extension.list.module')->getPath('meilisearch_demo') . '/config/demo/views.view.recipes.yml';
    View::create(Yaml::decode(file_get_contents($path)))->save();
  }

  /**
   * Creates the facets of the search page.
   */
  protected function createFacets(): void {
    $facets = [
      'cuisine' => ['Cuisine', 'or'],
      'meal_type' => ['Meal', 'and'],
      'diet' => ['Diet', 'and'],
    ];
    $weight = 0;
    foreach ($facets as $id => [$name, $operator]) {
      $facet = Facet::create([
        'id' => $id,
        'name' => $name,
        'weight' => $weight++,
        'use_hierarchy' => FALSE,
        'hierarchy' => ['type' => 'taxonomy', 'config' => []],
        'min_count' => 1,
        'query_operator' => $operator,
        'show_only_one_result' => FALSE,
        'show_title' => FALSE,
      ]);
      $facet->setFacetSourceId('search_api:views_page__recipes__page_1');
      $facet->setFieldIdentifier($id);
      $facet->setUrlAlias(str_replace('_type', '', $id));
      $facet->setWidget('links', ['show_numbers' => TRUE, 'soft_limit' => 0, 'show_reset_link' => FALSE]);
      $facet->addProcessor([
        'processor_id' => 'url_processor_handler',
        'weights' => ['pre_query' => -10, 'build' => -10],
        'settings' => [],
      ]);
      $facet->addProcessor([
        'processor_id' => 'count_widget_order',
        'weights' => ['sort' => 30],
        'settings' => ['sort' => 'DESC'],
      ]);
      $facet->addProcessor([
        'processor_id' => 'display_value_widget_order',
        'weights' => ['sort' => 40],
        'settings' => ['sort' => 'ASC'],
      ]);
      $facet->setEmptyBehavior(['behavior' => 'none']);
      $facet->setOnlyVisibleWhenFacetSourceIsVisible(TRUE);
      $facet->save();
    }
  }

  /**
   * Installs the demo theme and places its blocks.
   */
  protected function installTheme(): void {
    $this->themeInstaller->install([self::THEME]);
    \Drupal::configFactory()->getEditable('system.theme')->set('default', self::THEME)->save();
    \Drupal::configFactory()->getEditable('system.site')->set('page.front', '/recipes')->save();

    // Blocks copied from the previous default theme do not fit this layout.
    foreach (\Drupal::entityTypeManager()->getStorage('block')->loadByProperties(['theme' => self::THEME]) as $block) {
      $block->delete();
    }
    $blocks = [
      'search' => ['hero', 'views_exposed_filter_block:recipes-page_1', '', 0],
      'messages' => ['content', 'system_messages_block', '', -10],
      'tabs' => ['content', 'local_tasks_block', '', -5],
      'main' => ['content', 'system_main_block', '', 0],
      'facet_cuisine' => ['sidebar', 'facet_block:cuisine', 'Cuisine', 0],
      'facet_meal_type' => ['sidebar', 'facet_block:meal_type', 'Meal', 1],
      'facet_diet' => ['sidebar', 'facet_block:diet', 'Diet', 2],
    ];
    foreach ($blocks as $id => [$region, $plugin, $label, $weight]) {
      Block::create([
        'id' => self::THEME . '_' . $id,
        'theme' => self::THEME,
        'region' => $region,
        'plugin' => $plugin,
        'weight' => $weight,
        'settings' => [
          'id' => $plugin,
          'label' => $label,
          'label_display' => $label !== '' ? 'visible' : '0',
        ],
      ])->save();
    }
  }

  /**
   * Creates the recipes and indexes them.
   */
  protected function createContent(): void {
    $path = \Drupal::service('extension.list.module')->getPath('meilisearch_demo') . '/data/recipes.json';
    $recipes = json_decode(file_get_contents($path), TRUE);
    foreach ($recipes as $i => $recipe) {
      Node::create([
        'type' => 'recipe',
        'title' => $recipe['title'],
        'uid' => 1,
        'status' => 1,
        // Spread creation dates so "newest" sorts are meaningful.
        'created' => \Drupal::time()->getRequestTime() - $i * 86400,
        'body' => ['value' => $recipe['description'], 'format' => 'plain_text'],
        'field_ingredients' => $recipe['ingredients'],
        'field_cuisine' => [$this->term('cuisine', $recipe['cuisine'])],
        'field_meal_type' => array_map(fn($m) => $this->term('meal_type', $m), $recipe['meal_types']),
        'field_diet' => array_map(fn($d) => $this->term('diet', $d), $recipe['diets']),
        'field_total_time' => $recipe['total_time'],
        'field_rating' => $recipe['rating'],
        'field_emoji' => $recipe['emoji'],
      ])->save();
    }

    $index = Index::load('recipes');
    $index->indexItems();
    // From now on, edits reach Meilisearch right away.
    $index->setOption('index_directly', TRUE)->save();
  }

  /**
   * Returns the ID of a term, creating it on first use.
   */
  protected function term(string $vid, string $name): int {
    if (!isset($this->terms[$vid][$name])) {
      $term = Term::create(['vid' => $vid, 'name' => $name]);
      $term->save();
      $this->terms[$vid][$name] = (int) $term->id();
    }
    return $this->terms[$vid][$name];
  }

}

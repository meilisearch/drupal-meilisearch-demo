# Meili Kitchen

A recipe search site built with Drupal 11 and [`drupal/meilisearch`](https://www.drupal.org/project/meilisearch), the Meilisearch backend for Search API. One command gives you 116 recipes, typo-tolerant search that updates as you type, facets and highlighted excerpts.

## Quick start

```bash
cp .env.example .env    # set MEILISEARCH_MODULE_PATH if the module is elsewhere
docker compose up --build
```

The first start installs Drupal, creates the recipes and indexes them, which takes a minute or two. Then open <http://localhost:8080>. On OrbStack, <http://drupal.drupal-meilisearch-demo.orb.local> works too.

To log in, use `admin` / `admin`.

## What to try

| Try | What it shows |
|---|---|
| Type `chiken` | Typo tolerance: chicken recipes, while you type |
| `"coconut milk"` | Phrase search |
| `curry -chicken` | Leaving words out |
| `vegan dessert` | Facet values are searchable too |
| Pick two cuisines | An OR facet: the other cuisines keep their counts |
| *Under 30 min*, *Top rated* | Filters and strict sorts |
| Edit a recipe title | The change is searchable right away |

The line above the results shows how long Meilisearch took.

In the admin, **Configuration → Search and metadata → Search API** has the server and the *Recipes* index. The index's **Processors** tab has the *Meilisearch highlighting* settings.

## How it is built

| Part | Where |
|---|---|
| Stack: Meilisearch, and Drupal on SQLite | `compose.yaml`, `Dockerfile` |
| First-start install | `docker/entrypoint.sh` |
| Meilisearch URL and key from the environment (the recommended setup) | `docker/settings.demo.php` |
| Content model, server, index, facets, blocks and recipes | `web/modules/custom/meilisearch_demo/src/DemoSetup.php` |
| The search view | `web/modules/custom/meilisearch_demo/config/demo/views.view.recipes.yml` |
| Theme and live search | `web/themes/custom/meili_kitchen` |
| Recipe data (written for this demo) | `scripts/recipes.py` builds `data/recipes.json` |

Live search is a small script: it fetches the next results page from Drupal and swaps the results and the facets. Every search still goes through Views, Search API and the module.

## Working on the module

`MEILISEARCH_MODULE_PATH` points at a checkout of `drupal/meilisearch`, installed as a Composer path repository. Keep it in sync while you edit:

```bash
docker compose watch
```

This syncs the theme, the demo module and the module's `src/`. Clear caches after changes to services or plugins:

```bash
docker compose exec drupal vendor/bin/drush cr
```

## Reset

```bash
docker compose down -v
```

The next `up` installs everything again.

## Troubleshooting

- **Port already in use:** set `DEMO_PORT` or `MEILISEARCH_PORT` in `.env`.
- **The install fails at the Meilisearch step:** check `docker compose logs meilisearch`, then `docker compose down -v && docker compose up`.
- **The build fails on `drupal/meilisearch`:** `MEILISEARCH_MODULE_PATH` must point at the module's root, the folder with its `composer.json`.

## Not covered here

Semantic and hybrid search (they need an embedder), Cloud click analytics, location search and multilingual content are described in the module's documentation.

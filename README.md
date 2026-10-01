# Meili Kitchen

A recipe search site built with Drupal 11 and [`drupal/meilisearch`](https://www.drupal.org/project/meilisearch), the Meilisearch backend for Search API. One command gives you 116 recipes, typo-tolerant search that updates as you type, facets and highlighted excerpts.

## Quick start

```bash
cp .env.example .env    # set MEILISEARCH_MODULE_PATH if the module is elsewhere
docker compose up --build
```

The first start installs Drupal, creates the recipes and indexes them, which takes a minute or two. Then open <http://localhost:8080>. On OrbStack, <http://drupal.drupal-meilisearch-demo.orb.local> works too.

To log in, use `admin` / `admin` (a deployed demo sets its own, see [Deploy](#deploy)).

## A two-minute demo

1. **Type.** Results, facet counts and highlights follow every keystroke. The green pill is Meilisearch's own processing time.
2. **Click the *Try* chips** under the search box:

   | Chip | What it shows |
   |---|---|
   | `chiken` | Typo tolerance: chicken recipes, with *Chicken* highlighted |
   | `tirami` | Prefix search: the last word matches as you type |
   | `"coconut milk"` | Phrase search |
   | `curry -chicken` | Leaving a word out |
   | `vegan dessert` | Cuisine, meal and diet are searchable too |

3. **Open *Under the hood*.** It shows the request drupal/meilisearch sent for this page: the query, the filter built from the facets, the sort, highlighting. Keep it open while you type and click.
4. **Pick two cuisines.** Cuisine is an OR facet: the filter becomes `(cuisine = "Indian" OR cuisine = "Thai")` and the other cuisines keep their counts, through a second query in the same multi-search.
5. **Filter and sort:** *Under 30 min*, *Top rated*, *Quickest*.
6. **Edit a recipe.** Log in (`admin` / `admin`), change a title, search for it: it is indexed on save.

Press <kbd>/</kbd> to jump to the search box and <kbd>Esc</kbd> to clear it.

In the admin, **Search settings** (top right) opens the *Recipes* index; its **Processors** tab has the *Meilisearch highlighting* settings.

## How it is built

| Part | Where |
|---|---|
| Stack: Meilisearch, and Drupal on SQLite | `compose.yaml`, `Dockerfile` |
| First-start install | `docker/entrypoint.sh` |
| Meilisearch URL and key from the environment (the recommended setup) | `docker/settings.demo.php` |
| Content model, server, index, facets, blocks and recipes | `web/modules/custom/meilisearch_demo/src/DemoSetup.php` |
| The search view | `web/modules/custom/meilisearch_demo/config/demo/views.view.recipes.yml` |
| Theme and live search | `web/themes/custom/meili_kitchen` |
| *Try* chips, and recording the request for *Under the hood* (`hook_meilisearch_search_params_alter()`) | `web/modules/custom/meilisearch_demo/meilisearch_demo.module` |
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

## Deploy

The image runs anywhere that runs a container with a persistent disk. It installs `drupal/meilisearch` from drupal.org; the site (SQLite database and uploads) lives in `/opt/drupal/web/sites/default/files`, which must be on that disk. Set:

| Variable | Value |
|---|---|
| `MEILISEARCH_URL`, `MEILISEARCH_API_KEY` | A Meilisearch Cloud project, or any reachable instance |
| `DRUPAL_ADMIN_PASSWORD` | The admin password, applied on every start |
| `TRUSTED_HOST_PATTERNS` | The site's host names as regular expressions, comma-separated, for example `^demo\.example\.com$` |
| `MEILISEARCH_INDEX_PREFIX` | Optional: an index prefix, so the demo never touches other indexes of the project |

The container listens on port 80. The first start installs Drupal and indexes the recipes, which takes a few minutes; the logs show `[demo] Ready` when it is done.

## Reset

```bash
docker compose down -v
```

The next `up` installs everything again.

## Troubleshooting

- **Port already in use:** set `DEMO_PORT` or `MEILISEARCH_PORT` in `.env`.
- **"400 Bad Request" in the browser:** fixed in the image (browsers send every `localhost` cookie to every port, which can exceed Apache's default header size). Rebuild with `docker compose up --build`, or use the OrbStack URL.
- **Search feels slow:** each search fetches the next page from Drupal in the background (about 50–250 ms here; Meilisearch's share is a few milliseconds, shown in the pill). A busy machine slows Drupal down first.
- **The install fails at the Meilisearch step:** check `docker compose logs meilisearch`, then `docker compose down -v && docker compose up`.
- **The build fails on `drupal/meilisearch`:** `MEILISEARCH_MODULE_PATH` must point at the module's root, the folder with its `composer.json`.

## Not covered here

Semantic and hybrid search (they need an embedder), Cloud click analytics, location search and multilingual content are described in the module's documentation.

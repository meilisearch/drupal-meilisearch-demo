/**
 * @file
 * Live search: re-renders results and facets while typing.
 *
 * The page is still rendered by Drupal and searched by Meilisearch; this only
 * fetches the next page in the background and swaps the two regions.
 */
((Drupal, once, debounce) => {
  const REGIONS = ['[data-kitchen-results]', '[data-kitchen-facets]'];
  const HOOD_KEY = 'meili-kitchen-hood';
  let controller = null;

  function storage(key, value) {
    try {
      if (value === undefined) {
        return window.localStorage.getItem(key);
      }
      window.localStorage.setItem(key, value);
    } catch (e) {
      // Storage can be unavailable; the panel then starts closed.
    }
    return null;
  }

  function syncHood() {
    const open = document.body.classList.contains('show-hood');
    document.querySelectorAll('.hood-toggle').forEach((button) => {
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  async function load(url, push) {
    if (controller) {
      controller.abort();
    }
    controller = new AbortController();
    const { signal } = controller;
    document.body.classList.add('is-searching');
    try {
      const response = await fetch(url, { headers: { Accept: 'text/html' }, signal });
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      // Before the swap: behaviors of the new regions read the URL.
      window.history[push ? 'pushState' : 'replaceState']({}, '', url);
      REGIONS.forEach((selector) => {
        const current = document.querySelector(selector);
        const next = doc.querySelector(selector);
        if (current && next) {
          current.replaceWith(next);
          Drupal.attachBehaviors(next);
        }
      });
      syncHood();
      document.body.classList.remove('is-searching');
    } catch (e) {
      if (e.name !== 'AbortError') {
        window.location.href = url;
      }
    }
  }

  /**
   * The form's values, plus the active facets from the current URL.
   */
  function urlFor(form) {
    const params = new URLSearchParams();
    new FormData(form).forEach((value, key) => {
      if (value !== '' && value !== 'All' && !(key === 'sort_by' && value === 'relevance')) {
        params.append(key, value);
      }
    });
    new URLSearchParams(window.location.search).forEach((value, key) => {
      if (key.startsWith('f[')) {
        params.append(key, value);
      }
    });
    const query = params.toString();
    return form.getAttribute('action').split('?')[0] + (query ? `?${query}` : '');
  }

  function markChips(form, input) {
    form.querySelectorAll('[data-try]').forEach((chip) => {
      chip.classList.toggle('is-current', chip.dataset.try === input.value.trim());
    });
  }

  Drupal.behaviors.kitchenLiveSearch = {
    attach(context) {
      // Only on the search page, where the facets rail is.
      if (!document.querySelector('[data-kitchen-facets]')) {
        return;
      }

      once('kitchen-live-search', 'form[id^="views-exposed-form-recipes-page-1"]', context).forEach((form) => {
        const input = form.querySelector('input[name="search"]');
        const typed = debounce(() => load(urlFor(form), false), 120);
        const search = (value) => {
          input.value = value;
          markChips(form, input);
          load(urlFor(form), true);
          input.focus();
        };

        form.addEventListener('input', (event) => {
          if (event.target === input) {
            markChips(form, input);
            typed();
          }
        });
        form.addEventListener('change', (event) => {
          if (event.target !== input) {
            load(urlFor(form), true);
          }
        });
        form.addEventListener('submit', (event) => {
          event.preventDefault();
          load(urlFor(form), true);
        });
        form.addEventListener('click', (event) => {
          const chip = event.target.closest('[data-try]');
          if (chip && !event.metaKey && !event.ctrlKey) {
            event.preventDefault();
            search(chip.dataset.try);
          }
          if (event.target.closest('.kitchen-search__clear')) {
            search('');
          }
        });
        input.addEventListener('keydown', (event) => {
          if (event.key === 'Escape' && input.value !== '') {
            event.preventDefault();
            search('');
          }
        });
        document.addEventListener('keydown', (event) => {
          const field = event.target.closest('input, textarea, select, [contenteditable]');
          if (event.key === '/' && !field) {
            event.preventDefault();
            input.focus();
            input.select();
          }
        });

        markChips(form, input);
        if (!input.value && window.matchMedia('(min-width: 900px)').matches) {
          input.focus({ preventScroll: true });
        }
      });

      once('kitchen-live-links', 'body', context).forEach(() => {
        if (storage(HOOD_KEY) === 'open') {
          document.body.classList.add('show-hood');
        }
        document.addEventListener('click', (event) => {
          if (event.target.closest('.hood-toggle')) {
            const open = document.body.classList.toggle('show-hood');
            storage(HOOD_KEY, open ? 'open' : 'closed');
            syncHood();
            return;
          }
          const link = event.target.closest('[data-kitchen-facets] a, [data-kitchen-results] .pager a');
          if (!link || event.metaKey || event.ctrlKey || event.shiftKey) {
            return;
          }
          event.preventDefault();
          load(link.href, true);
        });
        window.addEventListener('popstate', () => window.location.reload());
      });
      syncHood();

      // "Clear filters" once a facet is active.
      const rails = context.matches && context.matches('[data-kitchen-facets]')
        ? [context]
        : context.querySelectorAll('[data-kitchen-facets]');
      once('kitchen-clear-facets', rails).forEach((rail) => {
        if (!rail.querySelector('a.is-active')) {
          return;
        }
        const url = new URL(window.location.href);
        [...url.searchParams.keys()].filter((key) => key.startsWith('f[')).forEach((key) => url.searchParams.delete(key));
        const link = document.createElement('a');
        link.className = 'kitchen__clear';
        link.href = url.pathname + url.search;
        link.textContent = Drupal.t('Clear filters');
        rail.prepend(link);
      });
    },
  };
})(Drupal, once, Drupal.debounce);

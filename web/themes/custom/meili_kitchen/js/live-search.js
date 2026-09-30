/**
 * @file
 * Live search: re-renders results and facets while typing.
 *
 * The page is still rendered by Drupal and searched by Meilisearch; this only
 * fetches the next page in the background and swaps the two regions.
 */
((Drupal, once, debounce) => {
  const REGIONS = ['[data-kitchen-results]', '[data-kitchen-facets]'];
  let latest = 0;

  async function load(url, push) {
    const ticket = ++latest;
    document.body.classList.add('is-searching');
    try {
      const response = await fetch(url, { headers: { Accept: 'text/html' } });
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      if (ticket !== latest) {
        return;
      }
      REGIONS.forEach((selector) => {
        const current = document.querySelector(selector);
        const next = doc.querySelector(selector);
        if (current && next) {
          current.replaceWith(next);
          Drupal.attachBehaviors(next);
        }
      });
      window.history[push ? 'pushState' : 'replaceState']({}, '', url);
    } catch (e) {
      window.location.href = url;
    } finally {
      if (ticket === latest) {
        document.body.classList.remove('is-searching');
      }
    }
  }

  /**
   * The form's values, plus the active facets from the current URL.
   */
  function urlFor(form) {
    const params = new URLSearchParams();
    new FormData(form).forEach((value, key) => {
      if (value !== '' && value !== 'All') {
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

  Drupal.behaviors.kitchenLiveSearch = {
    attach(context) {
      once('kitchen-live-search', 'form[id^="views-exposed-form-recipes-page-1"]', context).forEach((form) => {
        if (window.location.pathname !== new URL(form.action, window.location.href).pathname) {
          return;
        }
        const typed = debounce(() => load(urlFor(form), false), 180);
        form.addEventListener('input', (event) => {
          if (event.target.name === 'search') {
            typed();
          }
        });
        form.addEventListener('change', (event) => {
          if (event.target.name !== 'search') {
            load(urlFor(form), true);
          }
        });
        form.addEventListener('submit', (event) => {
          event.preventDefault();
          load(urlFor(form), true);
        });
      });

      once('kitchen-live-links', 'body', context).forEach(() => {
        document.addEventListener('click', (event) => {
          const link = event.target.closest('[data-kitchen-facets] a, [data-kitchen-results] .pager a');
          if (!link || event.metaKey || event.ctrlKey || event.shiftKey) {
            return;
          }
          event.preventDefault();
          load(link.href, true);
        });
        window.addEventListener('popstate', () => window.location.reload());
      });
    },
  };
})(Drupal, once, Drupal.debounce);

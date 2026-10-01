# Drupal 11 with drupal/meilisearch, Facets and Drush.
#
# The module comes from drupal.org, unless the build gets a "module" context
# with a local checkout (compose.yaml does, for development).
FROM scratch AS module

FROM drupal:11-php8.3-apache

# APCu keeps Drupal's bootstrap, config and discovery caches in memory, so
# search-as-you-type pages render quickly.
RUN pecl install apcu && docker-php-ext-enable apcu

WORKDIR /opt/drupal
COPY --from=module . /opt/meilisearch-module
ARG MEILISEARCH_MODULE_VERSION=^1.0@alpha
RUN if [ -f /opt/meilisearch-module/composer.json ]; then \
      composer config repositories.meilisearch '{"type": "path", "url": "/opt/meilisearch-module", "options": {"symlink": true}}' \
      && module='drupal/meilisearch:*@dev'; \
    else \
      module="drupal/meilisearch:${MEILISEARCH_MODULE_VERSION}"; \
    fi \
 && composer config allow-plugins.php-http/discovery true \
 && composer config allow-plugins.tbachert/spi true \
 && composer require --no-interaction --no-progress \
      "$module" 'drupal/facets:^3' 'drush/drush:^13'

COPY docker /opt/drupal/docker
RUN cp docker/php/demo.ini /usr/local/etc/php/conf.d/zz-demo.ini \
 && cp docker/apache/demo.conf /etc/apache2/conf-enabled/zz-demo.conf
COPY web/modules/custom /opt/drupal/web/modules/custom
COPY web/themes/custom /opt/drupal/web/themes/custom

ENTRYPOINT ["/opt/drupal/docker/entrypoint.sh"]
CMD ["apache2-foreground"]

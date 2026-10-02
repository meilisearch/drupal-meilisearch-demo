# Drupal 11 with drupal/meilisearch, Facets and Drush.
#
# MEILISEARCH_MODULE_SOURCE picks where the module comes from:
#   release  the drupal.org release (default)
#   local    a checkout passed as the "module" build context
#            (compose.module.yaml does both)
ARG MEILISEARCH_MODULE_SOURCE=release

FROM drupal:11-php8.3-apache AS base

# APCu keeps Drupal's bootstrap, config and discovery caches in memory, so
# search-as-you-type pages render quickly.
RUN pecl install apcu && docker-php-ext-enable apcu

WORKDIR /opt/drupal
RUN composer config allow-plugins.php-http/discovery true \
 && composer config allow-plugins.tbachert/spi true

FROM base AS release
ARG MEILISEARCH_MODULE_VERSION=^1.0@alpha
RUN composer require --no-interaction --no-progress \
      "drupal/meilisearch:${MEILISEARCH_MODULE_VERSION}" 'drupal/facets:^3' 'drush/drush:^13'

FROM base AS local
COPY --from=module . /opt/meilisearch-module
RUN composer config repositories.meilisearch '{"type": "path", "url": "/opt/meilisearch-module", "options": {"symlink": true}}' \
 && composer require --no-interaction --no-progress \
      'drupal/meilisearch:*@dev' 'drupal/facets:^3' 'drush/drush:^13'

FROM ${MEILISEARCH_MODULE_SOURCE}

COPY docker /opt/drupal/docker
RUN cp docker/php/demo.ini /usr/local/etc/php/conf.d/zz-demo.ini \
 && cp docker/apache/demo.conf /etc/apache2/conf-enabled/zz-demo.conf
COPY web/modules/custom /opt/drupal/web/modules/custom
COPY web/themes/custom /opt/drupal/web/themes/custom

ENTRYPOINT ["/opt/drupal/docker/entrypoint.sh"]
CMD ["apache2-foreground"]

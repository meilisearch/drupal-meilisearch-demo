# Drupal 11 with drupal/meilisearch from a local checkout (build context
# "module", see compose.yaml), Facets and Drush.
FROM drupal:11-php8.3-apache

WORKDIR /opt/drupal
COPY --from=module . /opt/meilisearch-module
RUN composer config repositories.meilisearch '{"type": "path", "url": "/opt/meilisearch-module", "options": {"symlink": true}}' \
 && composer config allow-plugins.php-http/discovery true \
 && composer config allow-plugins.tbachert/spi true \
 && composer require --no-interaction --no-progress \
      'drupal/meilisearch:*@dev' 'drupal/facets:^3' 'drush/drush:^13'

COPY docker /opt/drupal/docker
COPY web/modules/custom /opt/drupal/web/modules/custom
COPY web/themes/custom /opt/drupal/web/themes/custom

ENTRYPOINT ["/opt/drupal/docker/entrypoint.sh"]
CMD ["apache2-foreground"]

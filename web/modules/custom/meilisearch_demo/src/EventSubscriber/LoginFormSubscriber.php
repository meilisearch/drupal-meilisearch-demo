<?php

declare(strict_types=1);

namespace Drupal\meilisearch_demo\EventSubscriber;

use Drupal\Core\Site\Settings;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\RequestEvent;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Symfony\Component\HttpKernel\KernelEvents;

/**
 * Hides the login and password forms of a public demo.
 *
 * A public login form invites credential stuffing and brute force, so a
 * deployed demo answers "404 Not Found" on it. One-time login links
 * (drush user:login) keep working, for whoever runs the demo.
 *
 * The form is on when $settings['meilisearch_demo_login_form'] is TRUE, as in
 * the local Docker Compose setup.
 */
final class LoginFormSubscriber implements EventSubscriberInterface {

  /**
   * Routes that show or accept a user name and password.
   */
  private const ROUTES = [
    'user.login',
    'user.login.http',
    'user.login_status.http',
    'user.pass',
    'user.pass.http',
    'user.register',
  ];

  /**
   * {@inheritdoc}
   */
  public static function getSubscribedEvents(): array {
    // Right after routing (32), before any controller builds a form.
    return [KernelEvents::REQUEST => ['onRequest', 30]];
  }

  /**
   * Answers "404 Not Found" on the login routes when the form is off.
   */
  public function onRequest(RequestEvent $event): void {
    if (Settings::get('meilisearch_demo_login_form', FALSE)) {
      return;
    }
    if (in_array($event->getRequest()->attributes->get('_route'), self::ROUTES, TRUE)) {
      throw new NotFoundHttpException();
    }
  }

}

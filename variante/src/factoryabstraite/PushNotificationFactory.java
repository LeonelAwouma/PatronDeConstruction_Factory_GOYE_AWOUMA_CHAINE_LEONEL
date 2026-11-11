package factoryabstraite;

/**
 * Fabrique concrete : sait creer une PushNotification.
 */
public class PushNotificationFactory extends NotificationFactory {
    @Override
    protected Notification creerNotification() {
        return new PushNotification();
    }
}

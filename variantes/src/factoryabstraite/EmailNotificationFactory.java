package factoryabstraite;

/**
 * Fabrique concrete : sait creer une EmailNotification.
 */
public class EmailNotificationFactory extends NotificationFactory {
    @Override
    protected Notification creerNotification() {
        return new EmailNotification();
    }
}

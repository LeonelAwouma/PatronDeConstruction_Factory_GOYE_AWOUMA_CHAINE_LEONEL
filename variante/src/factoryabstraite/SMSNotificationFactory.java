package factoryabstraite;

/**
 * Fabrique concrete : sait creer une SMSNotification.
 */
public class SMSNotificationFactory extends NotificationFactory {
    @Override
    protected Notification creerNotification() {
        return new SMSNotification();
    }
}

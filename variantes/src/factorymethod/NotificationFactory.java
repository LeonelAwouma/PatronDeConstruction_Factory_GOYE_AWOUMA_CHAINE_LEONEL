package factorymethod;

/**
 * NotificationFactory : role FabriqueProduit.
 * La methode de fabrique creerNotification(canal) recoit le canal choisi
 * (EMAIL, SMS, PUSH) et decide quelle classe concrete instancier.
 */
public class NotificationFactory {
    public static final String EMAIL = "EMAIL";
    public static final String SMS = "SMS";
    public static final String PUSH = "PUSH";

    public Notification creerNotification(String canal) {
        Notification notification = null;
        switch (canal.toUpperCase()) {
            case EMAIL:
                notification = new EmailNotification();
                break;
            case SMS:
                notification = new SMSNotification();
                break;
            case PUSH:
                notification = new PushNotification();
                break;
            default:
                throw new IllegalArgumentException("Canal de notification inconnu : " + canal);
        }
        return notification;
    }
}

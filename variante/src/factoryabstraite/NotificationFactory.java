package factoryabstraite;

/**
 * Fabrique abstraite : declare la methode de fabrique creerNotification()
 * et implemente le traitement commun qui l'utilise (notifier).
 * Chaque sous-classe decide du type concret de notification.
 */
public abstract class NotificationFactory {
    public void notifier(String destinataire, String message) {
        Notification notification = creerNotification();
        notification.envoyer(destinataire, message);
    }

    protected abstract Notification creerNotification();
}

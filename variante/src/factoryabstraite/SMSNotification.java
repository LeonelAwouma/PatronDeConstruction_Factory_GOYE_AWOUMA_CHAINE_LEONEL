package factoryabstraite;

public class SMSNotification extends Notification {
    @Override
    public void envoyer(String destinataire, String message) {
        System.out.println("[SMS]   Vers " + destinataire + " : " + message);
    }
}

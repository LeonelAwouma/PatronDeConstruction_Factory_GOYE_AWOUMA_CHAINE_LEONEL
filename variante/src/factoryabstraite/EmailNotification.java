package factoryabstraite;

public class EmailNotification extends Notification {
    @Override
    public void envoyer(String destinataire, String message) {
        System.out.println("[EMAIL] A : " + destinataire + " : " + message);
    }
}

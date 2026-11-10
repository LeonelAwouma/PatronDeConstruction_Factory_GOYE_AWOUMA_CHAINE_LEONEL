package factorymethod;

public class SMSNotification extends Notification {
    @Override
    public void envoyer(String destinataire, String message) {
        String texte = message.length() > 160 ? message.substring(0, 157) + "..." : message;
        System.out.println("[SMS]   Vers " + destinataire + " : " + texte);
    }
}

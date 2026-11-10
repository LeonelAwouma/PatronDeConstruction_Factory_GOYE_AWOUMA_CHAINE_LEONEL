package factorymethod;

public class PushNotification extends Notification {
    @Override
    public void envoyer(String destinataire, String message) {
        System.out.println("[PUSH]  Appareil " + destinataire + " -> \"" + message + "\"");
    }
}

package factorymethod;

public class EmailNotification extends Notification {
    @Override
    public void envoyer(String destinataire, String message) {
        System.out.println("[EMAIL] A : " + destinataire);
        System.out.println("        Objet : Notification");
        System.out.println("        Corps : " + message);
    }
}

package factoryabstraite;

public class Client {
    public static void main(String[] args) {
        System.out.println("............Variante 2 : Notifications (fabrique abstraite)............");
        NotificationFactory[] fabriques = {
            new EmailNotificationFactory(),
            new SMSNotificationFactory(),
            new PushNotificationFactory()
        };
        for (NotificationFactory fabrique : fabriques) {
            fabrique.notifier("etudiant@univ.cm", "Votre devoir INF4067 a ete recu.");
        }
    }
}

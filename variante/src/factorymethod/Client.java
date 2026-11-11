package factorymethod;

/**
 * Client : le canal est choisi a l'execution (ici via les arguments de la ligne de commande,
 * sinon les trois canaux sont testes). Le client ne connait que Notification et la fabrique.
 */
public class Client {
    public static void main(String[] args) {
        System.out.println("............Variante 1 : Notifications (Factory Method)............");
        NotificationFactory fabrique = new NotificationFactory();
        String[] canaux = args.length > 0 ? args : new String[] {"EMAIL", "SMS", "PUSH", "FAX"};

        for (String canal : canaux) {
            try {
                Notification notification = fabrique.creerNotification(canal);
                notification.envoyer("etudiant@univ.cm", "Votre devoir INF4067 a ete recu.");
            } catch (IllegalArgumentException e) {
                System.out.println("Erreur : " + e.getMessage());
            }
        }
    }
}

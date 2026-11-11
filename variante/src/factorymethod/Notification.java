package factorymethod;

/**
 * Notification : classe abstraite (role Produit).
 * Toute notification sait s'envoyer a un destinataire avec un message.
 */
public abstract class Notification {
    public abstract void envoyer(String destinataire, String message);
}

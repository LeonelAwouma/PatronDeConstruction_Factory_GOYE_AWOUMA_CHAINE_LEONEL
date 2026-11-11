package factorymethod;

/**
 * Client : programme qui fait appel a la fabrique pour obtenir des objets de type Produit.
 * Le type a creer n'est connu qu'a l'execution.
 */
public class Client {
    public static void main(String[] args) {
        System.out.println("............Methode 1: Factory Method............");

        FabriqueProduit fabriqueproduit = new FabriqueProduit();
        Produit produit = null;

        // affiche un produit de type A
        produit = fabriqueproduit.createProduit(FabriqueProduit.typeA);
        produit.methodeproduit();
        // affiche un produit de type B
        produit = fabriqueproduit.createProduit(FabriqueProduit.typeB);
        produit.methodeproduit();
        // affiche un produit de type C
        produit = fabriqueproduit.createProduit(FabriqueProduit.typeC);
        produit.methodeproduit();

        // produit inexistant : la fabrique leve une exception
        String d = "D";
        try {
            produit = fabriqueproduit.createProduit(d);
            produit.methodeproduit();
        } catch (IllegalArgumentException e) {
            System.out.println("Erreur : " + e.getMessage() + " (" + d + ")");
        }
    }
}

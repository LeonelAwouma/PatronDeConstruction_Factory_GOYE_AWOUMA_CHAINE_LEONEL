package factorymethod;

public class ProduitA extends Produit {
    public ProduitA() {
    }

    @Override
    public void methodeproduit() {
        System.out.println("je suis un produit de type A");
        System.out.println("produitA.methodeproduit()");
    }
}

package factorymethod;

public class ProduitB extends Produit {
    @Override
    public void methodeproduit() {
        System.out.println("je suis un produit de type B");
        System.out.println("produitB.methodeproduit()");
    }
}

package factoryabstraite;

/**
 * FabriqueConcrete : implemente la methode fabrique pour creer un ProduitB.
 */
public class ProduitFactoryB extends ProduitFactory {
    @Override
    protected Produit createProduit() {
        Produit produit = null;
        produit = new ProduitB();
        return produit;
    }
}

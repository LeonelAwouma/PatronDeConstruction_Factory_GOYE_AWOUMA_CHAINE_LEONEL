package factoryabstraite;

/**
 * FabriqueConcrete : implemente la methode fabrique pour creer un ProduitA.
 */
public class ProduitFactoryA extends ProduitFactory {
    @Override
    protected Produit createProduit() {
        Produit produit = null;
        produit = new ProduitA();
        return produit;
    }
}

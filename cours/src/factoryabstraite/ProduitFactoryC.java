package factoryabstraite;

/**
 * FabriqueConcrete : implemente la methode fabrique pour creer un ProduitC.
 */
public class ProduitFactoryC extends ProduitFactory {
    @Override
    protected Produit createProduit() {
        Produit produit = null;
        produit = new ProduitC();
        return produit;
    }
}

package factoryabstraite;

/**
 * FabriqueAbstraite : abrite la signature de la methode de fabrique (createProduit)
 * et l'implementation des methodes qui l'invoquent (getProduit).
 * Ce sont les sous-classes concretes qui decident quel produit instancier.
 */
public abstract class ProduitFactory {
    public Produit getProduit() {
        return createProduit();
    }

    protected abstract Produit createProduit();
}

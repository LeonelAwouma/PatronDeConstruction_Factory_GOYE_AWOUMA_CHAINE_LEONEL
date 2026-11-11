package factorymethod;

/**
 * Produit : classe abstraite dont les sous-classes seront instanciees par la fabrique.
 * L'objet retourne par la fabrique est toujours de ce type (classe mere).
 */
public abstract class Produit {
    public abstract void methodeproduit();
}

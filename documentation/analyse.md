# Analyse du patron Factory

## Problème

L'opérateur `new` crée un couplage fort entre le client et la classe instanciée. Si le client choisit
la classe avec une instruction conditionnelle, chaque ajout de classe oblige à le modifier.

## Solution

Le client ne connaît que la classe mère abstraite (`Produit`, `Notification`) et délègue la création
à une fabrique. Le polymorphisme fait le reste.

| Forme | Principe | Cours | Variante |
|-------|----------|-------|----------|
| Factory Method | Une méthode de création reçoit le type et instancie la classe correspondante. | `FabriqueProduit.createProduit(type)` | `NotificationFactory.creerNotification(canal)` |
| Fabrique abstraite | La fabrique abstraite déclare `createProduit()` ; chaque sous-classe crée son produit. | `ProduitFactory` et `ProduitFactoryA/B/C` | `NotificationFactory` et `Email/SMS/PushNotificationFactory` |

## Pourquoi Factory convient à la variante

- Le canal (e-mail, SMS, push) n'est connu qu'à l'exécution.
- La création est centralisée : ajouter un canal ne touche pas au client.

## Comparaison des deux formes

| Forme | Avantage | Limite |
|-------|----------|--------|
| Factory Method | Une seule fabrique, simple. | Le `switch` est modifié à chaque nouveau produit. |
| Fabrique abstraite | Extension sans modifier l'existant (ouvert/fermé). | Plus de classes. |

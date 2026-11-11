# Patron de construction : Factory (Fabrique)

Devoir n° 1 – INF4067 / INF461 – Patrons de construction.
Ce dépôt contient l'implémentation du patron **Factory** sous ses deux formes vues en cours,
appliquée à l'exemple du cours puis à un exemple modifié (gestion de notifications).

## Structure du dépôt

```
Factory/
├── Cours/                      Exemple du cours (produits A, B, C)
│   ├── src/factorymethod/      Forme 1 : fabrique avec méthode de création paramétrée
│   ├── src/factoryabstraite/   Forme 2 : fabrique abstraite + fabriques concrètes
│   └── uml/                    Diagrammes DIA (.dia) et exports (.png)
└── variantes/                  Exemple modifié (notifications Email / SMS / Push)
│   ├── src/factorymethod/
│   ├── src/factoryabstraite/
│   └── uml/
```

## Les deux formes du patron Factory 

| Forme | Principe | Classes (cours) | Classes (variante) |
|-------|----------|-----------------|--------------------|
| Factory Method | Une fabrique concrète expose `createProduit(type)`. Le type reçu en paramètre détermine la classe à instancier. | `FabriqueProduit`, `Produit`, `ProduitA/B/C`, `Client` | `NotificationFactory`, `Notification`, `Email/SMS/PushNotification`, `Client` |
| Fabrique abstraite | `ProduitFactory` déclare `createProduit()` abstraite et `getProduit()` qui l'appelle. Chaque sous-classe (`ProduitFactoryA/B/C`) instancie son produit. | `ProduitFactory`, `ProduitFactoryA/B/C`, `Produit`, `ProduitA/B/C`, `Client` | `NotificationFactory`, `Email/SMS/PushNotificationFactory`, `Notification`, `Email/SMS/PushNotification`, `Client` |

Dans les deux cas, le client ne manipule que la classe mère `Produit` (ou `Notification`) :
le polymorphisme spécialise le traitement, et aucun `new` de classe concrète n'apparaît chez le client.

## Exemple modifié : système de notifications

Une application doit prévenir un utilisateur par **e-mail**, **SMS** ou **notification push**.
Le canal n'est connu qu'à l'exécution (préférence de l'utilisateur, argument de la ligne de commande).
La fabrique centralise la création : ajouter un canal (ex. WhatsApp) revient à ajouter une
sous-classe de `Notification` et un cas dans la fabrique, sans toucher au client.

## Compilation et exécution

Prérequis : JDK 17 ou supérieur.

```bash
# Exemple du cours
javac -d out/cours $(find Cours/src -name '*.java')
java -cp out/cours factorymethod.Client
java -cp out/cours factoryabstraite.Client

# Exemple modifié
javac -d out/variantes $(find variantes/src -name '*.java')
java -cp out/variantes factorymethod.Client            # teste EMAIL, SMS, PUSH et un canal inconnu
java -cp out/variantes factorymethod.Client SMS PUSH   # canaux choisis à l'exécution
java -cp out/variantes factoryabstraite.Client
```

## Résultat attendu (extrait)

```
............Methode 1: Factory Method............
je suis un produit de type A
produitA.methodeproduit()
...
Erreur : Type de produit inconnu (D)
```

## Diagrammes UML

| Diagramme | Fichier DIA | Image |
|-----------|-------------|-------|
| Cours, Factory Method | `Cours/uml/factory_method.dia` | ![Factory Method](Cours/uml/factory_method.png) |
| Cours, fabrique abstraite | `Cours/uml/factory_abstraite.dia` | ![Fabrique abstraite](Cours/uml/factory_abstraite.png) |
| Variante, Factory Method | `variantes/uml/notification_factory_method.dia` | ![Notifications Factory Method](variantes/uml/notification_factory_method.png) |
| Variante, fabrique abstraite | `variantes/uml/notification_factory_abstraite.dia` | ![Notifications fabrique abstraite](variantes/uml/notification_factory_abstraite.png) |

## Auteur

GOYE AWOUMA CHAINE LEONEL – INF4067.
Dépôt : https://github.com/LeonelAwouma/PatronDeConstruction_Factory_GOYE_AWOUMA_CHAINE_LEONEL

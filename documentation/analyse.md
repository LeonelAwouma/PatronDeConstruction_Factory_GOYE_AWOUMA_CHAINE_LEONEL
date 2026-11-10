# Analyse du patron Factory

## 1. Problème résolu

Dans un langage objet, créer un objet se fait avec `new ClasseConcrete()`. Cette instruction
crée un **couplage fort** entre l'appelant et la classe instanciée : si la hiérarchie change
(nouveau produit, produit renommé), tout le code client doit être modifié. De plus, la classe
passée à `new` ne peut pas être une variable : on ne peut pas paramétrer la création.

Le patron Factory répond à ce problème en **centralisant la création** dans une fabrique et en
ne rendant visible au client que la **classe mère** (abstraite). Le client dépend d'une
abstraction (relation classe-à-interface, couplage faible) et non des classes concrètes.

## 2. Modèle générique retenu

Le support INF461 présente deux manières d'implémenter la fabrique. Les deux sont réalisées
ici, pour l'exemple du cours comme pour la variante.

### Forme 1 : fabrique avec méthode de création paramétrée (« Factory Method », slides 16-23)

| Participant | Cours | Variante |
|-------------|-------|----------|
| Produit (abstrait) | `Produit` | `Notification` |
| ProduitConcret | `ProduitA`, `ProduitB`, `ProduitC` | `EmailNotification`, `SMSNotification`, `PushNotification` |
| Fabrique | `FabriqueProduit.createProduit(type)` | `NotificationFactory.creerNotification(canal)` |
| Client | `Client.main` | `Client.main` |

La méthode de fabrique reçoit la donnée nécessaire (une chaîne `"A"`, `"EMAIL"`...) et choisit la
classe à instancier avec un `switch`. Un type inconnu lève `IllegalArgumentException`.

Avantage : une seule fabrique, simple à utiliser quand le choix dépend d'une valeur connue à
l'exécution. Limite : le `switch` doit être modifié pour chaque nouveau produit.

### Forme 2 : fabrique abstraite et fabriques concrètes (slides 24-30)

| Participant | Cours | Variante |
|-------------|-------|----------|
| FabriqueAbstraite | `ProduitFactory` (`getProduit()` + `createProduit()` abstraite) | `NotificationFactory` (`notifier()` + `creerNotification()` abstraite) |
| FabriqueConcrete | `ProduitFactoryA/B/C` | `EmailNotificationFactory`, `SMSNotificationFactory`, `PushNotificationFactory` |
| Produit / ProduitConcret | identiques à la forme 1 | identiques à la forme 1 |
| Client | choisit une fabrique concrète | choisit une fabrique concrète |

La classe abstraite contient la signature de la méthode de fabrique **et** le code qui l'invoque
(`getProduit()` / `notifier()`). Les sous-classes ne redéfinissent que la création.

Avantage : ajouter un produit = ajouter une sous-classe de produit et une sous-classe de fabrique,
**sans modifier** le code existant (principe ouvert/fermé). Limite : plus de classes.

## 3. Pourquoi le patron Factory convient à la variante

Le système de notifications remplit les deux conditions d'utilisation données en cours :

1. **Le type d'objet n'est connu qu'à l'exécution** : le canal (e-mail, SMS, push) dépend de la
   préférence de l'utilisateur ou d'un argument de la ligne de commande.
2. **On veut centraliser la création** : les règles propres à chaque canal (format, troncature
   d'un SMS à 160 caractères...) sont dans chaque classe concrète, et le choix de la classe est
   dans la fabrique. Le client se contente d'appeler `envoyer()`.

Le client ne contient aucun `new EmailNotification()` : il manipule uniquement `Notification`.
Remplacer un canal par un autre ou en ajouter un (WhatsApp, Telegram) n'impacte pas le client.

## 4. Différence avec Abstract Factory

Factory crée **un** produit d'une hiérarchie. Abstract Factory fournit une interface pour créer
**une famille** de produits liés (par exemple Scooter + Automobile, en version Essence ou
Électrique). Abstract Factory fait l'objet d'un dépôt distinct dans ce devoir.

## 5. Diagrammes

Les diagrammes DIA se trouvent dans `Cours/uml/` et `variantes/uml/`. Convention : `Produit`,
`Notification`, `ProduitFactory` et `NotificationFactory` (forme 2) sont des classes abstraites,
représentées en italique. Les flèches pointillées `<<instantiate>>` relient chaque fabrique au
produit concret qu'elle crée ; les flèches pleines à triangle vide représentent l'héritage.

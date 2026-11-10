"""Build the HTML report for the Factory pattern from the repository sources."""
import html, os, sys, base64

ROOT = sys.argv[1]
OUT = sys.argv[2]
REPO = "https://github.com/LeonelAwouma/PatronDeConstruction_Factory_GOYE_AWOUMA_CHAINE_LEONEL"


def src(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return html.escape(f.read().rstrip())


def img(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def code_block(title, path):
    return f'<div class="file"><div class="fname">{html.escape(title)}</div><pre><code>{src(path)}</code></pre></div>'


def files(prefix, names):
    return "\n".join(code_block(f"{prefix}/{n}.java", f"{prefix}/{n}.java") for n in names)


CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: Calibri, "Segoe UI", Arial, sans-serif; font-size: 11pt; color: #1a1a1a; line-height: 1.4; }
h1 { font-size: 22pt; color: #8a6d1f; border-bottom: 2px solid #c9a227; padding-bottom: 4px; margin-top: 0; }
h2 { font-size: 16pt; color: #8a6d1f; margin-top: 22px; page-break-after: avoid; }
h3 { font-size: 13pt; color: #333; margin-top: 16px; page-break-after: avoid; }
p { margin: 6px 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 10pt; page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 4px 6px; vertical-align: top; }
th { background: #f3e9c9; text-align: left; }
.file { page-break-inside: avoid; margin: 8px 0; }
.fname { font-family: Consolas, monospace; font-size: 9pt; background: #e8e8e8; padding: 3px 6px; border: 1px solid #ccc; border-bottom: none; }
pre { page-break-inside: avoid; margin: 0; background: #fafafa; border: 1px solid #ccc; padding: 6px; font-family: Consolas, "Courier New", monospace; font-size: 8.6pt; white-space: pre-wrap; line-height: 1.25; }
.fig { text-align: center; margin: 10px 0; page-break-inside: avoid; }
.fig img { max-width: 100%; max-height: 165mm; border: 1px solid #ddd; }
.cap { font-size: 9.5pt; color: #555; margin-top: 4px; }
.cover { text-align: center; margin-top: 120px; page-break-after: always; }
.cover .u { font-size: 13pt; color: #555; }
.cover .t { font-size: 28pt; color: #8a6d1f; margin: 40px 0 10px; font-weight: bold; }
.cover .s { font-size: 16pt; margin-bottom: 60px; }
.cover .m { font-size: 12pt; line-height: 1.8; }
.pb { page-break-before: always; }
ul { margin: 4px 0 4px 18px; }
a { color: #1a4f8a; }
.note { background: #fff8e1; border-left: 4px solid #c9a227; padding: 6px 10px; margin: 8px 0; }
"""

FM = ["Produit", "ProduitA", "ProduitB", "ProduitC", "FabriqueProduit", "Client"]
FA = ["Produit", "ProduitA", "ProduitB", "ProduitC", "ProduitFactory", "ProduitFactoryA", "ProduitFactoryB", "ProduitFactoryC", "Client"]
VM = ["Notification", "EmailNotification", "SMSNotification", "PushNotification", "NotificationFactory", "Client"]
VA = ["Notification", "EmailNotification", "SMSNotification", "PushNotification", "NotificationFactory",
      "EmailNotificationFactory", "SMSNotificationFactory", "PushNotificationFactory", "Client"]

body = f"""
<div class="cover">
  <div class="u">Université de Yaoundé I<br>INF4067 / INF461 – Principes et processus du logiciel</div>
  <div class="t">Patron de construction<br>Factory (Fabrique)</div>
  <div class="s">Devoir n° 1 – Design Patterns : patrons de construction</div>
  <div class="m">
    <b>Étudiant :</b> GOYE AWOUMA CHAINE LEONEL<br>
    <b>Enseignant :</b> Pr KIMBI XAVERIA<br>
    <b>Dépôt GitHub :</b> <a href="{REPO}">{REPO}</a><br>
    <b>Date :</b> 10 novembre 2026
  </div>
</div>

<h1>1. Nom du patron</h1>
<p><b>Factory</b> (en français <b>Fabrique</b>). C'est un patron de <b>construction</b> (création) : il abstrait
le mécanisme de création d'objets. Le support de cours le présente sous deux formes :</p>
<ul>
  <li><b>Factory Method</b> : une fabrique possède une méthode de création qui reçoit les données nécessaires
      (par exemple une chaîne « A », « B », « C ») pour déterminer le type de l'objet à créer.</li>
  <li><b>Factory avec fabrique abstraite</b> : une classe de fabrique abstraite déclare la méthode de fabrique,
      et ce sont ses sous-classes concrètes qui créent les objets.</li>
</ul>

<h2>1.1 Problème résolu</h2>
<p>Dans un langage objet, la création se fait avec l'opérateur <code>new</code>. Son utilisation est « mauvaise »
car elle crée un <b>couplage fort</b> entre l'appelant et la classe instanciée : une relation classe-à-classe
est fragile. De plus, la classe passée à <code>new</code> ne peut pas être remplacée par une variable, donc on
ne peut pas paramétrer la création. Avec une instruction conditionnelle chez le client, chaque changement dans
la hiérarchie des classes oblige à modifier le code du client.</p>
<p>La solution est une relation <b>classe-à-interface</b> : le client ne connaît que la classe mère (abstraite)
et délègue la création à une fabrique. Le couplage devient faible et le <b>polymorphisme</b> spécialise les
traitements.</p>

<h2>1.2 Quand l'utiliser</h2>
<ul>
  <li>Le client ne peut déterminer le type d'objet à créer qu'à l'<b>exécution</b>.</li>
  <li>Il y a une volonté de <b>centraliser</b> la création d'objets.</li>
  <li>L'objet à créer fait partie d'un ensemble de sous-classes, et l'objet retourné est toujours du type de la classe mère.</li>
</ul>

<h1 class="pb">2. Modèle générique</h1>

<h2>2.1 Forme 1 : Factory Method</h2>
<p>Structure générique (support, slide 17) : le <b>Client</b> utilise une <b>Fabrique</b> dont la méthode
<code>methodeFabrique() : Produit</code> instancie un <b>ProduitConcret</b>, sous-classe de <b>Produit</b>.</p>
<table>
  <tr><th>Participant</th><th>Rôle</th></tr>
  <tr><td>Produit</td><td>Classe abstraite (ou interface) dont les sous-classes seront instanciées.</td></tr>
  <tr><td>ProduitConcret</td><td>Les sous-classes concrètes à instancier.</td></tr>
  <tr><td>Fabrique</td><td>Contient la méthode de fabrique ; elle reçoit les données nécessaires pour choisir la classe à instancier.</td></tr>
  <tr><td>Client</td><td>Programme qui fait appel à la fabrique pour obtenir des objets de type Produit.</td></tr>
</table>

<h2>2.2 Forme 2 : Factory avec fabrique abstraite</h2>
<p>Structure générique (support, slide 24) : une <b>FabriqueAbstraite</b> abrite la signature de la méthode de
fabrique et l'implémentation des méthodes qui l'invoquent ; une ou plusieurs <b>FabriqueConcrete</b>
implémentent la méthode de fabrique et instancient le <b>ProduitConcret</b>.</p>
<div class="fig"><img src="{img('Cours/uml/factory_abstraite.png')}">
<div class="cap">Figure 1 – Modèle générique de la forme 2, reproduit avec DIA d'après la slide 24.</div></div>
<table>
  <tr><th>Participant</th><th>Rôle</th></tr>
  <tr><td>FabriqueAbstraite</td><td>Classe abstraite : signature de la méthode de fabrique et méthodes qui l'invoquent.</td></tr>
  <tr><td>FabriqueConcrete</td><td>Classe concrète qui implémente la méthode de fabrique. Il peut y en avoir plusieurs.</td></tr>
  <tr><td>Produit / ProduitConcret</td><td>Classe abstraite et ses sous-classes concrètes à instancier.</td></tr>
  <tr><td>Client</td><td>Programme qui fait appel à la fabrique.</td></tr>
</table>

<h2>2.3 Différence avec Abstract Factory</h2>
<p>Factory crée <b>un</b> produit d'une hiérarchie. Abstract Factory fournit une interface unique pour créer
<b>une famille</b> d'objets liés (par exemple Scooter et Automobile, en version Essence ou Électrique).
Abstract Factory est un patron distinct, traité dans un autre dépôt.</p>

<h1>3. Exemple du cours</h1>
<p><b>Énoncé</b> : on gère trois types de produits dans un système. Le programme qui manipule ces produits ne
connaît le type de produit à exécuter que lors de l'exécution. On utilise le patron Factory pour gérer cette
situation, d'abord avec Factory Method (slides 18 à 23), puis avec une fabrique abstraite (slides 26 à 30).</p>

<h2>3.1 Modélisation – Factory Method</h2>
<div class="fig"><img src="{img('Cours/uml/factory_method.png')}">
<div class="cap">Figure 2 – Diagramme de classes de l'exemple du cours, forme Factory Method (DIA, d'après la slide 19).</div></div>
<div class="note">Le diagramme de la slide 19 présente <code>Produit</code> comme une interface alors que le code
des slides 20 et 28 la déclare <code>abstract class</code>. Le rendu suit le code : <code>Produit</code> est une
classe abstraite.</div>

<h2>3.2 Modélisation – fabrique abstraite</h2>
<p>La hiérarchie des fabriques (slide 27) : <code>ProduitFactory</code> abstraite avec <code>getProduit()</code>
qui appelle <code>createProduit()</code> abstraite ; <code>ProduitFactoryA</code>, <code>ProduitFactoryB</code>
et <code>ProduitFactoryC</code> instancient respectivement <code>ProduitA</code>, <code>ProduitB</code> et
<code>ProduitC</code>. Le modèle générique correspondant est la figure 1.</p>

<h2>3.3 Code source – Factory Method (Cours/src/factorymethod)</h2>
{files('Cours/src/factorymethod', FM)}

<h2>3.4 Code source – fabrique abstraite (Cours/src/factoryabstraite)</h2>
{files('Cours/src/factoryabstraite', FA)}

<h2>3.5 Résultat de l'exécution</h2>
<pre>............Methode 1: Factory Method............
je suis un produit de type A
produitA.methodeproduit()
je suis un produit de type B
produitB.methodeproduit()
je suis un produit de type C
produitC.methodeproduit()
Erreur : Type de produit inconnu (D)

............Methode 2: Factory avec fabrique abstraite............
je suis un produit de type A
produitA.methodeproduit()
je suis un produit de type B
produitB.methodeproduit()
je suis un produit de type C
produitC.methodeproduit()</pre>

<h1 class="pb">4. Exemple modifié : système de notifications</h1>
<p><b>Énoncé</b> : une application doit prévenir un utilisateur par <b>e-mail</b>, <b>SMS</b> ou
<b>notification push</b>. Le canal n'est connu qu'à l'exécution : il dépend de la préférence de l'utilisateur
ou d'un argument de la ligne de commande. Le programme ne doit manipuler que la classe mère
<code>Notification</code>. On utilise le patron Factory dans ses deux formes.</p>
<table>
  <tr><th>Participant du modèle</th><th>Exemple du cours</th><th>Exemple modifié</th></tr>
  <tr><td>Produit</td><td>Produit, methodeproduit()</td><td>Notification, envoyer(destinataire, message)</td></tr>
  <tr><td>ProduitConcret</td><td>ProduitA, ProduitB, ProduitC</td><td>EmailNotification, SMSNotification, PushNotification</td></tr>
  <tr><td>Fabrique (forme 1)</td><td>FabriqueProduit.createProduit(type)</td><td>NotificationFactory.creerNotification(canal)</td></tr>
  <tr><td>FabriqueAbstraite (forme 2)</td><td>ProduitFactory : getProduit(), createProduit()</td><td>NotificationFactory : notifier(), creerNotification()</td></tr>
  <tr><td>FabriqueConcrete (forme 2)</td><td>ProduitFactoryA, B, C</td><td>EmailNotificationFactory, SMSNotificationFactory, PushNotificationFactory</td></tr>
  <tr><td>Client</td><td>Client.main</td><td>Client.main (canal passé en argument)</td></tr>
</table>

<h2>4.1 Modélisation – Factory Method</h2>
<div class="fig"><img src="{img('variantes/uml/notification_factory_method.png')}">
<div class="cap">Figure 3 – Variante Notifications, forme Factory Method (DIA).</div></div>

<h2>4.2 Modélisation – fabrique abstraite</h2>
<div class="fig"><img src="{img('variantes/uml/notification_factory_abstraite.png')}">
<div class="cap">Figure 4 – Variante Notifications, forme fabrique abstraite (DIA).</div></div>

<h2>4.3 Code source – Factory Method (variantes/src/factorymethod)</h2>
{files('variantes/src/factorymethod', VM)}

<h2>4.4 Code source – fabrique abstraite (variantes/src/factoryabstraite)</h2>
{files('variantes/src/factoryabstraite', VA)}

<h2>4.5 Résultat de l'exécution</h2>
<pre>............Variante 1 : Notifications (Factory Method)............
[EMAIL] A : etudiant@univ.cm
        Objet : Notification
        Corps : Votre devoir INF4067 a ete recu.
[SMS]   Vers etudiant@univ.cm : Votre devoir INF4067 a ete recu.
[PUSH]  Appareil etudiant@univ.cm -> "Votre devoir INF4067 a ete recu."
Erreur : Canal de notification inconnu : FAX

............Variante 2 : Notifications (fabrique abstraite)............
[EMAIL] A : etudiant@univ.cm : Votre devoir INF4067 a ete recu.
[SMS]   Vers etudiant@univ.cm : Votre devoir INF4067 a ete recu.
[PUSH]  Appareil etudiant@univ.cm : Votre devoir INF4067 a ete recu.</pre>

<h1 class="pb">5. Analyse et justification</h1>
<p>Le système de notifications remplit les deux conditions d'utilisation du patron Factory données en cours.
Le type d'objet n'est connu qu'à l'exécution, puisque le canal dépend de l'utilisateur. La création est
centralisée dans la fabrique : les règles propres à chaque canal (format d'un e-mail, troncature d'un SMS à
160 caractères) sont dans les classes concrètes, et le choix de la classe est dans la fabrique.</p>
<p>Le client ne contient aucun <code>new EmailNotification()</code> : il manipule uniquement
<code>Notification</code>. Remplacer un canal par un autre ou en ajouter un (WhatsApp, Telegram) n'impacte pas
le client.</p>
<table>
  <tr><th>Forme</th><th>Avantage</th><th>Limite</th></tr>
  <tr><td>Factory Method</td><td>Une seule fabrique, simple quand le choix dépend d'une valeur connue à l'exécution.</td>
      <td>Le <code>switch</code> doit être modifié à chaque nouveau produit.</td></tr>
  <tr><td>Fabrique abstraite</td><td>Ajouter un produit = ajouter une sous-classe de produit et une sous-classe de fabrique, sans modifier le code existant (principe ouvert/fermé).</td>
      <td>Davantage de classes.</td></tr>
</table>

<h1>6. Dépôt GitHub</h1>
<p>Le code source complet (exemple du cours et exemple modifié), les diagrammes DIA avec leurs exports PNG,
le script de compilation et l'analyse sont disponibles à l'adresse :</p>
<p><a href="{REPO}">{REPO}</a></p>
<table>
  <tr><th>Dossier</th><th>Contenu</th></tr>
  <tr><td>Cours/src/factorymethod</td><td>Exemple du cours, forme Factory Method</td></tr>
  <tr><td>Cours/src/factoryabstraite</td><td>Exemple du cours, forme fabrique abstraite</td></tr>
  <tr><td>Cours/uml</td><td>factory_method.dia, factory_abstraite.dia et PNG</td></tr>
  <tr><td>variantes/src/factorymethod</td><td>Variante Notifications, forme Factory Method</td></tr>
  <tr><td>variantes/src/factoryabstraite</td><td>Variante Notifications, forme fabrique abstraite</td></tr>
  <tr><td>variantes/uml</td><td>Diagrammes DIA et PNG de la variante</td></tr>
  <tr><td>documentation</td><td>analyse.md, script de génération des diagrammes</td></tr>
  <tr><td>build.sh</td><td>Compile et exécute les quatre programmes (JDK 17)</td></tr>
</table>
<p>Compilation et exécution :</p>
<pre>javac -d out/cours $(find Cours/src -name '*.java')
java -cp out/cours factorymethod.Client
java -cp out/cours factoryabstraite.Client
javac -d out/variantes $(find variantes/src -name '*.java')
java -cp out/variantes factorymethod.Client SMS PUSH
java -cp out/variantes factoryabstraite.Client</pre>
"""

doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Patron Factory – GOYE AWOUMA CHAINE LEONEL</title><style>{CSS}</style></head><body>{body}</body></html>"""
with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)
print("html ok")

// Génère le rapport Word du patron Factory : node make_report_docx.js <racine du dépôt> <sortie.docx>
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, ImageRun, Footer, PageNumber, PageBreak, BorderStyle, LevelFormat,
  TableLayoutType,
} = require("docx");

const ROOT = process.argv[2];
const OUT = process.argv[3];
const REPO = "https://github.com/LeonelAwouma/PatronDeConstruction_Factory_GOYE_AWOUMA_CHAINE_LEONEL";
const FONT = "Times New Roman";
const MONO = "Courier New";
const CONTENT_W = 9072; // 16 cm en DXA (A4, marges 2,5 cm)

const read = (p) => fs.readFileSync(path.join(ROOT, p), "utf8").replace(/\r/g, "").trimEnd();

// ---------- helpers ----------
const run = (text, opts = {}) => new TextRun({ text, font: FONT, size: 24, color: "000000", ...opts });
const bold = (t) => run(t, { bold: true });
const mono = (t) => run(t, { font: MONO, size: 22 });

function p(children, opts = {}) {
  if (typeof children === "string") children = [run(children)];
  return new Paragraph({ children, alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 276 }, ...opts });
}
// texte avec segments en gras (**x**) et en code (`x`)
function rich(text, opts = {}) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g).filter(Boolean).map((s) => {
    if (s.startsWith("**")) return bold(s.slice(2, -2));
    if (s.startsWith("`")) return mono(s.slice(1, -1));
    return run(s);
  });
  return p(parts, opts);
}
const h1 = (t) => new Paragraph({ text: t, heading: HeadingLevel.HEADING_1 });
const h2 = (t) => new Paragraph({ text: t, heading: HeadingLevel.HEADING_2 });
const bullet = (text) => rich(text, { numbering: { reference: "puces", level: 0 } });

function codeBlock(title, text) {
  const lines = text.split("\n");
  const out = [];
  if (title) {
    out.push(new Paragraph({
      children: [new TextRun({ text: title, font: MONO, size: 18, bold: true, color: "000000" })],
      shading: { type: ShadingType.CLEAR, fill: "D9D9D9", color: "auto" },
      spacing: { before: 120, after: 0 }, keepNext: true,
      border: { top: { style: BorderStyle.SINGLE, size: 4, color: "808080" }, left: { style: BorderStyle.SINGLE, size: 4, color: "808080" }, right: { style: BorderStyle.SINGLE, size: 4, color: "808080" } },
    }));
  }
  lines.forEach((l, i) => {
    const last = i === lines.length - 1;
    out.push(new Paragraph({
      children: [new TextRun({ text: l.replace(/\t/g, "    ") || " ", font: MONO, size: 16, color: "000000" })],
      shading: { type: ShadingType.CLEAR, fill: "F2F2F2", color: "auto" },
      spacing: { before: 0, after: last ? 160 : 0, line: 240 },
      keepNext: !last && i < 3, // garde l'en-tête avec les premières lignes
      border: {
        left: { style: BorderStyle.SINGLE, size: 4, color: "808080" },
        right: { style: BorderStyle.SINGLE, size: 4, color: "808080" },
        ...(i === 0 && !title ? { top: { style: BorderStyle.SINGLE, size: 4, color: "808080" } } : {}),
        ...(last ? { bottom: { style: BorderStyle.SINGLE, size: 4, color: "808080" } } : {}),
      },
    }));
  });
  return out;
}
const javaFiles = (dir, names) => names.flatMap((n) => codeBlock(`${dir}/${n}.java`, read(`${dir}/${n}.java`)));

function table(headers, rows, widths) {
  const cell = (text, i, header) => new TableCell({
    width: { size: widths[i], type: WidthType.DXA },
    shading: header ? { type: ShadingType.CLEAR, fill: "D9D9D9", color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [rich(header ? `**${text}**` : text, { alignment: AlignmentType.LEFT, spacing: { after: 0, line: 240 } })],
  });
  const mk = (cells, header) => new TableRow({ tableHeader: header, cantSplit: true, children: cells.map((c, i) => cell(c, i, header)) });
  const t = new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    layout: TableLayoutType.FIXED,
    rows: [mk(headers, true), ...rows.map((r) => mk(r, false))],
  });
  return [t, new Paragraph({ spacing: { after: 120 } })];
}

function figure(file, caption, num) {
  const buf = fs.readFileSync(path.join(ROOT, file));
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const maxW = 470, maxH = 330; // points approx (px à 96 dpi)
  let W = w, H = h;
  if (W > maxW) { H = (H * maxW) / W; W = maxW; }
  if (H > maxH) { W = (W * maxH) / H; H = maxH; }
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 120, after: 60 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: Math.round(W), height: Math.round(H) } })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [run(`Figure ${num} – ${caption}`, { italics: true, size: 20 })],
    }),
  ];
}

// ---------- contenu ----------
const FM = ["Produit", "ProduitA", "ProduitB", "ProduitC", "FabriqueProduit", "Client"];
const FA = ["Produit", "ProduitA", "ProduitB", "ProduitC", "ProduitFactory", "ProduitFactoryA", "ProduitFactoryB", "ProduitFactoryC", "Client"];
const VM = ["Notification", "EmailNotification", "SMSNotification", "PushNotification", "NotificationFactory", "Client"];
const VA = ["Notification", "EmailNotification", "SMSNotification", "PushNotification", "NotificationFactory", "EmailNotificationFactory", "SMSNotificationFactory", "PushNotificationFactory", "Client"];

const cover = [
  new Paragraph({ spacing: { before: 2400 } }),
  p([run("Université de Yaoundé I", { size: 28 })], { alignment: AlignmentType.CENTER, spacing: { after: 60 } }),
  p([run("Faculté des Sciences – Département d'Informatique", { size: 26 })], { alignment: AlignmentType.CENTER, spacing: { after: 60 } }),
  p([run("INF4067 / INF461 – Principes et processus du logiciel", { size: 26 })], { alignment: AlignmentType.CENTER, spacing: { after: 1200 } }),
  p([run("RAPPORT D'ÉTUDE", { size: 32, bold: true })], { alignment: AlignmentType.CENTER, spacing: { after: 240 } }),
  p([run("Patron de construction Factory (Fabrique)", { size: 40, bold: true })], { alignment: AlignmentType.CENTER, spacing: { after: 240 } }),
  p([run("Devoir n° 1 – Design Patterns : patrons de construction", { size: 28 })], { alignment: AlignmentType.CENTER, spacing: { after: 1600 } }),
  p([bold("Étudiant : "), run("GOYE AWOUMA CHAINE LEONEL")], { alignment: AlignmentType.CENTER, spacing: { after: 120 } }),
  p([bold("Enseignant : "), run("Pr KIMBI XAVERIA")], { alignment: AlignmentType.CENTER, spacing: { after: 120 } }),
  p([bold("Dépôt GitHub : "), run(REPO, { size: 20 })], { alignment: AlignmentType.CENTER, spacing: { after: 120 } }),
  p([bold("Date : "), run("10 novembre 2026")], { alignment: AlignmentType.CENTER }),
];

const body = [
  h1("1. Introduction"),
  rich("Ce rapport présente l'étude du patron de construction **Factory** (Fabrique), réalisée dans le cadre du devoir n° 1 du cours INF4067 / INF461. Il suit le plan demandé : nom du patron, modèle générique, exemple du cours, exemple modifié, code source et lien vers le dépôt GitHub où le code est stocké."),
  rich("Les patrons de création ont pour vocation d'abstraire les mécanismes de création d'objets. Un système qui les utilise devient indépendant de la façon dont les objets sont créés et, en particulier, des mécanismes d'instanciation des classes concrètes. Ils encapsulent l'utilisation des classes concrètes et favorisent ainsi l'utilisation des interfaces."),

  h1("2. Nom du patron"),
  rich("**Factory** (en français **Fabrique**). C'est un patron de construction : il permet de créer un objet dont le type dépend du contexte, cet objet faisant partie d'un ensemble de sous-classes. L'objet retourné est toujours du type de la classe mère et le polymorphisme permet de spécialiser les traitements. Le support de cours le présente sous deux formes :"),
  bullet("**Factory Method** : une fabrique possède une méthode de création qui reçoit les données nécessaires (par exemple une chaîne « A », « B », « C ») pour déterminer le type de l'objet à créer."),
  bullet("**Factory avec fabrique abstraite** : une classe de fabrique abstraite déclare la méthode de fabrique, et ce sont ses sous-classes concrètes qui créent les objets."),
  h2("2.1 Problème résolu"),
  rich("Dans la plupart des langages objet, la création d'objets se fait avec l'opérateur `new`. Son utilisation est « mauvaise » car elle crée un **couplage fort** entre l'appelant et la classe instanciée : une relation classe-à-classe est fragile. De plus, la classe passée à `new` ne peut pas être remplacée par une variable, il est donc difficile de paramétrer la création. Enfin, lorsque le client utilise une instruction conditionnelle pour choisir la classe, chaque changement dans la hiérarchie des classes à instancier demande des modifications dans le code du client."),
  rich("La solution est une relation **classe-à-interface** : le client ne connaît que la classe mère abstraite et délègue la création à une fabrique. Le couplage devient faible et le polymorphisme spécialise les traitements."),
  h2("2.2 Conditions d'utilisation"),
  bullet("Le client ne peut déterminer le type d'objet à créer qu'à l'**exécution**."),
  bullet("Il y a une volonté de **centraliser** la création d'objets."),
  bullet("L'objet à créer fait partie d'un ensemble de sous-classes et l'objet retourné est toujours du type de la classe mère."),

  h1("3. Modèle générique"),
  h2("3.1 Forme 1 : Factory Method"),
  rich("Structure générique (support, slide 17) : le **Client** utilise une **Fabrique** dont la méthode `methodeFabrique() : Produit` instancie un **ProduitConcret**, sous-classe de **Produit**."),
  ...table(["Participant", "Rôle"], [
    ["Produit", "Classe abstraite (ou interface) dont les sous-classes seront instanciées."],
    ["ProduitConcret", "Les sous-classes concrètes à instancier."],
    ["Fabrique", "Contient la méthode de fabrique ; elle reçoit les données nécessaires pour choisir la classe à instancier."],
    ["Client", "Programme qui fait appel à la fabrique pour obtenir des objets de type Produit."],
  ], [2300, 6772]),
  h2("3.2 Forme 2 : Factory avec fabrique abstraite"),
  rich("Structure générique (support, slide 24) : une **FabriqueAbstraite** abrite la signature de la méthode de fabrique et l'implémentation des méthodes qui l'invoquent ; une ou plusieurs **FabriqueConcrete** implémentent la méthode de fabrique et instancient le **ProduitConcret**."),
  ...figure("Cours/uml/factory_abstraite.png", "Modèle générique de la forme 2, reproduit avec DIA d'après la slide 24.", 1),
  ...table(["Participant", "Rôle"], [
    ["FabriqueAbstraite", "Classe abstraite : signature de la méthode de fabrique et méthodes qui l'invoquent."],
    ["FabriqueConcrete", "Classe concrète qui implémente la méthode de fabrique. Il peut y en avoir plusieurs."],
    ["Produit / ProduitConcret", "Classe abstraite et ses sous-classes concrètes à instancier."],
    ["Client", "Programme qui fait appel à la fabrique."],
  ], [2300, 6772]),
  h2("3.3 Différence avec Abstract Factory"),
  rich("Factory crée **un** produit d'une hiérarchie. Abstract Factory fournit une interface unique pour créer **une famille** d'objets liés (par exemple Scooter et Automobile, en version Essence ou Électrique) sans avoir à connaître les classes à instancier. Abstract Factory est un patron distinct, traité dans un autre dépôt."),

  h1("4. Exemple du cours"),
  rich("**Énoncé** : on gère trois types de produits dans un système. Le programme qui manipule ces produits ne connaît le type de produit à exécuter que lors de l'exécution. On utilise le patron Factory pour gérer cette situation, d'abord avec Factory Method (slides 18 à 23), puis avec une fabrique abstraite (slides 26 à 30)."),
  h2("4.1 Modélisation – Factory Method"),
  ...figure("Cours/uml/factory_method.png", "Diagramme de classes de l'exemple du cours, forme Factory Method (DIA, d'après la slide 19).", 2),
  rich("Remarque : le diagramme de la slide 19 présente `Produit` comme une interface alors que le code des slides 20 et 28 la déclare `abstract class`. Le rendu suit le code : `Produit` est une classe abstraite."),
  h2("4.2 Modélisation – fabrique abstraite"),
  rich("La hiérarchie des fabriques (slide 27) : `ProduitFactory` abstraite avec `getProduit()` qui appelle `createProduit()` abstraite ; `ProduitFactoryA`, `ProduitFactoryB` et `ProduitFactoryC` instancient respectivement `ProduitA`, `ProduitB` et `ProduitC`. Le modèle générique correspondant est la figure 1."),
  h2("4.3 Code source – Factory Method"),
  ...javaFiles("Cours/src/factorymethod", FM),
  h2("4.4 Code source – fabrique abstraite"),
  ...javaFiles("Cours/src/factoryabstraite", FA),
  h2("4.5 Résultat de l'exécution"),
  ...codeBlock(null, `............Methode 1: Factory Method............
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
produitC.methodeproduit()`),

  h1("5. Exemple modifié : système de notifications"),
  rich("**Énoncé** : une application doit prévenir un utilisateur par **e-mail**, **SMS** ou **notification push**. Le canal n'est connu qu'à l'exécution : il dépend de la préférence de l'utilisateur ou d'un argument de la ligne de commande. Le programme ne doit manipuler que la classe mère `Notification`. On utilise le patron Factory dans ses deux formes."),
  ...table(["Participant du modèle", "Exemple du cours", "Exemple modifié"], [
    ["Produit", "Produit, methodeproduit()", "Notification, envoyer(destinataire, message)"],
    ["ProduitConcret", "ProduitA, ProduitB, ProduitC", "EmailNotification, SMSNotification, PushNotification"],
    ["Fabrique (forme 1)", "FabriqueProduit.createProduit(type)", "NotificationFactory.creerNotification(canal)"],
    ["FabriqueAbstraite (forme 2)", "ProduitFactory : getProduit(), createProduit()", "NotificationFactory : notifier(), creerNotification()"],
    ["FabriqueConcrete (forme 2)", "ProduitFactoryA, B, C", "EmailNotificationFactory, SMSNotificationFactory, PushNotificationFactory"],
    ["Client", "Client.main", "Client.main (canal passé en argument)"],
  ], [2300, 3200, 3572]),
  h2("5.1 Modélisation – Factory Method"),
  ...figure("variantes/uml/notification_factory_method.png", "Variante Notifications, forme Factory Method (DIA).", 3),
  h2("5.2 Modélisation – fabrique abstraite"),
  ...figure("variantes/uml/notification_factory_abstraite.png", "Variante Notifications, forme fabrique abstraite (DIA).", 4),
  h2("5.3 Code source – Factory Method"),
  ...javaFiles("variantes/src/factorymethod", VM),
  h2("5.4 Code source – fabrique abstraite"),
  ...javaFiles("variantes/src/factoryabstraite", VA),
  h2("5.5 Résultat de l'exécution"),
  ...codeBlock(null, `............Variante 1 : Notifications (Factory Method)............
[EMAIL] A : etudiant@univ.cm
        Objet : Notification
        Corps : Votre devoir INF4067 a ete recu.
[SMS]   Vers etudiant@univ.cm : Votre devoir INF4067 a ete recu.
[PUSH]  Appareil etudiant@univ.cm -> "Votre devoir INF4067 a ete recu."
Erreur : Canal de notification inconnu : FAX

............Variante 2 : Notifications (fabrique abstraite)............
[EMAIL] A : etudiant@univ.cm : Votre devoir INF4067 a ete recu.
[SMS]   Vers etudiant@univ.cm : Votre devoir INF4067 a ete recu.
[PUSH]  Appareil etudiant@univ.cm : Votre devoir INF4067 a ete recu.`),

  h1("6. Analyse et justification"),
  rich("Le système de notifications remplit les deux conditions d'utilisation du patron Factory données en cours. Le type d'objet n'est connu qu'à l'exécution, puisque le canal dépend de l'utilisateur. La création est centralisée dans la fabrique : les règles propres à chaque canal (format d'un e-mail, troncature d'un SMS à 160 caractères) sont dans les classes concrètes, et le choix de la classe est dans la fabrique."),
  rich("Le client ne contient aucun `new EmailNotification()` : il manipule uniquement `Notification`. Remplacer un canal par un autre ou en ajouter un (WhatsApp, Telegram) n'impacte pas le client."),
  ...table(["Forme", "Avantage", "Limite"], [
    ["Factory Method", "Une seule fabrique, simple quand le choix dépend d'une valeur connue à l'exécution.", "Le `switch` doit être modifié à chaque nouveau produit."],
    ["Fabrique abstraite", "Ajouter un produit = ajouter une sous-classe de produit et une sous-classe de fabrique, sans modifier le code existant (principe ouvert/fermé).", "Davantage de classes."],
  ], [2000, 4272, 2800]),

  h1("7. Dépôt GitHub"),
  rich("Le code source complet (exemple du cours et exemple modifié), les diagrammes DIA avec leurs exports PNG, le script de compilation et l'analyse sont disponibles à l'adresse :"),
  p([run(REPO)], { alignment: AlignmentType.LEFT }),
  ...table(["Dossier", "Contenu"], [
    ["Cours/src/factorymethod", "Exemple du cours, forme Factory Method"],
    ["Cours/src/factoryabstraite", "Exemple du cours, forme fabrique abstraite"],
    ["Cours/uml", "factory_method.dia, factory_abstraite.dia et PNG"],
    ["variantes/src/factorymethod", "Variante Notifications, forme Factory Method"],
    ["variantes/src/factoryabstraite", "Variante Notifications, forme fabrique abstraite"],
    ["variantes/uml", "Diagrammes DIA et PNG de la variante"],
    ["documentation", "analyse.md, rapport, scripts de génération"],
    ["build.sh", "Compile et exécute les quatre programmes (JDK 17)"],
  ], [3200, 5872]),
  rich("Compilation et exécution :"),
  ...codeBlock(null, `javac -d out/cours $(find Cours/src -name '*.java')
java -cp out/cours factorymethod.Client
java -cp out/cours factoryabstraite.Client
javac -d out/variantes $(find variantes/src -name '*.java')
java -cp out/variantes factorymethod.Client SMS PUSH
java -cp out/variantes factoryabstraite.Client`),

  h1("8. Conclusion"),
  rich("Le patron Factory répond au problème du couplage fort introduit par l'opérateur `new`. Dans sa forme Factory Method, une fabrique unique choisit la classe à instancier d'après un paramètre reçu à l'exécution. Dans sa forme à fabrique abstraite, chaque fabrique concrète est responsable d'un produit, ce qui permet d'étendre le système sans modifier le code existant. L'exemple des notifications montre que le même modèle s'applique directement à un contexte réel, le client restant indépendant des classes concrètes."),
];

const footer = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [run("Page ", { size: 20 }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20, color: "000000" }), run(" / ", { size: 20 }), new TextRun({ children: [PageNumber.TOTAL_PAGES_IN_SECTION], font: FONT, size: 20, color: "000000" })],
  })],
});

const page = { size: { width: 11906, height: 16838 }, margin: { top: 1418, bottom: 1418, left: 1418, right: 1418 } };

const doc = new Document({
  creator: "GOYE AWOUMA CHAINE LEONEL",
  title: "Patron de construction Factory – Rapport d'étude",
  styles: {
    default: { document: { run: { font: FONT, size: 24, color: "000000" } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 32, bold: true, color: "000000" },
        paragraph: { spacing: { before: 360, after: 160 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 28, bold: true, color: "000000" },
        paragraph: { spacing: { before: 240, after: 120 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "puces", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [
    { properties: { page }, children: cover },
    { properties: { page: { ...page, pageNumbers: { start: 1 } } }, footers: { default: footer }, children: body },
  ],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log("docx ok", OUT); });

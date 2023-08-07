#QT_getty
Par Étienne Bérubé

_english will follow_

**Description**: QE_Snatch est un programme développé pour Quantume Energie par Étienne Bérubé. Le programme est utilisé pour aller chercher des données publique sur certains site-web.

**Utilisation**: Lors de sa première utilisation, le programme va générer 2 fichiers: db.json et config.yml

>Note: Il est important d'avoir toutes les dépendances avant de pouvoir exécuter le programme. Utilisez la commande: "pip install -r requierments.txt" pour installer toutes les dépendances manquantes

La configuration peut être rentrée manuellement ou lors de l'exécution du programme (avec la commande "init").

Le fichier de configuration utilise le format suivant:

auto-csv: < true | false > \
db.path: < location du fichier database (doit être au format json) >\
env: < dev | prod >\
items: <Item à chercher dans YellowPages> \
locations: < Locations où effectuer la recherche> \

Les items et locations doivent respecter un format bien précis. Les items doivent rester sur la même ligne. Voici un exemple d'items valide:
'''
items:
- Rona
- plusieurs mots
- une longue liste de mots
'''
>Note: Si un item contient plusieurs mots, ils seront cherché comme étant un ensemble et non un par un.

Pour les locations, ils doivent suivre le format suivant < Nom de la ville > < province >
>Note: il y a un espace entre le nom de la ville et la province.

Vous pouvez toujours utiliser la commande 'init' dans le programme pour avoir les étapes a suivre pour générer un fichier de configuration.

>Note: La base de donnée est contenue dans un seul fichier JSON. Il peut donc être transporté de machine en machine.

<br/>
<br/>

Pour commencer l'exécution du programme, il faut seulement utiliser la commande 'run'. Si le programme est configuré correctement, la recherche va s'enclencher. Cela peut prendre un certain temps.
>Note: s'il advenait que le programme crash. Un dossier _logs_ apparaîtra à la racine. Ce dossier contiendra les informations nécessaire pour comprendre l'erreur

Suite à l'exécution du programme, la database peut être exporté en CSV. Si l'option était choisie de généré un fichier CSV après chaque exécution, vous le retrouverez à la racine du programme. Si l'option était désactivée, vous pouvez utiliser la commande 'to-csv' pour générer le ficher.

Vous pouvez toujours utiliser la commande 'help' pour avoir accès à la liste de commande et leurs descriptions.
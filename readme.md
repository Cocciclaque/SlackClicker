## Slack Clicker

Slack Clicker est un jeu incrémental *invisible*, c'est à dire qu'il n'a aucune interface et est presque totalement obfusqué. <br>

Pour jouer, simplement lancer l'exécutable SC.exe

Si, une fois l'exécutable lancé, rien ne se passe, tout va bien ! Ouvrez l'explorateur de fichier et vérifiez si le titre de la fenêtre change et contient "SPS".
Si c'est le cas, le jeu est bel est bien lancé.

</hr>

## Gameplay

Pour fermer le jeu, appuyez sur F9 (configurable dans config.json). Si le nom de fenêtre est immobile, cela signifie que vous êtes bien sorti du jeu.

La barre de chargement indique le "cooldown" de vos effets passifs. Une fois la barre remplie, tout les passifs s'activent

### Commencer une partie

Pour commencer une partie, vous devez marquer des points manuellement. Pour cela, faites ctrl+maj+alt+m (ou f7), qui vous donnera 1 point.
Appuyer sur ceci à répétition non seulement donne des points, mais réduis également le cooldown de vos passifs.

### Consulter vos points

Pour consulter vos points, vous avez deux manières :
- 1ère manière, Recommandé : faire ctrl+maj+alt+z  (ou f5) fait apparaître une notification windows contenant vos points ainsi que vos SPS (Slacks per Slack)

- 2ème manière, plus visible : Ouvrir une application avec le titre de fenêtre de base de windows (explorateur de fichier, applications similaires, testez avec quoi ça fonctionne). Le titre sera modifié en temps réel pour contenir vos Slacks ainsi que la barre.

### Acheter des améliorations

Pour acheter des améliorations, rendez vous dans le dossier appdata/roaming/file updates/updates (le dossier updates est caché, il faut afficher les dossiers cachés)
Vous pouvez également vous y rendre en faisant win+r et en rentrant dans la barre appdata/roaming/file updates/updates.

Les améliorations sont des fichiers sous ce format : Nom numéro-d'achat - prix.txt
Vous pouvez consulter ce que fait une amélioration simplement en ouvrant le fichier (ou en ouvrant le fichier upgrades.json dans le dossier dependencies)
Pour acheter une amélioration, supprimez simplement le fichier txt. Si il ne réapparait pas, c'est soit :
- une amélioration unique
- un bug visuel, dans ce cas il suffit de raffraichir.

Il est grandement conseillé d'ouvrir les fichiers en question car ils peuvent contenir des indications à propos de leur utilisation. 

Appuyez sur maj (shift) pour en acheter 5 d'un coup.

### Consulter vos améliorations

Pour consulter vos améliorations, rendez vous sur votre bureau. Un dossier "._sys_watchdog" a été créé (accessible également depuis l'exploreur de fichier si vous ne le trouvez pas)
Dans le dossier réside un seul fichier, "watchdog_eventlog.txt". Dans ce fichier est une liste de tout les objets et améliorations que vous possédez.

Vous pouvez choisir le nom du dossier et du fichier dans config.json, dans le dossier dependencies, dans le dossier d'installation du jeu.

### Résumé

Pour résumer :
Barre de chargement mouvante = jeu qui tourne 
Barre de chargement immobile = jeu qui ne tourne pas 

ctrl maj alt m (ou f7) pour gagner des points manuellement 
ctrl maj alz z (ou f5)/explorateur de fichier pour visionner les points 

ces deux contrôles sont paramétrables dans le fichier dependencies/config.json

suppression des fichiers dans appdata/roaming/file updates/updates pour les améliorations 
consultation des améliorations sur le bureau/.sys_watchdog/watchdog_eventlist.txt

f9 pour fermer le jeu (vérifier que la barre de son s'arrête bien)


## Compiling

### Dépendances
L'application a besoin des imports pip 
```
pip install keyboard plyer pywin32
```
pour fonctionner.

### Compilation

Pour compiler le projet vous même (PyInstaller ou Auto-py-to-exe requis), lancez depuis le projet :
- pyinstaller --onefile --windowed --add-data "./dependencies/platforms;plyer/platforms" --name "SlackClicker" didi.py 

puis collez le dossier dependencies dans le nouveau dossier output créé. Le dossier dependencies devrait se trouver au même niveau que "SlackClicker.exe".

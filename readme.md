## Slack Clicker

Slack Clicker est un jeu incrémental *invisible*, c'est à dire qu'il n'a aucune interface et est presque totalement obfusqué. <br>

Pour jouer, simplement lancer l'exécutable SC.exe
Ce jeu nécessite que votre système windows soit mis en sourdine. La barre de son sera manipulée donc quelconque son jouant
oscillera beaucoup. Le son doit pouvoir monter et descendre sans risquer d'être entendu, il est donc grandement conseillé de mute votre PC.

Si, une fois l'exécutable lancé, rien ne se passe, tout va bien ! Vérifiez que votre barre de son s'incrémente toute seule.
Si c'est le cas, le jeu est bel est bien lancé.

</hr>

## Gameplay

Pour fermer le jeu, appuyez sur F9 (configurable dans config.json). Si la barre de son ne bouge plus, cela signifie que vous êtes bien sorti du jeu.

La barre de son indique le "cooldown" de vos effets passifs. Une fois la barre remplie, tout les passifs s'activent

### Commencer une partie

Pour commencer une partie, vous devez marquer des points manuellement. Pour cela, faites ctrl+maj+alt+m, qui vous donnera 1 point.
Appuyer sur ceci à répétition non seulement donne des points, mais réduis également le cooldown de vos passifs.

### Consulter vos points

Pour consulter vos points, vous avez deux manières :
- 1ère manière, Recommandé : faire ctrl+maj+alt+z fait apparaître une notification windows contenant vos points ainsi que vos SPS (Slacks per Slack)
Un Slack étant l'acte de la barre de son atteignant le maximum, mais un slack est aussi une unité de point que vous obtené. 10 points = 10 slacks.

- 2ème manière, pour les gens qui veulent jouer au jeu hors du travail ou avec plus de clarté (moins invisible) : 
Se rendre dans le dossier d'installation du jeu, aller dans dependencies et ouvrir save.json, ainsi que upgrades.json.
Attention ! NE PAS MODIFIER LES FICHIERS PENDANT QUE LE JEU TOURNE !! Cela peut avoir des conséquences imprévisibles, comme l'achat compulsif d'améliorations
ou parfois même la suppression totale de votre sauvegarde/progression.

### Acheter des améliorations

Pour acheter des améliorations, rendez vous dans le dossier appdata/roaming/file updates/updates (le dossier updates est caché, il faut afficher les dossiers cachés)
Vous pouvez également vous y rendre en faisant win+r et en rentrant dans la barre appdata/roaming/file updates/updates.

Les améliorations sont des fichiers sous ce format : Nom numéro-d'achat - prix.txt
Vous pouvez consulter ce que fait une amélioration simplement en ouvrant le fichier (ou en ouvrant le fichier upgrades.json dans le dossier dependencies)
Pour acheter une amélioration, supprimez simplement le fichier txt. Si il ne réapparait pas, c'est soit :
- une amélioration unique
- un bug visuel, dans ce cas il suffit de raffraichir.

Appuyez sur maj (shift) pour en acheter 5 d'un coup.

### Consulter vos améliorations

Pour consulter vos améliorations, rendez vous sur votre bureau. Un dossier "._sys_watchdog" a été créé (accessible également depuis l'exploreur de fichier si vous ne le trouvez pas)
Dans le dossier réside un seul fichier, "watchdog_eventlog.txt". Dans ce fichier est une liste de tout les objets et améliorations que vous possédez.

Vous pouvez choisir le nom du dossier et du fichier dans config.json, dans le dossier dependencies, dans le dossier d'installation du jeu.

### Résumé

Pour résumer :
Barre de son mouvante = jeu qui tourne 
Barre de son immobile = jeu qui ne tourne pas 

ctrl maj alt m pour gagner des points manuellement 
ctrl maj alz z pour visionner les points 

suppression des fichiers dans appdata/roaming/file updates/updates pour les améliorations 

f9 pour fermer le jeu (vérifier que la barre de son s'arrête bien)


## Compiling
Pour compiler le projet vous même (PyInstaller ou Auto-py-to-exe requis), lancez depuis le projet :
- pyinstaller --onefile --windowed --add-data "./dependencies/platforms;plyer/platforms" --name "SlackClicker" didi.py 

puis coller le dossier dependencies dans le nouveau dossier output créé. Le dossier dependencies devrait se trouver au même niveau que "SlackClicker.exe".
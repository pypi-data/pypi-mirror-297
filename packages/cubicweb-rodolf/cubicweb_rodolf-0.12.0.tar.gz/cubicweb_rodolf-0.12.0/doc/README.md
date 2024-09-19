# Documentation sur l'usage de Rodolf

Rodolf est une application pour configurer, gérer et suivre la production et la
publication de données RDF. L'objectif est de définir des sources de données,
la manière de les transformer et comment les publier dans un entrepôt Sparql
Virtuoso.

Cette documentation a pour objectif de présenter comment utiliser cet outil.

## Connexion

La première étape est la connexion. L'application n'est pas disponible pour les
utilisateurices non connecté·e·s. Il existe un compte d'administration
obligatoire qui peut être utilisé comme compte d'utilisateurice, mais il est
aussi possible de créer de nouveaux comptes dans la partie d'administration de
Rodolf (que nous présenterons dans un prochaine chapitre).

![Interface de connexion](images/login.png)

Cette page de connexion est tout à fait standard. Il est demandé de spécifier
le nom d'utilisateurice et le mot de passe pour se connecter. Le jeton
d'authentification est le même pour la partie d'administration, il n'est donc
pas nécessaire de se connecter aux deux endroits.

## Créer un projet

Une fois que vous êtes connecté·e·s, vous pouvez observer une page d'acceuil
sans projet, ni sources de données. Cette vue permet de lister tous les projets
et sources de données créés dans l'instance de Rodolf, mais après la première
connexion, il n'y a aucun projet ni sources de données.

![Acceuil sans données](images/index_noproject.png)

La vue affiche la liste des projet en haut et la liste des sources de données
en bas. Vous pouvez ajouter un projet avec le bouton "ajouter" sur la même
ligne que le titre "Projets".

![Créer un projet](images/create_project.png)

Le formulaire de création d'un projet permet de spécifier son nom, et un bouton
permet de définir si le le projet est actif ou non. Ensuite il est demandé de
spécifier les paramètres de connexion au Virtuoso : l'URL du Virtuoso, le nom
d'utilisateur du compte d'administration sur le Virtuoso et son mot de passe.
Ensuite vous pouvez ajouter un fichier contenant l'ontologie et un contenant
les règles SHACL pour la validation des données.

![Le projet est créé](images/project_empty.png)

## Créer une source de données

Une fois le projet créé, vous devez créer une source de données. Cette entité
est utilisée pour définir le lien où récupérer les données. Pour ce faire, sur
la page d'acceuil, cliquez sur le bouton "ajouter" sur la même ligne que le
titre "sources de données".

![Ajouter une source de données](images/add_dataservice.png)

Sur cette vue vous pouvez spécifier les informations concernant la source de
données. Tout d'abord, le nom de la source de données qui sera utilisé dans
l'interface utilisateurice de Rodolf. Ensuite, vous pouvez spécifier le lien à
utiliser pour récupérer les données. Si vous ne disposez pas d'une URL, mais du
fichier directement, vous pouvez l'envoyer sur le serveur avec le bouton "A
partir d'un fichier". Vous spécifiez le format des données pour indiquer
comment interpréter les données, ainsi que la fréquence de mise à jour, qui
déterminera la fréquence de récupération de la source de données dans le ou les
projet(s) qui utilisent cette source. Enfin une description de cette source.

## Ajouter une recette pour lier une source de données à un projet

Une fois que vous avez créé l'ensemble des sources de données que vous
souhaitez utiliser, vous pouvez les lier à un projet. C'est nécessaire pour
définir quelles sources de données exposer dans l'entrepôt Virtuoso du projet.

Pour cela, vous devez créer des recettes. Ces recettes peuvent être créées dans
l'interface de visualisation d'un projet. Le bouton "ajouter" sur la même ligne
que le titre "Recettes" permet d'ouvrir une fenêtre pour la création d'une
recette. Tout d'abord, il faut définir le nom de la recette qui sera utilisé
dans l'interface de Rodolf. Ensuite il faut spécifier la source de données,
préalablement créée, à utiliser dans cette recette. L'identifiant (URI ou URN)
du graphe nommé dans lequel déposer les triplets générés et enfin le processus
à appliquer sur les données.

Le processus à appliquer est une fonction qui sera utilisée, juste après la
récupération des données. Cette fonction peut effectuer différentes opérations.
Le processus par défaut, récupère les données, les interprète suivant le format
des données défini dans la source de données, valide les données en utilisant
les règles SHACL du projet, pour ensuite les envoyer dans l'entrepôt Virtuoso
dans le graphe nommé spécifié dans la recette. Une version "de test" permet
d'effectuer ces mêmes opérations, sans la mise à jour des données dans
l'entrepôt.

Chaque recette permet d'envoyer les données provenant d'une source de données
dans un graphe nommé sur l'entrepôt Virtuoso. Elle permet de gérer spécifier
les données à envoyer et comment les manipuler. Chaque mise à jour des données
supprime tous les triplets du graphe nommé et renvoyer l'intégralité des
données. L'utilisation d'un graphe nommé permet aussi de n'effectuer que des
requêtes sur les données provenant de cette source spécifiquement. Il est alors
possible d'effectuer des requêtes sur l'intégralité des graphes nommées du
Virtuoso ou sur un sous ensemble qui nous interesse.

![Recette de données](images/recipe_data.png)

Une fois la recette créée, une carte apparait sur la page du projet. Cette
carte affiche les infromations principales à propos de la recette. Le nom, le
processus appliqué, le graphe nommé utilisé et l'état de la dernière tâche
d'éxécution.

## Historique des tâches d'import

En bas de la page d'un projet vous pouvez observer l'historique des tâches
d'import. Si vous cliquez sur l'accordéon, la liste de l'historique des tâches
d'import sera récupérée. Cette liste est paginée comme il peut y en avoir
beaucoup.

![Tâches d'import](images/import_processes.png)

Chaque ligne représente une tâche d'import sur le projet concerné. En plus de
l'identifiant de la tâche, est affiché la data et l'heure d'éxécution, la
recette utilisée, l'état de la tâche (pour savoir elle a réussie ou non) et les
fichiers générés. Vous pouvez télécharger les données d'entrées (les données
récupérées de l'URL de la source de données), les données générées (résultat du
processus appliqué par la recette qui peut modifier les données), le journal
d'éxécution pour suivre ce qu'il s'est passé durant la tâche, ainsi que le
rapport de validation SHACL.

## Interface d'administration

Si vous lancez le projet en local, l'interface d'administration est accessible
sur le port 8080. Cette interface utilise les vues par défaut du cadriciel
[CubicWeb](https://cubicweb.org). Cette interface permet d'accéder directement
aux entités et de modifier toutes les données. Elle est notamment utile pour
ajouter/modifier des comptes utilisateurices.

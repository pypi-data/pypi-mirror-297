# Rodolf usage documentation

Rodolf is an application to configure, manage and follow RDF data production.
The idea is to define data sources, way to transform them, and how to publish
them into a Virtuoso Sparql endpoint.

This documentaiton aims to present how to do it and explain the usages.

## Login

The first step is to login. This application is not available for non logged
users. Then this is necessary to login. There is a mandatory admin account
which can be used as user accont, but there is possibility to create new user
account into the backoffice application (which we will present into next
chapter).

![Login view](images/login.png)

This login page is a standard one. You specify user and password then you log
in. The login token is shared with backoffice and front rodolf application.
This means once you are logged in into on of the front or backoffice then you
are logged in both.

## Create Projet

Once you are logged in, then you can see an empty index view. This view is
supposed to render projects and dataservices, but after the first login there
is no project nor dataservices to render.

![Index with no data](images/index_noproject.png)

This view renders projects at the top of it, and dataservices in the bottom.
You can add a project with the "ajouter" button on the same line as the title
"Projet".

![Create project](images/create_project.png)

The create project form contains the name and a toggle to know if the project
is active. Then we can define the Virtuoso parameters : the virtuoso URL, the
admin username and the password. Then you can upload a file to specify which
ontology to use and the SHACL shapes to validate the data.

![Project created](images/project_empty.png)

## Create a DataService

Once the project is created, you need to create a DataService. This entity is
used to define where to reach the data. To do so, in the index view, create on
the button "ajouter" on the same line as the title "Sources de données".

![Add a dataservice](images/add_dataservice.png)

In this view you can define the DataService parameters. The first one is the
name you want to use into the rodolf UI. Then you can define how to reach the
dataservice file. You can define it with an URL, which leads to the datafile
directly, or by uploading a file thought the interface, which auto fills the
data URL input. Then you define the mimetype to use, to help Rodolf to know how
to parse the file. The frequency to update the file and a description to
explain what is stored.

## Add a recipe to link dataservice to project

Once you have created all the dataservices you want to use, you can link them
to the project. This is mandatory to define which data to expose into a
dedicated Virtuoso server.

To do so, you need to create recipes. This can be done in the project view,
using the button "Ajouter" in the "Recette" line. This button opens a modal,
which contains the form to create a new recipe. First you have to define the
name of the recipe to identify it in the Rodolf UI. Then the dataservice to
use, to define how to fetch data, the graph URI in which the output dataset
will be stored in the Virtuoso server and finally the process type to apply.

The process type is the function which will be used just after fetching the
data. This function can do several operations. The default one, fetchs the
data, parses it from the mimetype defined in the dataservice, validates the
data using SHACL rules from the project, then uploads the data to the virtuoso
server. A dry run version is defined, which is exactly identical except there
is no data uploaded in the Virtuoso server.

Each recipe uploads the data into a dedicated named graph in the Virtuoso
server. This is useful to manage the data. To replace all the data from a
dedicated recipe we can erase all triples from this named graph, and reupload
them. This is why we need to define a unique graph URI for each recipe to a
specific project. This named graph approach is convenient to query the data.
You can query only some graphs to not query all the Virtuoso server if you
don't want to.

![Recipe data](images/recipe_data.png)

Once the recipe is created, then a card appears in the project page. This card
shows the principal informations about this recipe. The name, the process type
used, the graph URI where the data are published, and the state of the last
import execution.

## Import process historic

At the bottom of the project page you can show the import process historic.
If you click to open the accordion, then the import processes are fetched.
Since it can be a lot of them, these import processes are paginated.

![import processes](images/import_processes.png)

Each line represents one import process which has occure for this project. You
can see the date and hour when the import process has occured, the recipe used
the state (to know if something went wrong) and the generated files. You can
download the input dataset (data juste fetched from the DataService data URL),
the ouput dataset (data generated after the process type execution, which can
change some data or format), the log to know what happended during the import
process execution and the SHACL validation report if some shapes are not
validated.

## Backoffice interface

If you run this project locally, the backoffice interface can be reached
thought the port 8080. This interface uses the default views from the
[CubicWeb](https://cubicweb.org) framework. You can access to all entities
directly to show and modify everything. This interface can be used to create
new user accounts.

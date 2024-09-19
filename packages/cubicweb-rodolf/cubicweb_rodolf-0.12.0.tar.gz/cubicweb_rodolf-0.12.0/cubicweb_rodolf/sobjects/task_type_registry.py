import io
import logging
import os

import requests
import yaml

from cubicweb.appobject import AppObject

from cubicweb_rodolf.schema import TaskProcess

DATA_GOUV_API_KEY = os.getenv("DATA_GOUV_API_KEY", "")
DATA_GOUV_API_BASE_URL = os.getenv(
    "DATA_GOUV_API_URL", "https://demo.data.gouv.fr/api/1/"
)

DATA_GOUV_API_HEADERS = {
    "X-Api-Key": DATA_GOUV_API_KEY,
    "Content-Type": "application/json",
}


def publish_file_to_datagouv(log, dataset_id, resource_id, content, content_format):
    resp = requests.get(
        f"{DATA_GOUV_API_BASE_URL}"
        f"/datasets/{dataset_id}"
        f"/resources/{resource_id}",
        headers=DATA_GOUV_API_HEADERS,
    )
    if not resp.ok:
        log.error(f"Dataset and resource must exist : {resp.json()}")
        resp.raise_for_status()
    resource = resp.json()
    resource_title = resource["title"]
    resp = requests.post(
        f"{DATA_GOUV_API_BASE_URL}"
        f"/datasets/{dataset_id}"
        f"/resources/{resource_id}"
        "/upload",
        files={
            "file": (
                f"rodolf.{content_format}",
                io.StringIO(content),
                content_format,
            ),
        },
        headers={
            "X-Api-Key": DATA_GOUV_API_KEY,
        },
    )
    if not resp.ok:
        log.error(f"DATA Gouv API failed : {resp.json()}")
        resp.raise_for_status()

    #  reset resource title since filename changes this attribute
    resp = requests.put(
        f"{DATA_GOUV_API_BASE_URL}"
        f"datasets/{dataset_id}"
        f"/resources/{resource_id}/",
        json={"title": resource_title},
        headers={**DATA_GOUV_API_HEADERS, "Accept": "application/json"},
    )
    resp.raise_for_status()
    log.info("Resource uploaded successfully")


class PublishDataGouvTask(AppObject):
    """
    This Task expects a YAML file as parameter.
    This YAML must be formated as following:
    ```yaml
        dataset: 668c10ef1914f7b4210a7f13
        resource: 695249e9-6519-4015-b5f9-a13f58a9e9c7
        format: ttl
    ```
    format is not mandatory, "ttl" is used by default
    """

    __registry__ = "rodolf.appobject.tasktype"
    __regid__ = "data-gouv-publisher-all"
    __name__ = "Publier toutes les données sur data.gouv.fr"

    def __call__(self, task_process: TaskProcess, log: logging.Logger) -> str:
        log.info("Initialize task to publish on data.gouv.fr")
        procedure = task_process.import_procedure[0]
        project_task = task_process.project_task[0]
        graphs = procedure.published_graphs

        if not project_task.parameters:
            log.error("This task needs a SPARQL query as parameter")
            raise ValueError("This task needs a SPARQL query as parameter")
        try:
            config = yaml.safe_load(project_task.parameters[0])
        except Exception:
            log.error("Seems like YAML parameters is not well formated")
            raise ValueError

        if "dataset" not in config or "resource" not in config:
            log.error("The YAML config must contain 'dataset', 'resource' entries")
            raise ValueError

        content_format = config.get("format", "ttl")
        dataset_id = config.get("dataset")
        resource_id = config.get("resource")
        content = graphs.serialize(format=content_format)

        publish_file_to_datagouv(log, dataset_id, resource_id, content, content_format)

        return content


class PublishDataGouvFromSPARQLTask(AppObject):
    """
    This Task expects a YAML file as parameter.
    This YAML must be formated as following:
    ```yaml
        dataset: 668c10ef1914f7b4210a7f13
        resource: 695249e9-6519-4015-b5f9-a13f58a9e9c7
        format: ttl
        sparql: >
          CONSTRUCT { ?a ?b ?c }
          WHERE { ?a ?b ?c}
          LIMIT 100
    ```
    format is not mandatory, "ttl" is used by default
    """

    __registry__ = "rodolf.appobject.tasktype"
    __regid__ = "data-gouv-publisher-sparql"
    __name__ = "Publier le résultat d'une requêtes SPARQL sur data.gouv.fr"

    def __call__(self, task_process: TaskProcess, log: logging.Logger) -> str:
        log.info("Initialize task to publish sparql result on data.gouv.fr")
        procedure = task_process.import_procedure[0]
        project_task = task_process.project_task[0]

        if not project_task.parameters:
            log.error("This task needs a SPARQL query as parameter")
            raise ValueError("This task needs a SPARQL query as parameter")
        try:
            config = yaml.safe_load(project_task.parameters[0])
        except Exception:
            log.error("Seems like YAML parameters is not well formated")
            raise ValueError

        if (
            "sparql" not in config
            or "dataset" not in config
            or "resource" not in config
        ):
            log.error(
                "The YAML config must contains 'dataset', 'resource' and"
                " 'sparql' entries"
            )
            raise ValueError

        sparql_query = config.get("sparql")
        content_format = config.get("format", "ttl")
        dataset_id = config.get("dataset")
        resource_id = config.get("resource")

        log.info(f"SPARQL query to execute {sparql_query}")

        resp = requests.post(
            procedure.sparql_url + "/sparql",
            data={
                "query": sparql_query,
                "format": content_format,
            },
        )
        resp.raise_for_status()
        log.info(f"SPARQL query answer has been fetched from {procedure.sparql_url}")
        content = resp.text

        publish_file_to_datagouv(log, dataset_id, resource_id, content, content_format)

        return content

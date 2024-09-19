import os
import json
import logging
import time
from rdflib import Graph
import requests

from cubicweb.appobject import AppObject

from cubicweb_rodolf.process_helpers import (
    get_graph_from_dataservice,
    rdfs_closure,
    upload_graph_to_virtuoso_endpoint,
)
from cubicweb_rodolf.schema import ImportProcess


def get_file_content_from_dataservice(dataservice, log):
    if dataservice.data_file:
        return dataservice.data_file[0].read()
    else:
        response = requests.get(
            dataservice.data_url,
            allow_redirects=True,
            timeout=4,
        )
        if not response.ok:
            log.error(
                f"Cannot get file {dataservice.data_url}:"
                f" {response.status_code} {response.text}"
            )
            response.raise_for_status()
        return response.content


class DefaultProcessType(AppObject):
    __registry__ = "rodolf.appobject.processtype"
    __regid__ = "default"
    __uiname__ = "Processus d'import standard"

    def __call__(self, import_process: ImportProcess, log: logging.Logger) -> Graph:
        log.info("Applying the default processtype")
        import_recipe = import_process.import_recipe[0]
        import_procedure = import_process.import_procedure[0]
        dataservice = import_recipe.dataservice[0]
        graph = get_graph_from_dataservice(dataservice, log)
        log.info(f"Data was successfully downloaded from {dataservice.dc_title()}")
        dataset_file = import_process.update_dataset(graph)
        log.info(
            "Output dataset has been set for ImportProcess" f" #{import_process.eid}"
        )
        upload_graph_to_virtuoso_endpoint(
            import_procedure,
            graph,
            import_recipe.graph_uri,
            dataset_file.data_name,
        )
        log.info(
            f"Data for DataService {dataservice.dc_title()} has been well"
            f" uploaded to virtuoso {import_procedure.virtuoso_url}"
        )
        return graph


class DefaultDryRunProcessType(AppObject):
    __registry__ = "rodolf.appobject.processtype"
    __regid__ = "default-dryrun"
    __uiname__ = "Process d'import standard sans publication"

    def __call__(self, import_process: ImportProcess, log: logging.Logger) -> Graph:
        log.info("Applying the default-dryrun processtype")
        import_recipe = import_process.import_recipe[0]
        dataservice = import_recipe.dataservice[0]
        graph = get_graph_from_dataservice(dataservice, log)
        log.info(f"Data was successfully downloaded from {dataservice.dc_title()}")
        import_process.update_dataset(graph)
        log.info(
            "Output dataset has been set for ImportProcess" f" #{import_process.eid}"
        )
        return graph


class DefaultWithClosureProcessType(AppObject):
    __registry__ = "rodolf.appobject.processtype"
    __regid__ = "default_with_closure"
    __uiname__ = "Processus d'import standard avec calcul des inférences"

    def __call__(self, import_process: ImportProcess, log: logging.Logger) -> Graph:
        log.info("Applying the default processtype with closure")
        import_recipe = import_process.import_recipe[0]
        import_procedure = import_process.import_procedure[0]
        dataservice = import_recipe.dataservice[0]
        graph = get_graph_from_dataservice(dataservice, log)
        log.info(f"Data was successfully downloaded from {dataservice.dc_title()}")

        log.info("Computing closure ...")
        previous_len = len(graph)
        ontology_graph = Graph()
        ontology_graph.parse(data=import_procedure.ontology_file[0].data.read())
        closed_graph = rdfs_closure(graph, ontology_graph)
        log.info(
            f"Closed graph computed ({len(closed_graph) - previous_len} triples added)"
        )

        dataset_file = import_process.update_dataset(closed_graph)
        log.info(
            "Output dataset has been set for ImportProcess" f" #{import_process.eid}"
        )
        upload_graph_to_virtuoso_endpoint(
            import_procedure,
            closed_graph,
            import_recipe.graph_uri,
            dataset_file.data_name,
        )
        log.info(
            f"Data for DataService {dataservice.dc_title()} has been well"
            f" uploaded to virtuoso {import_procedure.virtuoso_url}"
        )
        return graph


class OpenRefineProcessType(AppObject):
    __registry__ = "rodolf.appobject.processtype"
    __regid__ = "openrefine"
    __uiname__ = "Processus d'import en utilisant OpenRefine"

    def __call__(self, import_process: ImportProcess, log: logging.Logger) -> Graph:
        import_recipe = import_process.import_recipe[0]
        import_procedure = import_process.import_procedure[0]
        dataservice = import_recipe.dataservice[0]
        if not import_recipe.parameters:
            log.error(
                "OpenRefine processtype must be applied to a recipe with parameters"
            )

        openrefine_url = os.getenv("OPENREFINE_URL", "http://localhost:3333")
        log.info(f"Use the openrefine instance {openrefine_url}")

        get_csrf_token_resp = requests.get(
            openrefine_url + "/command/core/get-csrf-token"
        )
        csrf_token = get_csrf_token_resp.json()["token"]

        log.info("Launch import job in OpenRefine ...")
        importing_job_req = requests.post(
            openrefine_url
            + "/command/core/create-importing-job?csrf_token="
            + csrf_token
        )
        job_id = importing_job_req.json()["jobID"]
        log.info(f"Job ID on open refine is : {job_id}")

        log.info("Uploading file in OpenRefine job")
        files = {"upload": dataservice.data_file[0]}
        requests.post(
            openrefine_url + "/command/core/importing-controller"
            "?controller=core%2Fdefault-importing-controller"
            f"&jobID={job_id}&subCommand=load-raw-data"
            f"&csrf_token={csrf_token}",
            files=files,
        )

        parse_format = None
        while True:
            importing_status_req = requests.post(
                openrefine_url
                + f"/command/core/get-importing-job-status?jobID={job_id}"
            )
            resp = importing_status_req.json()
            if resp["code"] != "ok":
                time.sleep(2)
                continue
            parse_format = importing_status_req.json()["job"]["config"][
                "rankedFormats"
            ][0]
            break
        log.info(f"Mimetype discovered : {parse_format}")

        get_parser_param_req = requests.post(
            openrefine_url + "/command/core/importing-controller"
            "?controller=core%2Fdefault-importing-controller"
            f"&jobID={job_id}"
            "&subCommand=initialize-parser-ui"
            f"&format={parse_format}"
            f"&csrf_token={csrf_token}"
        )
        resp = get_parser_param_req.json()
        if resp["status"] == "error":
            log.error("OpenRefine Error : " + resp["message"])
            raise ValueError
        parser_params = get_parser_param_req.json()["options"]

        params = {
            "format": parse_format,
            "options": json.dumps(
                {
                    **parser_params,
                    "projectName": f"Rodolf Import : {import_procedure.eid} -- {dataservice.name}",
                    "projectTags": ["rodolf"],
                    "sheets": parser_params.get("sheetRecords"),
                }
            ),
        }
        log.info("Creating project ...")
        create_project_req = requests.post(
            openrefine_url + "/command/core/importing-controller"
            "?controller=core%2Fdefault-importing-controller"
            f"&jobID={job_id}"
            "&subCommand=create-project"
            f"&csrf_token={csrf_token}",
            data=params,
        )

        resp = create_project_req.json()
        if resp["status"] == "error":
            log.error("Error OpenRefine : " + resp["error"])
            raise ValueError(resp["error"])

        project_id = None
        while True:
            get_project_metadata_req = requests.post(
                openrefine_url
                + f"/command/core/get-importing-job-status?jobID={job_id}"
            )
            resp = get_project_metadata_req.json()
            if resp["job"]["config"]["state"] != "created-project":
                time.sleep(2)
                continue
            project_id = get_project_metadata_req.json()["job"]["config"]["projectID"]
            break
        log.info(f"Project created ID : {project_id}")

        recipe_operations = json.loads(import_recipe.parameters[0].data.read())
        log.info("Applying operations on project ...")
        requests.post(
            openrefine_url + "/command/core/apply-operations" f"?project={project_id}",
            data={
                "operations": json.dumps(recipe_operations),
                "csrf_token": csrf_token,
            },
        )

        log.info("Exporting rows in turtle format ...")
        export_rows_req = requests.post(
            openrefine_url
            + f"/command/core/export-rows?project={project_id}&format=Turtle"
        )

        g = Graph()
        g.parse(data=export_rows_req.content, format="ttl")
        log.info(f"Rows exported ({len(g)} triples fetched)")
        dataset_file = import_process.update_dataset(g)
        log.info(
            "Output dataset has been set for ImportProcess" f" #{import_process.eid}"
        )
        log.info("Deleting project...")
        requests.post(
            openrefine_url + f"/command/core/delete-project?project={project_id}"
        )
        log.info(f"Uploading graph into virtuoso (graph {import_recipe.graph_uri})")
        upload_graph_to_virtuoso_endpoint(
            import_procedure,
            g,
            import_recipe.graph_uri,
            dataset_file.data_name,
        )
        log.info(
            f"Data for DataService {dataservice.dc_title()} has been well"
            f" uploaded to virtuoso {import_procedure.virtuoso_url}"
        )
        return g

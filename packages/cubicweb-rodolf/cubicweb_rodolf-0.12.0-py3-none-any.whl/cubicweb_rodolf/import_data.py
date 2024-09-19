# -*- coding: utf-8 -*-
# copyright 2023 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import io
import logging
import pyshacl
import json

from cubicweb import Binary
from cubicweb_rq.rq import rqjob
from rdflib import Graph, URIRef
from rdflib.namespace import NamespaceManager


def summarize_validation_report(shacl_report_graph):
    summary_query = """
PREFIX sh: <http://www.w3.org/ns/shacl#>
select distinct ?property ?inverseProperty ?severity
?constraint ?shape ?message
(count(?x) as ?shcount)
(sample(?fmessage) as ?message)
(group_concat(?fnode; separator="|") as ?nodes)
(group_concat(?shvalue; separator="|") as ?shvalues)
where{
  ?x a sh:ValidationResult.
  ?x sh:resultPath ?property.
  ?x sh:resultSeverity ?severity.
  ?x sh:sourceShape ?shape.
  ?x sh:resultMessage ?fmessage.
  ?x sh:focusNode ?fnode.
  OPTIONAL{?x sh:sourceConstraintComponent ?constraint.}
  OPTIONAL{?property sh:inversePath ?inverseProperty}
  OPTIONAL{?x sh:value ?shvalue}
}
GROUP BY ?property ?severity ?shape ?inverseProperty ?constraint
    """
    qres = shacl_report_graph.query(summary_query)
    summary_report = []
    g = Graph()
    nm = NamespaceManager(g, bind_namespaces="rdflib")
    nb_violations = 0
    for row in qres:
        nb_violations += int(row.shcount)
        shproperty = None
        if isinstance(row.property, URIRef):
            shproperty = row.property.n3(nm)
        elif isinstance(row.inverseProperty, URIRef):
            shproperty = f"^{row.inverseProperty.n3(nm)}"

        summary_report.append(
            {
                "severity": row.severity.n3(nm),
                "count": int(row.shcount),
                "message": row.message,
                "constraint": row.constraint.n3(nm),
                "property": shproperty,
                "shape": row.shape.n3(nm) if isinstance(row.shape, URIRef) else None,
                "cases": {
                    "nodes": row.nodes.split("|")[:10],
                    "values": row.shvalues.split("|")[:10],
                },
            }
        )

    return nb_violations, summary_report


def check_rdf_graph(graph, import_procedure):
    errors = (None, None)
    everything_ok = True
    if import_procedure.shacl_file:
        shacl_file = import_procedure.shacl_file[0]
        shacl_shapes_graph = Graph().parse(
            data=shacl_file.data.getvalue().decode("utf8"),
            format=shacl_file.data_format,
        )
        conforms, graph_reports, text_reports = pyshacl.validate(
            graph,
            shacl_graph=shacl_shapes_graph,
        )
        if not conforms:
            nb_violations, json_summary = summarize_validation_report(graph_reports)
            everything_ok = False
            errors = (nb_violations, json_summary)
    return everything_ok, errors


def get_process_logger(stream_file):
    log = logging.getLogger("rq.task")
    handler = logging.StreamHandler(stream_file)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)s\n\n"
            "%(message)s\n\n"
            "--------\n"
        )
    )
    log.addHandler(handler)
    return log


@rqjob
def execute_task(
    cnx,
    task_process_eid: int,
):
    """Execute Task.

    :param Connection cnx: database connection
    :param int task_process_eid: TaskProcess eid

    """
    task_failed = False
    formatted_exc = None
    stream_log_file = io.StringIO()
    log = get_process_logger(stream_log_file)

    task_process = cnx.entity_from_eid(task_process_eid)
    wf = task_process.cw_adapt_to("IWorkflowable")
    project_task = task_process.project_task[0]
    import_procedure = task_process.import_procedure[0]
    try:
        wf.fire_transition("starts")
        cnx.commit()

        log.info(
            "Starting task process with project task"
            f" {project_task.dc_title()} on {import_procedure.dc_title()}"
        )
        process_to_apply = cnx.vreg["rodolf.appobject.tasktype"].select(
            project_task.use_task[0].regid, req=cnx
        )
        output = process_to_apply(task_process, log)
        task_process.cw_set(
            has_output_dataset=cnx.create_entity(
                "File",
                title=f"Task outputdataset for TaskProcess#{task_process_eid}",
                data=Binary(output.encode("utf8")),
                data_name=f"output_data_TaskProcess_{task_process_eid}.txt",
            )
        )
    except Exception as error:
        task_failed = True
        log.error(error, exc_info=True)
        log.error("Executing task aborted.")
        wf.fire_transition("fails", formatted_exc)
    else:
        log.info(f"Task type {process_to_apply} has been well applied")
        wf.fire_transition("success")

    stream_log_file.seek(0)
    task_process.cw_set(
        log_file=cnx.create_entity(
            "File",
            title=f"Log file for TaskProcess#{task_process_eid}",
            data=Binary(stream_log_file.read().encode("utf8")),
            data_name=f"log_TaskProcess_{task_process_eid}.txt",
            data_format="plain/text",
        )
    )
    cnx.commit()

    return not task_failed


@rqjob
def import_data(
    cnx,
    import_process_eid: int,
):
    """Import data.

    :param Connection cnx: database connection
    :param int import_process_eid: ImportProcess eid

    """
    task_failed = False
    formatted_exc = None
    stream_log_file = io.StringIO()
    log = get_process_logger(stream_log_file)

    import_process = cnx.entity_from_eid(import_process_eid)
    wf = import_process.cw_adapt_to("IWorkflowable")
    import_recipe = import_process.import_recipe[0]
    dataservice = import_recipe.dataservice[0]
    import_procedure = import_process.import_procedure[0]
    rdf_graph = None
    try:
        wf.fire_transition("starts")
        cnx.commit()

        log.info(
            "Starting import process with recipe"
            f" {import_recipe.dc_title()} from {dataservice.dc_title()} to"
            f" populate {import_procedure.dc_title()}"
        )
        process_to_apply = cnx.vreg["rodolf.appobject.processtype"].select(
            import_recipe.use_process[0].regid, req=cnx
        )
        rdf_graph = process_to_apply(import_process, log)
        import_process.cw_set(
            has_input_dataset=cnx.create_entity(
                "File",
                title=f"Input dataset for ImportProcess#{import_process_eid}",
                data=Binary(rdf_graph.serialize(format="ttl").encode("utf8")),
                data_name=f"input_data_ImportProcess_{import_process.eid}.ttl",
                data_format="text/turtle",
            )
        )
    except Exception as error:
        task_failed = True
        log.error(error, exc_info=True)
        log.error("Importing data aborted.")
        wf.fire_transition("fails", formatted_exc)
    else:
        log.info(
            f"Process type {process_to_apply} has been well applied for"
            f" dataservice {dataservice.dc_title()}"
        )
        wf.fire_transition("success")

    if rdf_graph is not None:
        log.info("Starting SHACL validation")
        valid_rdf, shacl_errors = check_rdf_graph(rdf_graph, import_procedure)
        if not valid_rdf:
            stream_shacl_log = io.StringIO()
            shacl_log = get_process_logger(stream_shacl_log)
            shacl_log.propagate = False  # do not log into stdout
            log.error("Data contains errors, see SHACL report")
            shacl_file = import_procedure.shacl_file[0]
            (nb_violations, json_report) = shacl_errors
            shacl_log.error(
                f"Data from {dataservice.dc_title()} does not comply with"
                f" SHACL file {shacl_file.dc_title()} and raises"
                f" {nb_violations} violations.\nSee details in SHACL Log"
            )
            stream_shacl_log.seek(0)
            import_process.cw_set(
                shacl_report=cnx.create_entity(
                    "File",
                    title=f"SHACL Log file for ImportProcess#{import_process_eid}",
                    data=Binary(json.dumps(json_report).encode("utf-8")),
                    data_name=f"log_SHACL_ImportProcess_{import_process.eid}.json",
                    data_format="application/json",
                )
            )
            import_process.cw_set(shacl_valid=False)
        else:
            import_process.cw_set(shacl_valid=True)
            log.info("Data was successfully validated")
    stream_log_file.seek(0)
    import_process.cw_set(
        import_report=cnx.create_entity(
            "File",
            title=f"Log file for ImportProcess#{import_process_eid}",
            data=Binary(stream_log_file.read().encode("utf8")),
            data_name=f"log_ImportProcess_{import_process.eid}.txt",
            data_format="plain/text",
        )
    )
    cnx.commit()

    return not task_failed


def launch_import_procedure(cnx, procedure, logger, only_delta_import=True):
    """
    procedure: ImportProcedure Entity
    logger: Logger
    only_delta_import: boolean
        - if set to False, every ImportRecipe of the ImportProcedure will have
            ImportProcess created and an associated RqTask launched
        - if set to True (default), only the ImportRecipe i) whose latest ImportProcess failed
            ii) or whose dataservice's refresh period has been over, iii) or which have
            never been launched will be launched (i.e. ImportProcess + RqTask created and enqueued)
    """
    if not procedure.activated:
        return 0
    return procedure.create_needed_import_process(only_delta_import, logger)

import requests
import logging

from rdflib import Graph, ConjunctiveGraph

from rdf_data_manager import delete_graph, upload_graph
from cubicweb_file.schema import File

from cubicweb_rodolf.schema import DataService, ImportProcedure


UPLOAD_MAX = 3
UPLOAD_DELAY = 10


def get_graph_from_url(
    download_url: str, content_type: str, log: logging.Logger
) -> Graph:
    response = requests.get(
        download_url,
        allow_redirects=True,
        timeout=4,
    )
    if not response.ok:
        log.error(
            f"Cannot get file {download_url}:"
            f" {response.status_code} {response.text}"
        )
        response.raise_for_status()

    graph = ConjunctiveGraph()
    graph.parse(data=response.text, format=content_type)
    return graph


def get_graph_from_file(file: File, content_type: str, log: logging.Logger) -> Graph:
    graph = ConjunctiveGraph()
    graph.parse(data=file.data, format=content_type)
    return graph


def get_graph_from_dataservice(dataservice: DataService, log: logging.Logger) -> Graph:
    if dataservice.data_file:
        graph = get_graph_from_file(
            dataservice.data_file[0], dataservice.content_type, log
        )
    else:
        graph = get_graph_from_url(dataservice.data_url, dataservice.content_type, log)
    return graph


def upload_graph_to_virtuoso_endpoint(
    import_procedure: ImportProcedure,
    graph: Graph,
    named_graph: str,
    filename: str,
) -> None:
    delete_graph(
        import_procedure.virtuoso_credentials,
        named_graph,
        UPLOAD_MAX,
        UPLOAD_DELAY,
    )
    upload_graph(
        import_procedure.virtuoso_credentials,
        named_graph,
        graph,
        filename,
        UPLOAD_MAX,
        UPLOAD_DELAY,
    )


def _update_graph_for_relation_closure(
    graph: Graph, ontology: Graph, query_to_get_correspondance: str
) -> Graph:
    for result in ontology.query(query_to_get_correspondance).bindings:
        insert_relation = result.get("generic_property")
        where_relation = result.get("specific_property")
        graph.update(
            f"""
            INSERT {{
                ?s <{insert_relation}> ?o.
            }} WHERE {{
                ?s <{where_relation}> ?o.
            }}
        """
        )
    return graph


def _update_graph_for_class_closure(
    graph: Graph, ontology: Graph, query_to_get_correspondance: str
) -> Graph:
    for result in ontology.query(query_to_get_correspondance).bindings:
        insert_class = result.get("generic_class")
        where_class = result.get("specific_class")
        graph.update(
            f"""
            INSERT {{
                ?s a <{insert_class}>.
            }} WHERE {{
                ?s a <{where_class}>.
            }}
        """
        )
    return graph


def rdfs_closure(graph: Graph, ontology: Graph) -> Graph:
    # add property if subPropertyOf
    graph = _update_graph_for_relation_closure(
        graph,
        ontology,
        """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?generic_property ?specific_property WHERE {
                    ?specific_property rdfs:subPropertyOf+ ?generic_property.
            }
        """,
    )
    # add property if equivalentProperty
    graph = _update_graph_for_relation_closure(
        graph,
        ontology,
        """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?generic_property ?specific_property WHERE {
                ?generic_property owl:equivalentProperty|^owl:equivalentProperty ?specific_property.
            }
        """,
    )
    # add property if equivalentProperty
    graph = _update_graph_for_class_closure(
        graph,
        ontology,
        """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?generic_class ?specific_class WHERE {
                ?specific_class rdfs:subClassOf+ ?generic_class.
            }
        """,
    )

    # add class type if equivalentClass
    graph = _update_graph_for_class_closure(
        graph,
        ontology,
        """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?generic_class ?specific_class WHERE {
                ?generic_class owl:equivalentClass|^owl:equivalentClass ?specific_class.
            }
        """,
    )
    return graph

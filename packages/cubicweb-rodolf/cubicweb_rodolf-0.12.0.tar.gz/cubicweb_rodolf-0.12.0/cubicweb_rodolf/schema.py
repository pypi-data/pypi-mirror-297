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

"""cubicweb-rodolf schema"""

from yams.buildobjs import (
    Boolean,
    EntityType,
    RichString,
    String,
    SubjectRelation,
)
from cubicweb.schema import WorkflowableEntityType, ERQLExpression
from cubicweb.rdf import RDF_MIMETYPE_TO_FORMAT


class ProcessType(EntityType):
    name = String(required=True, unique=True)
    regid = String(required=True, unique=True)
    description = RichString(fulltextindexed=True)
    activated = Boolean(required=True, default=True)


class TaskType(EntityType):
    name = String(required=True, unique=True)
    regid = String(required=True, unique=True)
    description = RichString(fulltextindexed=True)
    activated = Boolean(required=True, default=True)


class ImportProcedure(EntityType):
    name = String()
    virtuoso_url = String(required=True)
    virtuoso_user = String(required=True, default="dba")
    virtuoso_password = String(
        required=True,
        __permissions__={
            # Only allow admins to read the password
            "read": ("managers",),
            # Default attribute permissions
            "add": ("managers", ERQLExpression("U has_add_permission X")),
            "update": ("managers", ERQLExpression("U has_update_permission X")),
        },
    )
    sparql_url = String(required=True)
    ontology_file = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )
    shacl_file = SubjectRelation("File", cardinality="??", composite="subject")
    import_recipes = SubjectRelation(
        "ImportRecipe", cardinality="*?", composite="subject"
    )
    activated = Boolean(required=True, default=True)
    tasks = SubjectRelation("ProjectTask", cardinality="*?", composite="subject")


class DataService(EntityType):
    name = String(required=True)
    data_url = String(required=True, unique=True)
    data_file = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )
    refresh_period = String(
        required=True,
        vocabulary=["daily", "weekly", "monthly"],
        default="daily",
    )
    description = String()
    content_type = String(
        required=True,
        vocabulary=RDF_MIMETYPE_TO_FORMAT.keys(),
        default="text/turtle",
    )


class ImportRecipe(EntityType):
    name = String(required=True)
    dataservice = SubjectRelation("DataService", cardinality="1*", composite="object")
    graph_uri = String()
    use_process = SubjectRelation("ProcessType", cardinality="1*", composite="object")
    parameters = SubjectRelation("File", cardinality="?*")


class ProjectTask(EntityType):
    name = String(required=True)
    graph_uri = String()
    use_task = SubjectRelation("TaskType", cardinality="1*", composite="object")
    parameters = SubjectRelation("File", cardinality="?*")


class TaskProcess(WorkflowableEntityType):
    project_task = SubjectRelation(
        "ProjectTask", cardinality="1*", inlined=True, composite="object"
    )
    import_procedure = SubjectRelation(
        "ImportProcedure", cardinality="1*", inlined=True, composite="object"
    )
    rq_task = SubjectRelation(
        "RqTask", cardinality="11", inlined=True, composite="subject"
    )
    has_output_dataset = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )
    log_file = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )


class ImportProcess(WorkflowableEntityType):
    import_recipe = SubjectRelation(
        "ImportRecipe", cardinality="1*", inlined=True, composite="object"
    )
    import_procedure = SubjectRelation(
        "ImportProcedure", cardinality="1*", inlined=True, composite="object"
    )
    rq_task = SubjectRelation(
        "RqTask", cardinality="11", inlined=True, composite="subject"
    )
    has_input_dataset = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )
    has_output_dataset = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )
    import_report = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )
    shacl_valid = Boolean()
    shacl_report = SubjectRelation(
        "File", cardinality="??", inlined=True, composite="subject"
    )

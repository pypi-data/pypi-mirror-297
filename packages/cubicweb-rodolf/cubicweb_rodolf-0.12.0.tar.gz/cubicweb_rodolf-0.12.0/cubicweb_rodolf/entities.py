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

"""cubicweb-rodolf entity's classes"""

from datetime import datetime, timedelta
from typing import Optional
import requests
import pytz
from cubicweb import NoResultError, Binary

from cubicweb.entities import AnyEntity
from rdf_data_manager import VirtuosoCredentials
from rdflib import ConjunctiveGraph, Graph


TIMEDELTA_REFRESH = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
    "monthly": timedelta(days=30),
}


class DataService(AnyEntity):
    __regid__ = "DataService"

    @property
    def refresh_timedelta(self):
        return TIMEDELTA_REFRESH[self.refresh_period]


class ImportProcedure(AnyEntity):
    __regid__ = "ImportProcedure"

    def dc_title(self):
        return self.name if self.name else self.virtuoso_url

    @property
    def delta_import_recipes(self):
        for recipe in self.import_recipes:
            if not recipe.needs_delta_import():
                continue
            yield recipe

    def create_needed_import_process(self, only_delta_import, logger):
        recipes = self.import_recipes
        if only_delta_import:
            recipes = [x for x in self.delta_import_recipes]
        created_import_process = 0
        for recipe in recipes:
            import_process = self._cw.create_entity(
                "ImportProcess",
                import_recipe=(recipe,),
                import_procedure=(self,),
            )
            print(
                f"ImportProcess for {self.virtuoso_url} (recipe : {recipe.name})"
                f" created ({import_process.eid})"
            )
            logger.info(
                f"[rodolf-import]: create rq task for import process "
                f"'{import_process.dc_title()}' ({import_process.eid})"
            )
            created_import_process += 1

        return created_import_process

    @property
    def virtuoso_credentials(self) -> VirtuosoCredentials:
        #  since self.virtuoso_password is readable only by admin
        #  be sure this property is called from an admin cnx
        #  worker and hooks are admin cnx
        return VirtuosoCredentials(
            self.virtuoso_url,
            self.virtuoso_user,
            self.virtuoso_password,
        )

    @property
    def are_virtuoso_credentials_valid(self) -> bool:
        virtuoso_credentials = self.virtuoso_credentials
        resp = requests.post(
            f"{virtuoso_credentials.url}/sparql-graph-crud-auth?",
            auth=requests.auth.HTTPDigestAuth(
                virtuoso_credentials.user, virtuoso_credentials.password
            ),
        )
        return resp.status_code == 200

    @property
    def published_graphs(self) -> ConjunctiveGraph:
        published_graphs = ConjunctiveGraph()
        for recipe in self.import_recipes:
            last_succeed_import_process = recipe.last_succeed_import_process
            graph = published_graphs.get_context(recipe.graph_uri)
            if last_succeed_import_process.has_output_dataset:
                rdf_content = (
                    last_succeed_import_process.has_output_dataset[0]
                    .read()
                    .decode("utf8")
                )
                graph.parse(
                    data=rdf_content,
                    format="ttl",
                )
        return published_graphs


class ImportProcess(AnyEntity):
    __regid__ = "ImportProcess"

    def update_dataset(self, graph: Graph):
        dataset_file = self._cw.create_entity(
            "File",
            title=f"Graph file for ImportProcess#{self.eid}",
            data=Binary(graph.serialize(format="ttl").encode("utf8")),
            data_name=f"output_data_ImportProcess_{self.eid}.ttl",
            data_format="text/turtle",
        )
        self.cw_set(
            has_output_dataset=dataset_file,
        )
        return dataset_file


class ImportRecipe(AnyEntity):
    __regid__ = "ImportRecipe"

    def needs_delta_import(self):
        try:
            import_process = self.last_succeed_import_process
            dataservice = import_process.import_recipe[0].dataservice[0]
            if (
                datetime.now(tz=pytz.utc) - import_process.creation_date
                > dataservice.refresh_timedelta
            ):
                return True
        except NoResultError:
            return True
        return False

    @property
    def last_succeed_import_process(self) -> Optional[ImportProcess]:
        return self._cw.execute(
            "Any I ORDERBY D DESC LIMIT 1 WHERE "
            "I is ImportProcess, "
            "I import_recipe %(recipe_eid)s, "
            "I import_procedure %(import_procedure)s, "
            "I in_state S, S name 'successful', "
            "I creation_date D",
            {
                "recipe_eid": self.eid,
                "import_procedure": self.reverse_import_recipes[0].eid,
            },
        ).one()

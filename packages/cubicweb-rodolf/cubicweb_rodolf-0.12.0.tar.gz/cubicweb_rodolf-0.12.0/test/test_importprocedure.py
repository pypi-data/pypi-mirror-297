# copyright 2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

import logging
import fakeredis
import requests_mock
import rq


from cubicweb.devtools import testlib

from cubicweb_rodolf.import_data import launch_import_procedure

LOGGER = logging.getLogger("testing.rodolf.importdata")


class ImportProcedure(testlib.CubicWebTC):
    def setUp(self):
        super(ImportProcedure, self).setUp()
        self.fakeredis = fakeredis.FakeStrictRedis()

    def _create_test_data(self, cnx):
        process_dryrun = cnx.find("ProcessType", regid="default-dryrun").one()
        ds1 = cnx.create_entity(
            "DataService",
            data_url="https://dbpedia.org/resource/Leonardo_da_Vinci",
            name="DBpedia Leo",
        )
        ir1 = cnx.create_entity(
            "ImportRecipe",
            name="IR1",
            dataservice=[ds1],
            use_process=process_dryrun,
        )
        ds2 = cnx.create_entity(
            "DataService",
            data_url="https://dbpedia.org/resource/Virginia_Woolf",
            name="DBpedia Virgi",
        )
        ir2 = cnx.create_entity(
            "ImportRecipe",
            name="IR2",
            dataservice=[ds2],
            use_process=process_dryrun,
        )
        importprocedure = cnx.create_entity(
            "ImportProcedure",
            virtuoso_url="https://sparql.poulet",
            sparql_url="https://sparql.pouet.fr",
            virtuoso_password="loutre",
            import_recipes=[ir1, ir2],
        )
        cnx.commit()
        return {
            "import_procedure": importprocedure,
            "import_recipes": (ir1, ir2),
            "dataservices": (ds1, ds2),
        }

    @requests_mock.mock()
    def test_only_delta_import(self, mock):
        """
        Trying: create an ImportProcedure from 2 recipes (ir1, ir2).
        Create needed import processes and mark one of them as failed.

        Expected:
        - launching the procedure the first time must contain the 2 recipes
        - launching the procedure in delta mode must now only contain the failed recipe
        - launching the procedure in full mode must contain both recipes
        """
        mock.post("https://sparql.poulet/sparql-graph-crud-auth")
        with self.admin_access.cnx() as cnx, rq.Connection(self.fakeredis):
            data = self._create_test_data(cnx)
            importprocedure = data["import_procedure"]
            ir1, ir2 = data["import_recipes"]
            delta_recipes = [x for x in importprocedure.delta_import_recipes]
            self.assertEqual(delta_recipes, [ir1, ir2])

            # fake running the import processes
            # import_process1 fails and import_process2 succeeds
            nb_task_launched = launch_import_procedure(
                cnx, importprocedure, LOGGER, only_delta_import=True
            )
            self.assertEqual(nb_task_launched, 2)

            import_process1 = cnx.execute(
                "Any X WHERE X is ImportProcess, X import_recipe R, R name 'IR1'"
            ).one()
            import_process2 = cnx.execute(
                "Any X WHERE X is ImportProcess, X import_recipe R, R name 'IR2'"
            ).one()
            wf1 = import_process1.cw_adapt_to("IWorkflowable")
            wf1.fire_transition("starts")
            wf2 = import_process2.cw_adapt_to("IWorkflowable")
            wf2.fire_transition("starts")
            cnx.commit()
            wf1.fire_transition("fails")
            wf2.fire_transition("success")
            cnx.commit()

            # Check data only the failed IR is part of the delta recipes
            delta_recipes = [x for x in importprocedure.delta_import_recipes]
            self.assertEqual(delta_recipes, [ir1])

            # Launching in delta mode creates only 1 task
            nb_task_launched = launch_import_procedure(
                cnx, importprocedure, LOGGER, only_delta_import=True
            )
            self.assertEqual(nb_task_launched, 1)

            # Launching in full mode created 2 tasks
            nb_task_launched = launch_import_procedure(
                cnx, importprocedure, LOGGER, only_delta_import=False
            )
            self.assertEqual(nb_task_launched, 2)

    @requests_mock.mock()
    def test_delete_import_procedure(self, mock):
        mock.delete("https://sparql.poulet/sparql-graph-crud-auth")
        mock.post("https://sparql.poulet/sparql-graph-crud-auth")
        with self.admin_access.cnx() as cnx, rq.Connection(self.fakeredis):
            # create fake data
            data = self._create_test_data(cnx)

            # launch task
            launch_import_procedure(
                cnx, data["import_procedure"], LOGGER, only_delta_import=False
            )

            # assert everything has been created as expected
            self.assertEqual(len(cnx.find("RqTask")), 2)
            self.assertEqual(len(cnx.find("DataService")), 2)
            self.assertEqual(len(cnx.find("ImportRecipe")), 2)
            self.assertEqual(len(cnx.find("ImportProcess")), 2)
            self.assertEqual(len(cnx.find("ImportProcedure")), 1)

            # delete the import procedure
            data["import_procedure"].cw_delete()

            # assert composite object has been deleted as expected
            self.assertEqual(len(cnx.find("RqTask")), 0)
            self.assertEqual(len(cnx.find("ImportRecipe")), 0)
            self.assertEqual(len(cnx.find("ImportProcess")), 0)
            self.assertEqual(len(cnx.find("ImportProcedure")), 0)

            # assert non included object are kept
            self.assertEqual(len(cnx.find("DataService")), 2)

    @requests_mock.mock()
    def test_delete_dataservices(self, mock):
        mock.delete("https://sparql.poulet/sparql-graph-crud-auth")
        mock.post("https://sparql.poulet/sparql-graph-crud-auth")
        with self.admin_access.cnx() as cnx, rq.Connection(self.fakeredis):
            # create fake data
            data = self._create_test_data(cnx)

            # launch task
            launch_import_procedure(
                cnx, data["import_procedure"], LOGGER, only_delta_import=False
            )

            # assert everything has been created as expected
            self.assertEqual(len(cnx.find("RqTask")), 2)
            self.assertEqual(len(cnx.find("DataService")), 2)
            self.assertEqual(len(cnx.find("ImportRecipe")), 2)
            self.assertEqual(len(cnx.find("ImportProcess")), 2)
            self.assertEqual(len(cnx.find("ImportProcedure")), 1)

            # delete all the dataservices
            [ds.cw_delete() for ds in data["dataservices"]]

            # assert composite object has been deleted as expected
            self.assertEqual(len(cnx.find("RqTask")), 0)
            self.assertEqual(len(cnx.find("DataService")), 0)
            self.assertEqual(len(cnx.find("ImportRecipe")), 0)
            self.assertEqual(len(cnx.find("ImportProcedure")), 1)

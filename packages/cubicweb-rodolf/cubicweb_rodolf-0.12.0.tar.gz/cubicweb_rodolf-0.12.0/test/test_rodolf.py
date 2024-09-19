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

import fakeredis
import rq
import logging
import requests_mock

from cubicweb import Binary
from cubicweb.devtools import testlib

from cubicweb_rq.rq import work
from cubicweb_s3storage.testing import S3StorageTestMixin

from cubicweb_rodolf.import_data import launch_import_procedure

LOGGER = logging.getLogger("testing.rodolf.importdata")

RDF_DATA = """
@prefix foaf:	<http://xmlns.com/foaf/0.1/> .
@prefix dbo: <http://dbpedia.org/ontology/> .
@prefix dbr: <http://dbpedia.org/resource/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dbr:Leonardo_da_Vinci a dbo:Person;
    foaf:name "Leonardo da Vinci"@en ;
    dbo:birthYear	"1452"^^xsd:gYear;
    dbo:deathYear	"1519"^^xsd:gYear .

"""


class ImportDataTC(S3StorageTestMixin, testlib.CubicWebTC):
    s3_bucket = "rodolf"

    def work(self, cnx):
        """Start task.

        :param Connection cnx: CubicWeb database connection
        """
        return work(cnx, burst=True, worker_class=rq.worker.SimpleWorker)

    @requests_mock.mock()
    def setUp(self, mock):
        super(ImportDataTC, self).setUp()

        # mock all Virtuoso query (delete and update graph)
        mock.register_uri(
            requests_mock.ANY,
            "/sparql-graph-crud-auth?",
        )

        self.fakeredis = fakeredis.FakeStrictRedis()
        with self.admin_access.cnx() as cnx:
            dataservice = cnx.create_entity(
                "DataService",
                data_url="https://dbpedia.org/resource/Leonardo_da_Vinci",
                name="DBpedia Leo",
            )
            recipe = cnx.create_entity(
                "ImportRecipe",
                name="Ma recette",
                dataservice=[dataservice],
                use_process=cnx.find("ProcessType", regid="default-dryrun").one(),
            )
            with open(self.datapath("dboPerson.rdf"), "rb") as fp:
                file = cnx.create_entity(
                    "File",
                    **{
                        "title": "dboPerson.rdf",
                        "data": Binary(fp.read()),
                        "data_format": "application/rdf+xml",
                        "data_name": "dbo:person ontology",
                    },
                )
            importprocedure = cnx.create_entity(
                "ImportProcedure",
                virtuoso_url="https://sparql.poulet",
                virtuoso_password="loutre",
                import_recipes=[recipe],
                ontology_file=file,
                sparql_url="https://sparql.pouet.fr",
            )
            self.import_procedure_eid = importprocedure.eid
            cnx.commit()

    @requests_mock.mock()
    def test_shacl_ok(self, mock):
        mock.get(
            "https://dbpedia.org/resource/Leonardo_da_Vinci",
            text=RDF_DATA,
            headers={"Content-Type": "text/turtle ; charset=UTF-8"},
        )
        with self.admin_access.cnx() as cnx, rq.Connection(self.fakeredis):
            import_procedure = cnx.entity_from_eid(self.import_procedure_eid)
            with open(self.datapath("ok_shacl.ttl"), "rb") as fp:
                ok_shacl = cnx.create_entity(
                    "File",
                    **{
                        "title": "ok_shacl.ttl",
                        "data": Binary(fp.read()),
                        "data_format": "text/turtle",
                        "data_name": "shacl ok",
                    },
                )
            import_procedure.cw_set(
                shacl_file=ok_shacl
            )
            cnx.commit()
            started_processes = launch_import_procedure(cnx, import_procedure, LOGGER)
            assert started_processes == 1
            task = cnx.execute("Any X WHERE X is RqTask, X name 'import_process'").one()
            job = task.cw_adapt_to("IRqJob")
            self.assertEqual(job.status, "queued")
            self.work(cnx)
            job.refresh()
            self.assertEqual(job.status, "finished")
            log = job.log
            for expected in (
                "Starting import process",
                "Data was successfully downloaded",
                "Data was successfully validated",
            ):
                self.assertIn(expected, log)
            import_process = task.reverse_rq_task[0]
            wf = import_process.cw_adapt_to("IWorkflowable")
            self.assertEqual(wf.state, "successful")
            self.assertEqual(len(import_process.has_input_dataset), 1)
            input_dataset = import_process.has_input_dataset[0]
            self.assertEqual(
                input_dataset.data_name,
                f"input_data_ImportProcess_{import_process.eid}.ttl",
            )

    @requests_mock.mock()
    def test_shacl_nok(self, mock):
        mock.get(
            "https://dbpedia.org/resource/Leonardo_da_Vinci",
            text=RDF_DATA,
            headers={"Content-Type": "text/turtle ; charset=UTF-8"},
        )
        with self.admin_access.cnx() as cnx, rq.Connection(self.fakeredis):
            import_procedure = cnx.entity_from_eid(self.import_procedure_eid)
            with open(self.datapath("nok_shacl.ttl"), "rb") as fp:
                nok_shacl = cnx.create_entity(
                    "File",
                    **{
                        "title": "nok_shacl.ttl",
                        "data": Binary(fp.read()),
                        "data_format": "text/turtle",
                        "data_name": "shacl nok",
                    },
                )
            import_procedure.cw_set(
                shacl_file=nok_shacl
            )
            cnx.commit()
            started_processes = launch_import_procedure(cnx, import_procedure, LOGGER)
            assert started_processes == 1
            task = cnx.execute("Any X WHERE X is RqTask, X name 'import_process'").one()
            job = task.cw_adapt_to("IRqJob")
            self.assertEqual(job.status, "queued")
            self.work(cnx)
            job.refresh()
            self.assertEqual(job.status, "finished")
            log = job.log
            for expected in (
                "Starting import process",
                "Data was successfully downloaded",
                "Data from DBpedia Leo does not comply with SHACL file nok_shacl.ttl",
                "raises 1 violations",
                "See details in SHACL Log",
            ):
                self.assertIn(expected, log)

            import_process = task.reverse_rq_task[0]
            wf = import_process.cw_adapt_to("IWorkflowable")
            self.assertEqual(wf.state, "successful")
            self.assertEqual(import_process.shacl_valid, False)

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

"""cubicweb-rodolf specific hooks and operations"""
import os
from datetime import datetime, timedelta
import logging
from threading import Thread

import rq
from cubicweb import ValidationError
from cubicweb.server.hook import Hook, match_rtype
from cubicweb.predicates import is_instance
from cubicweb_rq.ccplugin import get_rq_redis_connection
from cubicweb_s3storage.storages import S3Storage
from rdflib import Graph
from rdf_data_manager import delete_graph

from cubicweb_rodolf.process_helpers import (
    UPLOAD_DELAY,
    UPLOAD_MAX,
    upload_graph_to_virtuoso_endpoint,
)
from cubicweb_rodolf.import_data import (
    execute_task,
    import_data,
    launch_import_procedure,
)


# check each RODOLF_IMPORT_DELTA seconds if there is a recipe to execute
RODOLF_IMPORT_DELTA = timedelta(
    seconds=float(os.getenv("RODOLF_IMPORT_DELTA", 60 * 60))
)

RODOLF_CHECK_TASK_STATUS_DELAY = timedelta(
    seconds=float(os.getenv("RODOLF_CHECK_TASK_STATUS_DELAY", 60 * 2))
)


def looping_task_rodolf_import(repo):
    logger = logging.getLogger("rodolf-import-thread")
    with repo.internal_cnx() as cnx:
        started_processes = 0
        procedures = cnx.find("ImportProcedure").entities()
        for procedure in procedures:
            started_processes += launch_import_procedure(
                cnx,
                procedure,
                logger,
            )
        logger.info(f"[rodolf-import]: {started_processes} rq-tasks created")
        logger.info(
            f"[rodolf-import] next import in {RODOLF_IMPORT_DELTA} seconds (at"
            f" {datetime.now() + RODOLF_IMPORT_DELTA})"
        )


def looping_task_rodolf_check_tasks_status(repo):
    repo.info("Check status of unfinished tasks")
    redis_cnx_url = get_rq_redis_connection(repo.config.appid)
    with repo.internal_cnx() as cnx, rq.Connection(redis_cnx_url):
        # iterate over all unfinished task
        rq_tasks = cnx.execute("Any X WHERE X is RqTask, X status NULL")
        for rq_task in rq_tasks.entities():
            rq_job = rq_task.cw_adapt_to("IRqJob")
            import_process = rq_task.reverse_rq_task[0]
            wf = import_process.cw_adapt_to("IWorkflowable")
            status = rq_job.get_job().get_status()

            if status == rq.job.JobStatus.FAILED:
                repo.info("Task %s has failed", rq_task.eid)
                # mark task and related import_process as failure
                rq_job.handle_failure()
                wf.fire_transition("fails")

            elif status == rq.job.JobStatus.FINISHED:
                # mark task and related import_process as success
                repo.info("Task %s has finished", rq_task.eid)
                rq_job.handle_finished()
                wf.fire_transition("success")

            else:
                repo.debug("Task %s is ongoing.", rq_task.eid)

        cnx.commit()


class RodolfImportScheduler(Hook):
    __regid__ = "rodolf.server-startup-rodolf-import-hook"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        if self.repo.has_scheduler():
            self.repo.looping_task(
                RODOLF_IMPORT_DELTA.total_seconds(),
                looping_task_rodolf_import,
                self.repo,
            )

            self.repo.looping_task(
                RODOLF_CHECK_TASK_STATUS_DELAY.total_seconds(),
                looping_task_rodolf_check_tasks_status,
                self.repo,
            )


class S3StorageStartupHook(Hook):
    __regid__ = "rodolf.server-startup-hook"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        storage = S3Storage(os.environ.get("RODOLF_S3_BUCKET", "rodolf"))
        self.repo.system_source.set_storage("File", "data", storage)


class ProcessTypeStartupHook(Hook):
    """Register Process Type entity"""

    __regid__ = "rodolf.process-type-register-hook"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        if "rodolf.appobject.processtype" not in self.repo.vreg:
            self.error("No Rodolf ProcessType found")
            return

        process_vreg = self.repo.vreg["rodolf.appobject.processtype"]
        with self.repo.internal_cnx() as cnx:
            for process_func_id in process_vreg.keys():
                process_class = process_vreg[process_func_id][
                    0
                ]  # there is only one per regid
                uiname = getattr(process_class, "__uiname__", process_class.__regid__)
                try:
                    rset = cnx.find("ProcessType", regid=process_func_id)
                except KeyError:
                    # this exception must be handle, because the hook is called
                    # *before* the migration can be executed. Therefore it's
                    # possible to be in a state where ProcessType does not exists
                    # yet. It should only happen here though.
                    self.error(
                        "ProcessType is not a known entity_type. It probably "
                        "means you need to run a migration."
                    )
                    return
                if not rset:
                    cnx.create_entity("ProcessType", regid=process_func_id, name=uiname)
                else:
                    pf = rset.one()
                    if not pf.activated:
                        pf.cw_set(activated=True)
                    if pf.name == pf.regid and uiname != pf.regid:
                        pf.cw_set(name=uiname)
            cnx.commit()


class TaskTypeStartupHook(Hook):
    """Register Task Type entity"""

    __regid__ = "rodolf.task-type-register-hook"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        if "rodolf.appobject.tasktype" not in self.repo.vreg:
            self.error("No Rodolf TaskType found")
            return

        task_vreg = self.repo.vreg["rodolf.appobject.tasktype"]
        with self.repo.internal_cnx() as cnx:
            for task_type_id in task_vreg.keys():
                try:
                    rset = cnx.find("TaskType", regid=task_type_id)
                except KeyError:
                    # this exception must be handle, because the hook is called
                    # *before* the migration can be executed. Therefore it's
                    # possible to be in a state where ProcessType does not exists
                    # yet. It should only happen here though.
                    self.error(
                        "TaskType is not a known entity_type. It probably "
                        "means you need to run a migration."
                    )
                    return
                if not rset:
                    cnx.create_entity("TaskType", regid=task_type_id, name=task_type_id)
                else:
                    pf = rset.one()
                    if not pf.activated:
                        pf.cw_set(activated=True)
            cnx.commit()


class EnqueueImportProcessHook(Hook):
    __regid__ = "rodolf.enqueue-importprocess-hook"
    __select__ = Hook.__select__ & is_instance("ImportProcess")
    events = ("after_add_entity",)

    def __call__(self):
        task_title = "import-process {eid} ({date})".format(
            eid=self.entity.eid,
            date=datetime.utcnow().strftime("%Y-%m-%d"),
        )
        rqtask = self._cw.create_entity(
            "RqTask", name="import_process", title=task_title
        )
        self.entity.cw_set(rq_task=rqtask)
        self._cw.commit()
        rqtask.cw_adapt_to("IRqJob").enqueue(
            import_data, import_process_eid=self.entity.eid
        )
        self._cw.commit()


class EnqueueTaskHook(Hook):
    __regid__ = "rodolf.enqueue-task-hook"
    __select__ = Hook.__select__ & is_instance("TaskProcess")
    events = ("after_add_entity",)

    def __call__(self):
        task_title = "task-process {eid} ({date})".format(
            eid=self.entity.eid,
            date=datetime.utcnow().strftime("%Y-%m-%d"),
        )
        rqtask = self._cw.create_entity("RqTask", name="task_process", title=task_title)
        self.entity.cw_set(rq_task=rqtask)
        self._cw.commit()
        rqtask.cw_adapt_to("IRqJob").enqueue(
            execute_task, task_process_eid=self.entity.eid
        )
        self._cw.commit()


class UploadOntologyHook(Hook):
    __regid__ = "rodolf.upload-ontology-hook"
    __select__ = Hook.__select__ & match_rtype("ontology_file")
    events = ("after_add_relation",)

    def __call__(self):
        ontology_graph = Graph()
        file = self._cw.entity_from_eid(self.eidto)
        procedure = self._cw.entity_from_eid(self.eidfrom)
        ontology_graph.parse(
            data=file.data.read(),
            format=file.data_format,
        )
        upload_graph_to_virtuoso_endpoint(
            procedure,
            ontology_graph,
            f"urn:rodolf:{procedure.eid}:ontology",
            file.download_file_name(),
        )


class UnlinkRecipeHook(Hook):
    __regid__ = "rodolf.unlink-recipe-hook"
    __select__ = Hook.__select__ & match_rtype("import_recipes")
    events = ("after_delete_relation",)

    def __call__(self):
        procedure = self._cw.entity_from_eid(self.eidfrom)
        recipe = self._cw.entity_from_eid(self.eidto)
        thread = Thread(
            target=delete_graph,
            args=(
                procedure.virtuoso_credentials,
                recipe.graph_uri,
                UPLOAD_MAX,
                UPLOAD_DELAY,
            ),
        )
        thread.start()
        # Do not wait until the graph is deleted to not block the UI


class SynchroniseDataServiceURLAndFile(Hook):
    __regid__ = "rodolf.sync-dataservice-url-file"
    __select__ = Hook.__select__ & is_instance("DataService")
    events = (
        "after_add_entity",
        "after_update_entity",
    )

    def __call__(self):
        self.entity.cw_clear_all_caches()  # clear caches to have reload relations
        if not self.entity.data_file:
            return
        data_file = self.entity.data_file[0]
        if data_file.download_url() != self.entity.data_url:
            self.entity.cw_set(data_file=None)
            data_file.cw_delete()


class CheckVirtuosoDBAConnection(Hook):
    __regid__ = "rodolf.check-virtuoso-dba-connection"
    __select__ = Hook.__select__ & is_instance("ImportProcedure")
    events = (
        "before_add_entity",
        "before_update_entity",
    )

    def __call__(self):
        if set(self.entity.cw_edited) & set(
            ["virtuoso_url", "virtuoso_user", "virtuoso_password"]
        ):
            if not self.entity.are_virtuoso_credentials_valid:
                raise ValidationError(
                    self.entity.eid,
                    {"virtuoso_credentials": "Credentials are not valid"},
                )

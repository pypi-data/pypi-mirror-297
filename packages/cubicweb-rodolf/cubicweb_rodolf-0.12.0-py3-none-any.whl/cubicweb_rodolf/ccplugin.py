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
import logging
import rq


from cubicweb.cwctl import CWCTL
from cubicweb.toolsutils import Command

from cubicweb_rq.ccplugin import get_rq_redis_connection
from cubicweb_rq import admincnx

from cubicweb_rodolf.import_data import launch_import_procedure


@CWCTL.register
class PeriodicImport(Command):
    """run ``cubicweb_rodolf.import_data`` in RqTask"""

    arguments = "<instance>"
    name = "rodolf-import"
    max_args = None
    min_args = 1
    options = [
        (
            "force-all",
            {
                "action": "store_true",
                "default": "False",
                "help": "Launch every ImportRecipe for every ImportProcedure, "
                "even if they are up-to-date",
            },
        ),
    ]

    def run(self, args):
        appid = args.pop()
        connection = get_rq_redis_connection(appid)
        self.logger = logging.getLogger("rodolf-import")
        self.logger.setLevel(logging.INFO)
        started_processes = 0
        with admincnx(appid) as cnx, rq.Connection(connection):
            procedures = cnx.find("ImportProcedure").entities()
            for procedure in procedures:
                started_processes += launch_import_procedure(
                    cnx,
                    procedure,
                    self.logger,
                    only_delta_import=(not self.config.force_all),
                )
        self.logger.info(f"[rodolf-import]: {started_processes} rq-tasks created")

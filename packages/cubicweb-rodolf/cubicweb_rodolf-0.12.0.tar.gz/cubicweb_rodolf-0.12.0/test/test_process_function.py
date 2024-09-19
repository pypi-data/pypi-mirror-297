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


from cubicweb.devtools import testlib


class ProcessTypeCreation(testlib.CubicWebTC):
    def test_process_function_creation(self):
        with self.admin_access.cnx() as cnx:
            process_types = cnx.find("ProcessType").entities()
            ptypes_regid = [pf.regid for pf in process_types]
            self.assertTrue(len(ptypes_regid) >= 2)
            self.assertIn("default", ptypes_regid)
            self.assertIn("default-dryrun", ptypes_regid)
            self.assertEqual(
                cnx.find("ProcessType", regid="default").one().name,
                "Processus d'import standard"
            )

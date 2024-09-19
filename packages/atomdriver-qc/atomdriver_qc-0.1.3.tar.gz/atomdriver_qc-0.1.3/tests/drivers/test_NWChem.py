#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from io import StringIO
from textwrap import dedent

from conformer_core.records import RecordStatus

from atomdriver.drivers.nwchem import NWChem
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2


class NWChemTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = NWChem()
        self.backend.configure()
        self.sys = make_system(atoms=2, ghost_atoms=2)

    def tearDown(self) -> None:
        self.backend.cleanup()
        return super().tearDown()

    def test_atom(self):
        atom = self.sys[0]
        self.assertEqual(self.backend.template.atom_to_string(atom), "H    0.0 0.0 0.0")

    def test_ghost_atom(self):
        atom = self.sys[2]
        self.assertEqual(
            self.backend.template.atom_to_string(atom), "bqH    0.0 0.0 0.0"
        )

    def test_template(self):
        out_templ = self.backend.template.system_to_string(self.sys, name="fragment_1")
        self.assertEqual(
            out_templ,
            dedent(
                """\
            start fragment_1
            title "fragment_1"
            charge 0
            geometry
            H    0.0 0.0 0.0
            H    1.0 1.0 1.0
            bqH    0.0 0.0 0.0
            bqH    1.0 1.0 1.0
            end
            basis
                * library 6-31G
            end
            task scf
            """
            ),
        )

    def test_properties(self):
        props = self.backend.get_properties(
            None,
            [
                StringIO(
                    dedent(
                        """\
        Total SCF energy =   -108.300041537502
        Total times  cpu:        5.9s     wall:       18.9s
        """
                    )
                )
            ],
        )
        self.assertDictEqual(
            props.to_dict(),
            {
                "total_energy": -108.300041537502,
                "cpu_time": 5.9,
            },
        )

    @unittest.skipIf(not NWChem.is_available(), "Could not find NWChem exe")
    def test_exec(self):
        res = self.backend(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -1.108592485356, 5)


# need to add test for exec (similar to orca)

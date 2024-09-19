#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import unittest
from io import StringIO
from textwrap import dedent

from conformer_core.records import RecordStatus

from atomdriver.drivers.mopac import MOPAC
from tests import AtomDriverTestCase
from tests._util import make_system
from tests.drivers.util import H2


class MOPACTestCases(AtomDriverTestCase):
    def setUp(self) -> None:
        self.backend = MOPAC()
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
        self.assertEqual(self.backend.template.atom_to_string(atom), None)

    def test_template(self):
        out_templ = self.backend.template.system_to_string(self.sys, name="fragment_1")
        self.assertEqual(
            out_templ,
            dedent(
                """\
            PM7 XYZ PRECISE NOSYM NOREOR GEO-OK


            H    0.0 0.0 0.0
            H    1.0 1.0 1.0
            """
            ),
        )

    def test_properties(self):
        props = self.backend.get_properties(
            None,
            [
                "output",
                StringIO(
                    dedent(
                        """\
        TOTAL ENERGY            =      -1915.74402 EV
        COMPUTATION TIME        =       0.05 SECONDS
        """
                    )
                ),
            ],
        )
        self.assertDictEqual(
            props.to_dict(),
            {
                "total_energy": -70.40229478174886,
                "cpu_time": 0.05,
            },
        )

    @unittest.skipIf(not MOPAC.is_available(), "Could not find MOPAC exe")
    def test_exec(self):
        res = self.backend(H2())

        # Now checkout how our job went :)
        self.assertEqual(res.status, RecordStatus.COMPLETED)
        self.assertAlmostEqual(res.properties["total_energy"], -1.030707, 5)

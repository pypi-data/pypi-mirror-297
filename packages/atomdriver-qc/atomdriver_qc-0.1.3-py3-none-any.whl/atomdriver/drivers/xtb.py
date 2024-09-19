#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import subprocess
from os import environ
from typing import List, Tuple

from conformer_core.properties.extraction import calc_property

from atomdriver.abstract_driver import (
    RunContext,
    ShellCommandDriver,
)


class xTB(ShellCommandDriver):
    # class Options(ShellCommandDriverOptions):

    DEFAULT_TEMPLATE_PARAMS = {
        "template": """\
            {n_atoms}
            Fragment {name}; Charge={charge}; Multiplicity={mult}
            {geometry}
        """,
        "atom": "{symbol}    {x} {y} {z}",
        "ghost_atom": None,
    }
    FILE_MANIFEST = {"input": ".xyz", "output": ".out"}
    STDOUT_FILE = "output"
    RUN_CMD = "xtb"
    AVAILABLE_RETURN_CODE = 1

    @classmethod
    def is_available(cls):
        try:
            return (
                subprocess.run(
                    [cls.RUN_CMD, "file_does_not_exits"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode
                == cls.AVAILABLE_RETURN_CODE
            )
        except FileNotFoundError:
            return False

    def configure(self) -> None:
        super().configure()
        alloc = self.allocation
        if alloc.memory:
            environ["OMP_STACKSIZE"] = f"{alloc.memory } M"
        environ["OMP_NUM_THREADS"] = f"{alloc.cpus},1"

    def get_run_cmd(self, ctx: RunContext) -> Tuple[str, List[str]]:
        return self.RUN_CMD, [str(ctx.files["input"])]

    @calc_property(source="re_file", patterns=[r"TOTAL ENERGY\s+(-?\d+\.\d+)\sEh"])
    def prop_total_energy(self, ctx, m, _):
        return float(m[1])

    @calc_property(
        source="re_file",
        patterns=[r"cpu-time:\s+(\d+) d,\s+(\d+) h,\s+(\d+) min,\s+(\d+.\d+) sec"],
    )
    def prop_cpu_time(self, ctx, m, _):
        times = [float(m[1]) * 86400, float(m[2]) * 3600, float(m[3]) * 60, float(m[4])]
        return sum(times)

    @calc_property(source="re_file", patterns=[r"TOTAL ENTHALPY\s+(-?\d+.\d+) Eh"])
    def prop_total_enthalpy(self, ctx, m, _):
        """
        Properties from frequency calcualtions
        Enthalphy reported in Eh
        """
        return float(m[1])

    @calc_property(
        source="re_file", patterns=[r"TOT\s+\d+.\d+\s+\d+.\d+\s+(\d+.\d+)\s+\d+.\d+"]
    )
    def prop_total_entropy(self, ctx, m, _):
        """
        Entropy reported in cal/mol*K
        """
        return float(m[1])

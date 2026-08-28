# (C) Copyright IBM 2026
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


from typing import TypedDict

from typeguard import typechecked

from qc_grader.grader.grade import grade_answer

_CHALLENGE = "tcs_enablement_2026"
_LAB = "lab_implicit_solvent"


System = TypedDict("System", {"casci_e": float})
SweepPoint = TypedDict("SweepPoint", {"energy": float})


def _grade(answer_dict, exercise: str) -> None:
    grade_answer(answer_dict, lab=_LAB, exercise=exercise, challenge=_CHALLENGE)


@typechecked
def grade_lab_implicit_solvent_ex1(
    diy_systems: dict[str, System],
    diy_sqd_sweep_results: dict[str, list[SweepPoint]],
) -> None:
    """
    Grade Exercise 1: Ethanol and Methylamine SQD/IEF-PCM reproduction.

    Args:
        diy_systems: The DIY cell's `diy_systems` dict -- "Ethanol" and/or
            "Methylamine", each with a `casci_e` field (Hartree).
        diy_sqd_sweep_results: The DIY cell's `diy_sqd_sweep_results` dict --
            same keys, each a list of sweep-point dicts with an `energy`
            field (Hartree).
    """
    answer_dict = {
        name: (min(r["energy"] for r in diy_sqd_sweep_results[name]), s["casci_e"])
        for name, s in diy_systems.items()
        if name in diy_sqd_sweep_results
    }
    _grade(answer_dict, "ex1")

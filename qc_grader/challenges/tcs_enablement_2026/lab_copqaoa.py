# (C) Copyright IBM 2026
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


from typeguard import typechecked

from qc_grader.grader.grade import grade_answer

_CHALLENGE = "tcs_enablement_2026"
_LAB = "lab_copqaoa"


def _grade(answer_dict, exercise: str) -> None:
    grade_answer(answer_dict, lab=_LAB, exercise=exercise, challenge=_CHALLENGE)


@typechecked
def grade_lab_copqaoa_ex1(answer_dict: dict[str, int]) -> None:
    """
    Grade Exercise 1: retrain the 100-item cop-QAOA angles.

    Args:
        answer_dict: Measurement counts sampled at the trained angles, on the
            100-item circuit (i.e. `res_100[0].data.meas.get_counts()`).
    """
    _grade(answer_dict, "ex1")


@typechecked
def grade_lab_copqaoa_ex2(answer_dict: dict[str, int]) -> None:
    """
    Grade Exercise 2: retrain the 150-item cop-QAOA angles.

    Args:
        answer_dict: Measurement counts sampled at the trained angles, on the
            150-item circuit (i.e. `res_r150[0].data.meas.get_counts()`).
    """
    _grade(answer_dict, "ex2")


@typechecked
def grade_lab_copqaoa_ex3(answer_dict: dict[str, int]) -> None:
    """
    Grade Exercise 3: the training-pipeline drill, swapped onto a paper
    instance.

    Args:
        answer_dict: Measurement counts sampled at the pipeline's trained angles,
            on whichever paper instance (100- or 150-item) was swapped in.
    """
    _grade(answer_dict, "ex3")

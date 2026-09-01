# (C) Copyright IBM 2026
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of the license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.


"""
TCS Enablement Workshop 2026 - Grading Functions
"""

from qc_grader.grader.grade import create_check_progress_function
from .lab_copqaoa import (
    grade_lab_copqaoa_ex1,
    grade_lab_copqaoa_ex2,
    grade_lab_copqaoa_ex3,
)

from .lab_implicit_solvent import grade_lab_implicit_solvent_ex1
from .lab_non_covalent_sqd import grade_lab_non_covalent_sqd_ex1

_CHALLENGE = "tcs_enablement_2026"
check_progress = create_check_progress_function(_CHALLENGE)

__all__ = [
    "check_progress",
    # lab_copqaoa
    "grade_lab_copqaoa_ex1",
    "grade_lab_copqaoa_ex2",
    "grade_lab_copqaoa_ex3",
    # lab_implicit_solvent
    "grade_lab_implicit_solvent_ex1",
    # lab_non_covalent_sqd
    "grade_lab_non_covalent_sqd_ex1",
]

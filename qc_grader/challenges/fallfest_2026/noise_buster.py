"""
Fall Fest 2026 - Noise Busters - Grading Functions
"""

from typeguard import typechecked

from qc_grader.grader.grade import grade_answer

_CHALLENGE = "fallfest_2026"
_LAB = "noise_buster"


@typechecked
def check_result(value: float | int) -> None:
    """Submit your mitigated <Z6 Z7> expectation value for scoring."""
    grade_answer(float(value), lab=_LAB, exercise="scored", challenge=_CHALLENGE)

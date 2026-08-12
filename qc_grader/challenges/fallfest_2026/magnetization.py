"""
Fall Fest 2026 - SLC Magnetization Partner Lab - Grading Functions
"""

from typing import Any, TypedDict

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import BoxOp, CircuitInstruction
from qiskit.quantum_info import PauliLindbladMap
from qiskit_ibm_runtime import QuantumProgram
from typeguard import typechecked

from qc_grader.grader.grade import grade_answer

_CHALLENGE = "fallfest_2026"
_LAB = "magnetization"
_NUM_QUBITS = 20


class _NoiseLearnerOptions(TypedDict):
    num_randomizations: int
    shots_per_randomization: int
    layer_pair_depths: list[int] | np.ndarray
    post_selection: dict[str, Any]


def _grade(answer: Any, exercise: str) -> None:
    grade_answer(answer, lab=_LAB, exercise=exercise, challenge=_CHALLENGE)


@typechecked
def grade_magnetization_ex1(
    boxed_circuit: QuantumCircuit,
    unique_2q_instructions: list[CircuitInstruction],
    noise_model_paulis: dict[str, PauliLindbladMap],
    backward_bounds: dict[str, PauliLindbladMap],
    noise_learner_options: _NoiseLearnerOptions,
) -> None:
    """Grade Exercise 1 - boxing + noise-learning setup."""
    n_boxes = sum(1 for inst in boxed_circuit.data if isinstance(inst.operation, BoxOp))
    depths = noise_learner_options["layer_pair_depths"]

    facts = {
        "num_qubits": int(boxed_circuit.num_qubits),
        "num_boxes": int(n_boxes),
        "num_unique_layers": int(len(unique_2q_instructions)),
        "num_noise_models": int(len(noise_model_paulis)),
        "num_backward_bounds": int(len(backward_bounds)),
        "num_layer_pair_depths": int(len(depths)),
        "num_randomizations": int(noise_learner_options["num_randomizations"]),
        "shots_per_randomization": int(
            noise_learner_options["shots_per_randomization"]
        ),
    }
    _grade(facts, "ex1")


@typechecked
def grade_magnetization_ex2(
    local_scales_per_site: list,
    gamma_per_site: list[float] | np.ndarray,
    num_qubits: int,
) -> None:
    """Grade Exercise 2 - per-site local scales + sampling overhead gamma."""
    g = np.asarray(gamma_per_site, dtype=float)

    facts = {
        "num_qubits": int(num_qubits),
        "num_sites_scales": int(len(local_scales_per_site)),
        "num_sites_gamma": int(len(gamma_per_site)),
        "gamma_min": float(g.min()),
        "gamma_max": float(g.max()),
        "gamma_sq_max": float((g**2).max()),
    }
    _grade(facts, "ex2")


@typechecked
def grade_magnetization_ex3(
    program: QuantumProgram,
    num_qubits: int,
    num_randomizations: int,
) -> None:
    """Grade Exercise 3 - one samplex item per site in a single QuantumProgram."""
    # Newer QuantumProgram exposes `.samplex_items`; fall back to `.items`.
    items = getattr(program, "samplex_items", None)
    if items is None:
        items = program.items

    facts = {
        "num_qubits": int(num_qubits),
        "num_items": int(len(items)),
        "num_randomizations": int(num_randomizations),
    }
    _grade(facts, "ex3")


@typechecked
def grade_magnetization_ex4(
    magnetization: np.ndarray | list[float],
    magnetization_raw: np.ndarray | list[float],
    magnetization_exact: np.ndarray | list[float],
) -> None:
    """Grade Exercise 4 (scored) - the mitigated magnetization profile."""
    m = np.asarray(magnetization, dtype=float)
    r = np.asarray(magnetization_raw, dtype=float)
    e = np.asarray(magnetization_exact, dtype=float)

    facts = {
        "num_qubits": int(m.size),
        "slc_total_abs_error": float(np.abs(m - e).sum()),
        "raw_total_abs_error": float(np.abs(r - e).sum()),
        "slc_total_magnetization": float(m.sum()),
        "exact_total_magnetization": float(e.sum()),
    }
    _grade(facts, "ex4")

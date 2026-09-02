"""
Fall Fest 2026 - SLC Magnetization Partner Lab - Grading Functions
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import BoxOp, CircuitInstruction
from qiskit.quantum_info import QubitSparsePauliList
from qiskit_ibm_runtime import QuantumProgram
from typeguard import typechecked

from qc_grader.grader.grade import grade_answer

_CHALLENGE = "fallfest_2026"
_LAB = "magnetization"
_NUM_QUBITS = 20


@typechecked
def grade_magnetization_ex1(
    boxed_circuit: QuantumCircuit,
    unique_2q_instructions: list[CircuitInstruction],
    noise_model_paulis: dict[str, QubitSparsePauliList],
) -> None:
    """Grade Exercise 1: box the ISA circuit and learn per-layer noise."""
    n_boxes = sum(1 for inst in boxed_circuit.data if isinstance(inst.operation, BoxOp))

    facts = {
        "num_qubits": int(boxed_circuit.num_qubits),
        "num_boxes": int(n_boxes),
        "num_unique_layers": int(len(unique_2q_instructions)),
        "num_noise_models": int(len(noise_model_paulis)),
    }
    grade_answer(facts, lab=_LAB, exercise="ex1", challenge=_CHALLENGE)


@typechecked
def grade_magnetization_ex2(gamma_per_site: list[float] | np.ndarray) -> None:
    """Grade Exercise 2: the per-site sampling overhead gamma."""
    g = np.asarray(gamma_per_site, dtype=float)

    facts = {
        "gamma_min": float(g.min()),
        "gamma_max": float(g.max()),
        "gamma_sq_max": float((g**2).max()),
    }
    grade_answer(facts, lab=_LAB, exercise="ex2", challenge=_CHALLENGE)


@typechecked
def grade_magnetization_ex3(
    program: QuantumProgram,
    final_template_circuit: QuantumCircuit,
    num_qubits: int,
    num_randomizations: int,
) -> None:
    """Grade Exercise 3: the samplex item args and program assembly."""
    # Newer QuantumProgram exposes `.samplex_items`; fall back to `.items`.
    items = getattr(program, "samplex_items", None)
    if items is None:
        items = program.items

    expected_shape = (int(num_randomizations),)
    expected_clbits = int(final_template_circuit.num_clbits)

    num_bad_shape = sum(1 for it in items if tuple(it.shape) != expected_shape)
    num_bad_circuit = sum(
        1 for it in items if int(it.circuit.num_clbits) != expected_clbits
    )

    facts = {
        "num_qubits": int(num_qubits),
        "num_items": int(len(items)),
        "num_bad_shape": int(num_bad_shape),
        "num_bad_circuit": int(num_bad_circuit),
    }
    grade_answer(facts, lab=_LAB, exercise="ex3", challenge=_CHALLENGE)


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
    grade_answer(facts, lab=_LAB, exercise="ex4", challenge=_CHALLENGE)

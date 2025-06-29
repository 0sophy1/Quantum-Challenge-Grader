from typeguard import typechecked
from typing import List

from qiskit import transpile, QuantumCircuit, generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager
from qiskit.circuit.library import QuantumVolume, QAOAAnsatz
from qiskit.providers.fake_provider import GenericBackendV2

from qiskit_ibm_runtime.fake_provider import FakeBrisbane
import rustworkx

from qc_grader.grader.grade import grade


_challenge_id = 'qgss_2025'

# TODO!!!! 

@typechecked
def grade_lab2_ex1(
    solutions: List, backend
) -> None:
    
    properties = backend.properties()
    num_qubits = backend.num_qubits
    coupling_map = backend.coupling_map
    index_t1_max, max_t1 = max(
        ((i, properties.t1(i)) for i in range(num_qubits)), key=lambda x: x[1]
    )
    index_t2_max, max_t2 = max(
        ((i, properties.t2(i)) for i in range(num_qubits)), key=lambda x: x[1]
    )
    index_min_x_error, min_x_error = min(
        ((i, properties.gate_error(qubits=i, gate="x")) for i in range(num_qubits)),
        key=lambda x: x[1],
    )
    index_min_readout, min_readout = min(
        ((i, properties.readout_error(i)) for i in range(num_qubits)),
        key=lambda x: x[1],
    )
    min_ecr_pair, min_ecr_error = min(
        ((pair, properties.gate_error(gate="ecr", qubits=pair)) for pair in coupling_map),
        key=lambda x: x[1],
    )
    key_values = [
        [index_t1_max, max_t1],
        [index_t2_max, max_t2],
        [index_min_x_error, min_x_error],
        [index_min_readout, min_readout],
        [min_ecr_pair, min_ecr_error],
    ]

    grade({
        'solutions': solutions,
        'key_values': key_values,
    }, 'lab2-ex1', _challenge_id)


def prepare_graph(graph) -> list[tuple[str, float]]:
    # Convert the graph to Pauli list.
    pauli_list = []
    for edge in list(graph.edge_list()):
        paulis = ["I"] * len(graph)
        paulis[edge[0]], paulis[edge[1]] = "Z", "Z"
        weight = graph.get_edge_data(edge[0], edge[1])
        pauli_list.append(("".join(paulis)[::-1], weight))
    return pauli_list


@typechecked
def grade_lab2_ex2(
    cost_hamiltonian: SparsePauliOp, graph: rustworkx.PyGraph
) -> None:
    prepared_graph = prepare_graph(graph)

    grade({
        'cost_hamiltonian': cost_hamiltonian,
        'prepared_graph': prepared_graph,
    }, 'lab2-ex2', _challenge_id)


#TODO obscuse
def prepare_backend(backend, circuit):
    properties = backend.properties()
    n = len({circuit.qubits.index(q) for instr in circuit.data for q in instr.qubits})
    qubit_layout = list(circuit.layout.initial_layout.get_physical_bits().keys())[:n]
    # We define various lists of metrics for all the qubits of the backend
    # Readout error
    readout_error = []
    for i in qubit_layout:
        readout_error.append(properties.readout_error(i))
    acc_readout_error = sum(readout_error)
    # Defining two qubit gates
    if "ecr" in (backend.configuration().basis_gates):
        two_qubit_gate = "ecr"
    elif "cz" in (backend.configuration().basis_gates):
        two_qubit_gate = "cz"
    # Initializing quantities
    acc_single_qubit_error = 0
    acc_two_qubit_error = 0
    single_qubit_gate_count = 0
    two_qubit_gate_count = 0
    # Looping over the instructions to account for the errors
    for instruction in circuit.data:
        if instruction.operation.num_qubits == 1:
            index = instruction.qubits[0]._index
            acc_single_qubit_error += properties.gate_error(gate="x", qubits=index)
            single_qubit_gate_count += 1
        elif instruction.operation.num_qubits == 2:
            pair = [instruction.qubits[0]._index, instruction.qubits[1]._index]
            acc_two_qubit_error += properties.gate_error(gate=two_qubit_gate, qubits=pair)
            two_qubit_gate_count += 1
    acc_total_error = acc_two_qubit_error + acc_single_qubit_error + acc_readout_error
    backend = [
        acc_total_error,
        acc_two_qubit_error,
        acc_single_qubit_error,
        acc_readout_error,
        single_qubit_gate_count,
        two_qubit_gate_count,
    ]
    return backend


@typechecked
def grade_lab2_ex3(
    results_list: list, backend_list: list, circuit_list: list
) -> None:
    prepared_backends=[]
    for result, backend, circuit in zip(results_list, backend_list, circuit_list):
        prepared_backend = prepare_backend(backend, circuit)
        prepared_backends.append(prepared_backend)

    grade({
        'results_list': results_list,
        'prepared_backends': prepared_backends,
    }, 'lab2-ex3', _challenge_id)


#TODO obscuse
def find_paths_with_weight_sum_below_threshold(
    graph, threshold, two_qubit_ops_list, logical_pair_list
):
    valid_paths = []
    valid_weights = []
    for start_node in range(graph.num_nodes()):
        paths = [[start_node]]
        weights = [0]
        for i in range(len(two_qubit_ops_list)):
            new_paths = []
            new_weights = []
            for path, weight in zip(paths, weights):
                if logical_pair_list[i][0] < logical_pair_list[i][1]:
                    important_node = path[
                        logical_pair_list[i][0]
                    ]  # we know the structure is 10, 02, 30 and 14
                    for neighbor in graph.neighbors(important_node):
                        if neighbor not in path and graph.has_edge(important_node, neighbor):
                            edge_weight = (
                                graph.get_edge_data(important_node, neighbor)
                                * two_qubit_ops_list[i]
                            )  # we multiply by the number of times each two-qubit gate is applied
                            new_paths.append(path + [neighbor])
                            new_weights.append(weight + edge_weight)

                else:
                    important_node = path[logical_pair_list[i][1]]
                    for neighbor in graph.neighbors_undirected(important_node):
                        if neighbor not in path and graph.has_edge(neighbor, important_node):
                            edge_weight = (
                                graph.get_edge_data(neighbor, important_node)
                                * two_qubit_ops_list[i]
                            )  # we multiply by the number of times each two-qubit gate is applied
                            new_paths.append(path + [neighbor])
                            new_weights.append(weight + edge_weight)
            paths = new_paths
            weights = new_weights
        # Check which paths are valid
        for path, weight in zip(paths, weights):
            if weight < threshold:
                valid_paths.append(path)
                valid_weights.append(weight)
    return valid_paths, valid_weights


@typechecked
def grade_lab2_ex4(
    valid_paths: list, valid_weights: list, graph: rustworkx.PyDiGraph, threshold: float, two_qubit_ops_list: list, logical_pair_list: list) -> None:
    
    prepa, prepb = find_paths_with_weight_sum_below_threshold(
        graph, threshold, two_qubit_ops_list, logical_pair_list
    )

    grade({
        'valid_paths': valid_paths,
        'valid_weights': valid_weights,
        'prepa': prepa,
        'prepb': prepb,
    }, 'lab2-ex4', _challenge_id)


#TODO obscuse
@typechecked
def grade_lab2_ex5(
    best_seed_transpiler: int, min_err_acc_seed: float, circuit_trivial: QuantumCircuit, noisy_backend, two_qubit_gate_errors_per_circuit_layout: callable
) -> None:
    
    #TODO obfuscate
    def prepare_submission(circuit, backend):
        min_err_acc_seed = 1
        for seed_transpiler in range(0, 1000):
            pm = generate_preset_pass_manager(
                backend=backend,
                optimization_level=3,
                seed_transpiler=seed_transpiler,
                layout_method="sabre",
            )
            circuit_opt_seed = pm.run(circuit)
            acc_total_error_seed, *_ = two_qubit_gate_errors_per_circuit_layout(
                circuit_opt_seed, backend
            )

            if min_err_acc_seed > acc_total_error_seed:
                min_err_acc_seed = acc_total_error_seed
                best_seed_transpiler = seed_transpiler
        return best_seed_transpiler, min_err_acc_seed

    prepa, prepb = prepare_submission(circuit_trivial, noisy_backend)

    grade({
        'best_seed_transpiler': best_seed_transpiler,
        'min_err_acc_seed': min_err_acc_seed,
        'prepa': prepa,
        'prepb': prepb,
    }, 'lab2-ex5', _challenge_id)


@typechecked
def grade_lab2_ex6a(
    fold_circuit: callable
) -> None:
    
    circuit = QuantumVolume(5)
    folded_circuit = fold_circuit(circuit, scale_factor=5)

    grade({
        'folded_circuit_ops': folded_circuit.count_ops()
    }, 'lab2-ex6a', _challenge_id)


@typechecked
def grade_lab2_ex6b(
    fold_circuit: callable
) -> None:
    
    circuit = QuantumVolume(5)
    pm = generate_preset_pass_manager(optimization_level=2, backend=FakeBrisbane())
    transpiled_circuit = pm.run(circuit)
    folded_circuit = fold_circuit(transpiled_circuit, scale_factor=5)

    grade({
        'transpiled_circuit_ops': transpiled_circuit.count_ops(),
        'folded_circuit_ops': folded_circuit.count_ops()
    }, 'lab2-ex6b', _challenge_id)


@typechecked
def grade_lab2_ex7(
    basic_zne: callable
) -> None:
    
    max_cut_paulis = [
        ('IIIZZ', 1),
        ('IIIZZ', 1),
        ('IIZIZ', 1),
        ('IIZIZ', 1),
        ('IZIIZ', 1),
        ('IZIIZ', 1),
        ('ZIIIZ', 1),
        ('ZIIIZ', 1),
        ('IIZZI', 1),
        ('IIZZI', 1),
        ('IZIZI', 1),
        ('IZIZI', 1),
        ('ZIIZI', 1),
        ('ZIIZI', 1),
        ('IZZII', 1),
        ('IZZII', 1),
        ('ZIZII', 1),
        ('ZIZII', 1),
        ('ZZIII', 1)
    ]
    cost_hamiltonian = SparsePauliOp.from_list(max_cut_paulis)
    circuit = QAOAAnsatz(cost_operator=cost_hamiltonian, reps=2)
    backend = GenericBackendV2(5, seed=43)
    pm = generate_preset_pass_manager(optimization_level=2, backend=backend)
    isa_circuit = pm.run(circuit)
    xdata, exp_vals, pub = basic_zne(
        isa_circuit, 
        [5], 
        backend, 
        [0.90328799, 1.1925605 , 0.02658611, 0.94133493], 
        cost_hamiltonian
    )

    folded_circuit = pub[0]
    observables = pub[1]
    parameters = pub[2]

    grade({
        'transpiled_circuit_ops': isa_circuit.count_ops(),
        'folded_circuit_ops': folded_circuit.count_ops(),
        'observables': observables,
        'parameters': parameters,
    }, 'lab2-ex7', _challenge_id)

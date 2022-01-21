import converter

def get_intermediate_list(circuit):
    """Get gate list and the number of qubit from qulacs circuit.

    Args:
        circuit : qulacs.QuantumCircuit
            Quantum circuit of the object to be converted

    Returns:
        gate_list : list
            [[gate name, target index],...]

        nqubit : int
            The number of qubit.

    """
    gate_list = []
    for i in range(circuit.get_gate_count()):
        gate = circuit.get_gate(i)
        if gate.get_name() in ["X-rotation", "Y-rotation", "Z-rotation"]:
            gate_list.append([gate.get_name(), gate.get_target_index_list()[0], gate.get_angle()])
        elif gate.get_name() == "SWAP":
            gate_list.append([gate.get_name(), gate.get_target_index_list()])
        elif len(gate.get_control_index_list())==0:
            gate_list.append([gate.get_name(), gate.get_target_index_list()[0]])
        elif len(gate.get_control_index_list())==1:
            gate_list.append([gate.get_name(), [gate.get_target_index_list()[0], gate.get_control_index_list()[0]]])
        else:
            gate_list.append([gate.get_name(), [*gate.get_target_index_list(), *gate.get_control_index_list()]])
        nqubit = circuit.get_qubit_count()
    return gate_list, nqubit

def get_qiskit_circuit(circuit):
    """Get the circuit for qiskit from qulacs circuit

    Args:
        circuit : qulacs.QuantumCircuit
            Quantum circuit of the object to be drawn

    Returns:
        circuit : qiskit.circuit.quantumcircuit.QuantumCircuit
            Quantum circuit of the object to be drawn
    """
    gate_list, nqubit = get_intermediate_list(circuit)
    circuit_qiskit = converter.convert(gate_list, nqubit)
    return circuit_qiskit

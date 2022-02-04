import qulacs 
import qiskit

qulacs_dict = {
    "id":         [qulacs.gate.I,       0],
    "x":          [qulacs.gate.X,       0],
    "y":          [qulacs.gate.Y,       0],
    "z":          [qulacs.gate.Z,       0],
    "h":          [qulacs.gate.H,       0],
    "s":          [qulacs.gate.S,       0],
    "sdg":        [qulacs.gate.Sdag,    0],
    "t":          [qulacs.gate.T,       0],
    "tdg":        [qulacs.gate.Tdag,    0],
    "cx":         [qulacs.gate.CNOT,    0],
    "cz":         [qulacs.gate.CZ,      0],
    "rx":         [qulacs.gate.RX,      1],
    "ry":         [qulacs.gate.RY,      1],
    "rz":         [qulacs.gate.RZ,      1],
    "u2":         [qulacs.gate.U2,      0],      # u2 gate
    "u":          [qulacs.gate.U3,      0],      # u3 gate
    "swap":       [qulacs.gate.SWAP,    0],
}

class QiskitConverter:
    def __init__(self, circuit: qiskit.QuantumCircuit, convert_type='qulacs'):
        self.convert_type = convert_type
        self.qubit_count = circuit.num_qubits

        convert_dict = {
                'qulacs': [qulacs_dict, self.qiskit_convert],
        }
        self.dict = convert_dict[self.convert_type][0]
        self.func = convert_dict[self.convert_type][1]
        self.circuit = circuit

    def convert(self):
        return self.func()

    def qiskit_convert(self):
        qulacs_circuit = qulacs.QuantumCircuit(self.qubit_count)
        for i in range(self.circuit.get_gate_count()):
            gate = self.circuit.get_gate(i)
            parse = self.dict.get(gate.get_name())
            if parse is None:
                print("Warning: "+ gate.get_name() + " is unsupported yet.")
                continue
            qulacs_gate = parse[0]
            target = gate.get_target_index_list()
            control = gate.get_control_index_list()
            if parse[1] == 0:
                qulacs_circuit.append(qulacs_gate(), control + target, [])
            elif parse[1] == 1:
                angle = gate.get_angle()
                qulacs_circuit.append(qulacs_gate(angle), control + target, [])

        return qulacs_circuit

import qulacs 
import qiskit
import braket

qiskit_dict = {
    "I":          [qiskit.circuit.library.standard_gates.IGate,    0],
    "X":          [qiskit.circuit.library.standard_gates.XGate,    0],
    "Y":          [qiskit.circuit.library.standard_gates.YGate,    0],
    "Z":          [qiskit.circuit.library.standard_gates.ZGate,    0],
    "H":          [qiskit.circuit.library.standard_gates.HGate,    0],
    "S":          [qiskit.circuit.library.standard_gates.SGate,    0],
    "Sdag":       [qiskit.circuit.library.standard_gates.SdgGate,  0],
    "T":          [qiskit.circuit.library.standard_gates.TGate,    0],
    "Tdag":       [qiskit.circuit.library.standard_gates.TdgGate,  0],
    "CNOT":       [qiskit.circuit.library.standard_gates.CXGate,   0],
    "CZ":         [qiskit.circuit.library.standard_gates.CZGate,   0],
    "X-rotation": [qiskit.circuit.library.standard_gates.RXGate,   1],
    "Y-rotation": [qiskit.circuit.library.standard_gates.RYGate,   1],
    "Z-rotation": [qiskit.circuit.library.standard_gates.RZGate,   1],
    "U2":         [qiskit.circuit.library.standard_gates.U2Gate,   0],
    "U3":         [qiskit.circuit.library.standard_gates.U3Gate,   0],
    "SWAP":       [qiskit.circuit.library.standard_gates.SwapGate, 0],
    "sqrtX":      [qiskit.circuit.library.standard_gates.SXGate,   0],
    "sqrtXdag":   [qiskit.circuit.library.standard_gates.SXdgGate, 0],
}

braket_dict = {
    "I":           [braket.circuits.gates.I,       0],
    "X":           [braket.circuits.gates.X,       0],
    "Y":           [braket.circuits.gates.Y,       0],
    "Z":           [braket.circuits.gates.Z,       0],
    "H":           [braket.circuits.gates.H,       0],
    "S":           [braket.circuits.gates.S,       0],
    "Sdag":        [braket.circuits.gates.Si,      0],
    "T":           [braket.circuits.gates.T,       0],
    "Tdag":        [braket.circuits.gates.Ti,      0],
    "CNOT":        [braket.circuits.gates.CNot,    0],
    "SWAP":        [braket.circuits.gates.Swap,    0],
    "CZ":          [braket.circuits.gates.CZ,      0],
    "X-rotation":  [braket.circuits.gates.Rx,      1],
    "Y-rotation":  [braket.circuits.gates.Ry,      1],
    "Z-rotation":  [braket.circuits.gates.Rz,      1],
    "DenseMatrix": [braket.circuits.gates.Unitary, 2],
}

class QulacsConverter:
    def __init__(self, circuit: qulacs.QuantumCircuit, convert_type='qiskit'):
        self.convert_type = convert_type
        self.qubit_count = circuit.get_qubit_count()

        convert_dict = {
                'qiskit': [qiskit_dict, self.qiskit_convert],
                'braket': [braket_dict, self.braket_convert],
        }
        self.dict = convert_dict[self.convert_type][0]
        self.func = convert_dict[self.convert_type][1]
        self.circuit = circuit

    def convert(self):
        return self.func()

    def qiskit_convert(self):
        qiskit_circuit = qiskit.QuantumCircuit(self.qubit_count)
        for i in range(self.circuit.get_gate_count()):
            gate = self.circuit.get_gate(i)
            parse = self.dict.get(gate.get_name())
            if parse is None:
                print("Warning: "+ gate.get_name() + " is unsupported yet.")
                continue
            qiskit_gate = parse[0]
            target = gate.get_target_index_list()
            control = gate.get_control_index_list()
            if parse[1] == 0:
                qiskit_circuit.append(qiskit_gate(), control + target, [])
            elif parse[1] == 1:
                angle = gate.get_angle()
                qiskit_circuit.append(qiskit_gate(angle), control + target, [])

        return qiskit_circuit

    def braket_convert(self):
        braket_circuit = braket.circuits.Circuit()
        for i in range(self.circuit.get_gate_count()):
            gate = self.circuit.get_gate(i)
            parse = self.dict.get(gate.get_name())
            if parse is None:
                parse = self.dict.get("DenseMatrix")
            braket_gate = parse[0]
            target = gate.get_target_index_list()
            control = gate.get_control_index_list()
            if parse[1] == 0:
                instr = braket.circuits.Instruction(braket_gate(), control+target)
                braket_circuit.add(instr)
            elif parse[1] == 1:
                angle = gate.get_angle()
                instr = braket.circuits.Instruction(braket_gate(angle), target)
                braket_circuit.add(instr)
            elif parse[1] == 2:
                matrix=gate.get_matrix()
                instr = braket.circuits.Instruction(braket_gate(matrix=matrix, display_name=gate.get_name()), target)
                braket_circuit.add(instr)

        return braket_circuit

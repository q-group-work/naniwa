import qulacs
import braket
from braket.circuits import Circuit

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

class QulacsConverter_2_Braket:
    def __init__(self, circuit: qulacs.QuantumCircuit, convert_type='braket'):
        self.convert_type = convert_type
        self.qubit_count = circuit.get_qubit_count()

        convert_dict = {
                'braket': [braket_dict, self.braket_convert],
        }
        self.dict = convert_dict[self.convert_type][0]
        self.func = convert_dict[self.convert_type][1]
        self.circuit = circuit

    def convert(self):
        return self.func()

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

    def draw(self):
        print(self.circ)

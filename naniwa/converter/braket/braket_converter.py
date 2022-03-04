import qulacs 
from braket.circuits import Circuit

class QulacsConverter_2_Braket:
    def __init__(self, circuit: qulacs.QuantumCircuit, convert_type='braket'):
        self.convert_type = convert_type
        self.qubit_count = circuit.get_qubit_count()
        self.circ = Circuit()
        self.braket_dict = {
            "I":           [self.circ.i,       0],
            "X":           [self.circ.x,       0],
            "Y":           [self.circ.y,       0],
            "Z":           [self.circ.z,       0],
            "H":           [self.circ.h,       0],
            "S":           [self.circ.s,       0],
            "T":           [self.circ.t,       0],
            "CNOT":        [self.circ.cnot,    0],
            "SWAP":        [self.circ.swap,    0],
            "CZ":          [self.circ.cz,      0],
            "X-rotation":  [self.circ.rx,      1],
            "Y-rotation":  [self.circ.ry,      1],
            "Z-rotation":  [self.circ.rz,      1],
            "DenseMatrix": [self.circ.unitary, 2],
        }

        convert_dict = {
                'braket': [self.braket_dict, self.braket_convert],
        }
        self.dict = convert_dict[self.convert_type][0]
        self.func = convert_dict[self.convert_type][1]
        self.circuit = circuit

    def convert(self):
        return self.func()

    def braket_convert(self):
        braket_circuit = Circuit()
        for i in range(self.circuit.get_gate_count()):
            gate = self.circuit.get_gate(i)
            parse = self.dict.get(gate.get_name())
            if parse is None:
                parse = self.dict.get("DenseMatrix")
            braket_gate = parse[0]
            target = gate.get_target_index_list()
            control = gate.get_control_index_list()
            if parse[1] == 0:
                braket_gate(*control, *target)
            elif parse[1] == 1:
                angle = gate.get_angle()
                braket_gate(*target, angle)
            elif parse[1] == 2:
                matrix=gate.get_matrix()
                braket_gate(matrix=matrix, targets=target)

        return self.circ

    def draw(self):
        print(self.circ)

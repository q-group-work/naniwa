import qulacs 
import qiskit
from qiskit.circuit import Parameter

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

class QulacsConverter:
    def __init__(self, circuit: qulacs.QuantumCircuit, convert_type='qiskit'):
        self.convert_type = convert_type
        self.qubit_count = circuit.get_qubit_count()

        convert_dict = {
                'qiskit': [qiskit_dict, self.qiskit_convert],
        }
        self.dict = convert_dict[self.convert_type][0]
        self.func = convert_dict[self.convert_type][1]
        self.circuit = circuit

    def convert(self):
        return self.func()

    def qiskit_convert(self,  parameterized=False):
        qiskit_circuit = qiskit.QuantumCircuit(self.qubit_count)
        num=0
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
                if parameterized:
                    theta = Parameter('θ{}'.format(num))
                    num+=1
                    qiskit_circuit.append(qiskit_gate(theta), control + target, [])
                else:
                    angle = gate.get_angle()
                    qiskit_circuit.append(qiskit_gate(angle), control + target, [])

        return qiskit_circuit

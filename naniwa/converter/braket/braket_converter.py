import qulacs 
from braket.circuits import Circuit, Gate, Observable

"""
1-qubit gate:0
2-qubit gate(angleなし):1
1-qubit rotation gatec(angle 1つ):2
u2 gate:3
u3 gate:4
"""
qulacs_dict = {
    "I":         [qulacs.gate.Identity,     0],
    "X":         [qulacs.gate.X,            0],
    "Y":         [qulacs.gate.Y,            0],
    "Z":         [qulacs.gate.Z,            0],
    "H":         [qulacs.gate.H,            0],
    "S":         [qulacs.gate.S,            0],
    "Si":        [qulacs.gate.Sdag,         0],
    "T":         [qulacs.gate.T,            0],
    "Ti":        [qulacs.gate.Tdag,         0],
    "V" :        [qulacs.gate.sqrtX,        0],
    "Vi" :       [qulacs.gate.sqrtXdag,     0],
    "CNot":      [qulacs.gate.CNOT,         1],
    "CZ":        [qulacs.gate.CZ,           1],
    "Rx":        [qulacs.gate.RX,           2],
    "Ry":        [qulacs.gate.RY,           2],
    "Rz":        [qulacs.gate.RZ,           2],
    "Swap":      [qulacs.gate.SWAP,         1],
}

class BraketConverter:
    def __init__(self, circuit: Circuit, convert_type='qulacs'):
        self.convert_type = convert_type
        self.qubit_count = circuit.qubit_count
        self.instructions = circuit.instructions
        self.gate_count = len(self.instructions)     # gate数を力技でcircuit.dataのlengthから出しているが、他にいい方法があれば教えてください

        convert_dict = {
                'qulacs': [qulacs_dict, self.qulacs_convert],
        }
        self.dict = convert_dict[self.convert_type][0]
        self.func = convert_dict[self.convert_type][1]
        # self.circuit = circuit

    def convert(self):
        return self.func()

    def qulacs_convert(self):
        qulacs_circuit = qulacs.QuantumCircuit(self.qubit_count)
        for i, instr in enumerate(self.instructions):     #要変更
            
            parse = self.dict.get(instr.operator.name)           
            if parse is None:
                print("Warning: "+ instr.operator.name + " is unsupported yet.")  
                continue
            qulacs_gate = parse[0]
            qubit_index_list = [int(qubit) for qubit in instr.target] # 要変更
            if parse[1] == 0:
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0]))
            elif parse[1] == 1:
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0], qubit_index_list[1]))
            elif parse[1] == 2:
                angle_list = instr.operator.angle
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0], angle_list[0]))

        return qulacs_circuit

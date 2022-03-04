import qulacs 
import qiskit

"""
1-qubit gate:0
2-qubit gate(angleなし):1
1-qubit rotation gatec(angle 1つ):2
u2 gate:3
u3 gate:4
"""
qulacs_dict = {
    "id":         [qulacs.gate.Identity,     0],
    "x":          [qulacs.gate.X,            0],
    "y":          [qulacs.gate.Y,            0],
    "z":          [qulacs.gate.Z,            0],
    "h":          [qulacs.gate.H,            0],
    "s":          [qulacs.gate.S,            0],
    "sdg":        [qulacs.gate.Sdag,         0],
    "t":          [qulacs.gate.T,            0],
    "tdg":        [qulacs.gate.Tdag,         0],
    "cx":         [qulacs.gate.CNOT,         1],
    "cz":         [qulacs.gate.CZ,           1],
    "rx":         [qulacs.gate.RX,           2],
    "ry":         [qulacs.gate.RY,           2],
    "rz":         [qulacs.gate.RZ,           2],
    "u2":         [qulacs.gate.U2,           3],      # u2 gate
    "u":          [qulacs.gate.U3,           4],      # u3 gate
    "swap":       [qulacs.gate.SWAP,         1],
}

class QiskitConverter:
    def __init__(self, circuit: qiskit.QuantumCircuit, convert_type='qulacs'):
        self.convert_type = convert_type
        self.qubit_count = circuit.num_qubits
        self.gate_datas = circuit.data
        self.gate_count = len(self.gate_datas)     # gate数を力技でcircuit.dataのlengthから出しているが、他にいい方法があれば教えてください

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
        for i, gate_data in enumerate(self.gate_datas):
            # gate_data = self.circuit.data[i]
            parse = self.dict.get(gate_data[0].name)
            if parse is None:
                print("Warning: "+ gate_data[0].name + " is unsupported yet.")
                continue
            qulacs_gate = parse[0]
            qubit_index_list = [qubit.index for qubit in gate_data[1]] 
            if parse[1] == 0:
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0]))
            elif parse[1] == 1:
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0], qubit_index_list[1]))
            elif parse[1] == 2:
                angle_list = gate_data[0].params
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0], angle_list[0]))
            elif parse[1] == 3:
                angle_list = gate_data[0].params
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0], angle_list[0],  angle_list[1]))
            elif parse[1] == 4:
                angle_list = gate_data[0].params
                qulacs_circuit.add_gate(qulacs_gate(qubit_index_list[0], angle_list[0],  angle_list[1], angle_list[2]))


        return qulacs_circuit

from braket.circuits import Circuit

class Braket:
    def __init__(self):
        self.circ = Circuit()
        self.gate_one = {"I", "X", "Y", "Z", "H", "S", "Sdag", "T", "Tdag", "sqrtX", "sqrtXdag"}
        self.gate_one_rotation = {"X-rotation", "Y-rotation", "Z-rotation"}

        self.gate_two = {"CNOT", "CZ"} # control, target
        self.gate_two_target_only = {"SWAP"} # target, target

        self.gate_any = {"DenseMatrix"}

    def get_angle(self):
        return 0
    
    def append(self, gate):
        parsing_dict = {
            "I": self.circ.i,
            "X": self.circ.x,
            "Y": self.circ.y,
            "Z": self.circ.z,
            "H": self.circ.h,

            "S": self.circ.s,
            "T": self.circ.t,

            "X-rotation": self.circ.rx,
            "Y-rotation": self.circ.ry,
            "Z-rotation": self.circ.rz,

            "CNOT": self.circ.cnot,
            "SWAP": self.circ.swap,
            "CZ": self.circ.cz,

            "DenseMatrix": self.circ.unitary,
        }

        gate_name = gate.get_name()
        if gate_name in self.gate_one:
            parsing_dict[gate_name](gate.get_target_index_list()[0])
        elif gate_name in self.gate_one_rotation:
            parsing_dict[gate_name](gate.get_target_index_list()[0], self.get_angle())
        elif gate_name in self.gate_two:
            parsing_dict[gate_name](gate.get_control_index_list()[0], gate.get_target_index_list()[0])
        elif gate_name in self.gate_two_target_only:
            parsing_dict[gate_name](*gate.get_target_index_list())
        elif gate_name in self.gate_any:
            parsing_dict[gate_name](matrix=gate.get_matrix(), targets=gate.get_target_index_list())
        else:
            print("Warning: "+ gate_name + " is unsupported yet.")
            print("Please represent the circuit by using supported gates, if you use .draw()")

    def parsing(self, qulacs_circuit):
        self.circ = Circuit()
        for i in range(qulacs_circuit.get_gate_count()):
            gate = qulacs_circuit.get_gate(i)
            self.append(gate)

    def draw(self):
        print(self.circ)

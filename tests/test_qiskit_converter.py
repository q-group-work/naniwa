import pytest
from naniwa import QiskitConverter
from qiskit import QuantumCircuit
from qulacs import QuantumCircuit as qulacsQuantumCircuit
from qulacs.gate import Identity, X, Y, Z, H, S, Sdag, T, Tdag, CNOT, CZ, RX, RY, RZ, Pauli, PauliRotation, DenseMatrix


import math
import qulacs

def test_qiskit_converter():
    circuit = QuantumCircuit(2, 2)
    
    circuit.h(0)
    circuit.id(0)
    circuit.x(0)
    circuit.y(0)
    circuit.z(0)
    circuit.s(0)
    circuit.sdg(0)
    circuit.t(0)
    circuit.tdg(0)
    circuit.rx(math.pi/2,0)
    circuit.ry(math.pi/2,0)
    circuit.rz(math.pi/2,0)
    circuit.cx(0,1)
    circuit.cz(0,1)

    con = QiskitConverter(circuit)
    converted_circuit = con.convert()

    qulacs_circuit = qulacsQuantumCircuit(2)
    qulacs_circuit.add_gate(H(0))
    qulacs_circuit.add_gate(Identity(0))
    qulacs_circuit.add_gate(X(0))
    qulacs_circuit.add_gate(Y(0))
    qulacs_circuit.add_gate(Z(0))
    qulacs_circuit.add_gate(S(0))
    qulacs_circuit.add_gate(Sdag(0))
    qulacs_circuit.add_gate(T(0))
    qulacs_circuit.add_gate(Tdag(0))
    qulacs_circuit.add_gate(RX(0,math.pi/2))
    qulacs_circuit.add_gate(RY(0,math.pi/2))
    qulacs_circuit.add_gate(RZ(0,math.pi/2))
    qulacs_circuit.add_gate(CNOT(0,1))
    qulacs_circuit.add_gate(CZ(0,1))

    converted_gates = [converted_circuit.get_gate(i).get_name() for i in range(converted_circuit.get_gate_count())]
    qulacs_gates = [qulacs_circuit.get_gate(i).get_name() for i in range(qulacs_circuit.get_gate_count())]


    assert converted_gates == qulacs_gates
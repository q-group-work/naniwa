import pytest
from naniwa.converter.qiskit.qiskit_converter import QiskitConverter
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
    qulacs_circuit.add_H_gate(0)
    qulacs_circuit.add_Identity_gate(0)
    qulacs_circuit.add_X_gate(0)
    qulacs_circuit.add_Y_gate(0)
    qulacs_circuit.add_Z_gate(0)
    qulacs_circuit.add_S_gate(0)
    qulacs_circuit.add_Sdag_gate(0)
    qulacs_circuit.add_T_gate(0)
    qulacs_circuit.add_Tdag_gate(0)
    qulacs_circuit.add_gate(RX(0,math.pi/2))
    qulacs_circuit.add_gate(RY(0,math.pi/2))
    qulacs_circuit.add_gate(RZ(0,math.pi/2))
    qulacs_circuit.add_gate(CNOT(0,1))
    qulacs_circuit.add_gate(CZ(0,1))


    assert converted_circuit == qulacs_circuit
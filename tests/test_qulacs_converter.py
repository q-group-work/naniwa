import pytest
from naniwa import QulacsConverter
from qiskit import QuantumCircuit as qiskitQuantumCircuit
from qulacs import QuantumCircuit
from qulacs.gate import Identity, X, Y, Z, H, S, Sdag, T, Tdag, CNOT, CZ, RX, RY, RZ, Pauli, PauliRotation, DenseMatrix


import math
import qulacs

def test_qiskit_converter():

    circuit = QuantumCircuit(2)
    circuit.add_gate(H(0))
    circuit.add_gate(Identity(0))
    circuit.add_gate(X(0))
    circuit.add_gate(Y(0))
    circuit.add_gate(Z(0))
    circuit.add_gate(S(0))
    circuit.add_gate(Sdag(0))
    circuit.add_gate(T(0))
    circuit.add_gate(Tdag(0))
    circuit.add_gate(RX(0,math.pi/2))
    circuit.add_gate(RY(0,math.pi/2))
    circuit.add_gate(RZ(0,math.pi/2))
    circuit.add_gate(CNOT(0,1))
    circuit.add_gate(CZ(0,1))

    qiskit_circuit = qiskitQuantumCircuit(2)
    qiskit_circuit.h(0)
    qiskit_circuit.id(0)
    qiskit_circuit.x(0)
    qiskit_circuit.y(0)
    qiskit_circuit.z(0)
    qiskit_circuit.s(0)
    qiskit_circuit.sdg(0)
    qiskit_circuit.t(0)
    qiskit_circuit.tdg(0)
    qiskit_circuit.rx(math.pi/2,0)
    qiskit_circuit.ry(math.pi/2,0)
    qiskit_circuit.rz(math.pi/2,0)
    qiskit_circuit.cx(0,1)
    qiskit_circuit.cz(0,1)

    con = QulacsConverter(circuit)
    converted_circuit = con.convert()

    assert converted_circuit == qiskit_circuit

import pytest
from naniwa.converter.qulacs.qulacs_converter import QulacsConverter

import qiskit
import qulacs

def test_qulacs_converter():
    for i in range(6):
        circuit = qulacs.QuantumCircuit(6)
        circuit.add_X_gate(i)
        con = QulacsConverter(circuit)
        converted_circuit = con.convert()

        qiskit_circuit = qiskit.QuantumCircuit(6)
        qiskit_circuit.x(i)

        assert converted_circuit == qiskit_circuit

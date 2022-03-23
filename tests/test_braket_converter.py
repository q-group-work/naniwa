import pytest
from naniwa import BraketConverter


import qulacs
import braket

def test_braket_converter():
    circuit = braket.circuits.Circuit()
    for i in range(6):
        circuit.x(i)
        con = BraketConverter(circuit)
        converted_circuit = con.convert()

    qulacs_circuit = qulacs.QuantumCircuit(6)
    for i in range(6):
        qulacs_circuit.add_X_gate(i)

    converted_gates = [converted_circuit.get_gate(i).get_name() for i in range(converted_circuit.get_gate_count())]
    qulacs_gates = [qulacs_circuit.get_gate(i).get_name() for i in range(qulacs_circuit.get_gate_count())]


    assert converted_gates == qulacs_gates

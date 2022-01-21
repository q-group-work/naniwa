import qulacs
import qiskit

# gate_info = [ゲート Type, qubit_count]とcircitのqubit数をもらうと
# qiskitゲートを生成
def convert(gate_list, nqubit):
    qiskit_circ = qiskit.QuantumCircuit(nqubit)
    for gate_info in gate_list:
    # Pauliゲート
        if gate_info[0] == "X":
            qiskit_circ.x(gate_info[1])
        elif gate_info[0] == "Y":
            qiskit_circ.y(gate_info[1])
        elif gate_info[0] == "Z":
            qiskit_circ.z(gate_info[1])
        elif gate_info[0] == "I":
            qiskit_circ.id(gate_info[1])
        # クリフォードゲート
        elif gate_info[0] == "H":
            qiskit_circ.h(gate_info[1])
        elif gate_info[0] == "CNOT":
            qiskit_circ.cx(gate_info[1][0], gate_info[1][1])
        elif gate_info[0] == "CZ":
            qiskit_circ.cz(gate_info[1][0], gate_info[1][1])
        elif gate_info[0] == "S":
            qiskit_circ.s(gate_info[1])
        elif gate_info[0] == "Sdag":
            qiskit_circ.sdg(gate_info[1])
        # 回転ゲート
        elif gate_info[0] == "X-rotation":
            qiskit_circ.rx(gate_info[2], gate_info[1])
        elif gate_info[0] == "Y-rotation":
            qiskit_circ.ry(gate_info[2], gate_info[1])
        elif gate_info[0] == "Z-rotation":
            qiskit_circ.rz(gate_info[2], gate_info[1])
        # C3ゲート
        elif gate_info[0] == "T" :
            qiskit_circ.t(gate_info[1])
        elif gate_info[0] == "Tdag" :
            qiskit_circ.tdg(gate_info[1])
        # Uゲート
        elif gate_info[0] == "U3" :
            qiskit_circ.u(gate_info[2], gate_info[1])
        elif gate_info[0] == "U2" :
            qiskit_circ.u2(gate_info[2], gate_info[1])
        # Swapゲート
        elif gate_info[0] == "SWAP" :
            qiskit_circ.swap(gate_info[1][0], gate_info[1][1])

        elif gate_info[0] == "sqrtX" :
            qiskit_circ.sx(gate_info[1])
        elif gate_info[0] == "sqrtXdag" :
            qiskit_circ.sxdg(gate_info[1])
        
        else:
            print("Warning: "+ gate_info[0] + " is unsupported yet.")
            print("Please represent the circuit by using supported gates, if you use .draw()")
    return qiskit_circ

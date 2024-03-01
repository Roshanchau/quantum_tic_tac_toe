from qiskit import QuantumCircuit

def connected_qubits(circuit, qubit):
    """Find the qubits connected to a given qubit in a quantum circuit."""
    connected = set()

    for gate in circuit.data:
        if qubit in gate[1]:
            for q in gate[1]:
                if q != qubit:
                    connected.add(q.index)

    return connected

# Create a quantum circuit
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.h(1)

# Find the qubits connected to q1
print(connected_qubits(qc, qc.qubits[1]))

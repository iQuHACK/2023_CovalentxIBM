import covalent as ct
import pennylane as qml

def layer(x, params, wires, i0=0, inc=1):
    i = i0
    for j, wire in enumerate(wires):
        qml.Hadamard(wires=[wire])
        qml.RZ(x[i % len(x)], wires=[wire])
        i += inc
        qml.RY(params[0, j], wires=[wire])

    qml.broadcast(unitary=qml.CRZ, pattern="ring", wires=wires, parameters=params[1])

def ansatz(x, params, wires):
    for j, layer_params in enumerate(params):
        layer(x, layer_params, wires, i0=j * len(wires))

def adjoint_ansatz(ansatz):
    return qml.adjoint(ansatz)

def kernel_circuit(params):
    dev = qml.device(
        "default.qubit", wires=params.shape[2], shots=None
    )  # number of wires corresponds to the third dimension of params
    wires = dev.wires.tolist()

    @qml.qnode(dev)
    def circuit(x1, x2, params):
        ansatz(x1, params, wires=wires)
        adjoint_ansatz(ansatz)(x2, params, wires=wires)
        return qml.probs(wires=wires)

    return circuit

def kernel(x1, x2, params):
    return kernel_circuit(params)(x1, x2, params)[0]


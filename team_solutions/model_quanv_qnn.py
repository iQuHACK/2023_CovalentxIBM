import torch
import torch.nn as nn
import numpy as np
import pennylane as qml

torch.manual_seed(0)

n_qubits = 4
n_layers = 2
n_class = 3
n_features = 196
image_x_y_dim = 14
var_per_qubit = n_qubits
kernel_size = n_qubits 
stride = n_qubits

qnn_qubits = 8
qnn_layers = 3
assert qnn_qubits >= n_class

dev = qml.device("default.qubit", wires = n_qubits)
dev_qnn = qml.device("default.qubit", wires = qnn_qubits)

def circuit(inputs, weights):
    encoding_gates = ['RZ', 'RX']*int(var_per_qubit/2)
    for qub in range(n_qubits):
        qml.Hadamard(wires = qub)
        for i in range(var_per_qubit):
            if (qub * var_per_qubit + i) < len(inputs):
                exec('qml.{}({}, wires = {})'.format(encoding_gates[i], inputs[qub * var_per_qubit + i], qub))
            else: #load nothing
                pass

    for l in range(n_layers):
        for i in range(n_qubits):
            qml.CRZ(weights[l, i], wires = [i, (i + 1) % n_qubits])
            #qml.CNOT(wires = [i, (i + 1) % n_qubits])
        for j in range(n_qubits, 2 * n_qubits):
            qml.RY(weights[l, j], wires = j % n_qubits)

    _expectations = [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]
    return _expectations
    #return qml.expval(qml.PauliZ(0))

def qnn_circuit(inputs, weights):
    
    encoding_gates = ['RZ', 'RX'] * int(len(inputs)/2)
    var_per_qubit = int(len(inputs)/qnn_qubits) + 1
    for qub in range(qnn_qubits):
        qml.Hadamard(wires = qub)
        for i in range(var_per_qubit):
            if (qub * var_per_qubit + i) < len(inputs):
                exec('qml.{}({}, wires = {})'.format(encoding_gates[i], np.pi * inputs[qub * var_per_qubit + i], qub))
            else: #load nothing
                pass
    

    for l in range(qnn_layers):
        for i in range(qnn_qubits):
            qml.CRZ(weights[l, i], wires = [i, (i + 1) % qnn_qubits])
            #qml.CNOT(wires = [i, (i +n 1) % n_qubits])
        for j in range(qnn_qubits, 2 * qnn_qubits):
            qml.RY(weights[l, j], wires = j % qnn_qubits)

    _expectations = [qml.expval(qml.PauliZ(i)) for i in range(qnn_qubits)]
    return _expectations
    #return qml.expval(qml.PauliZ(0))


class Net(nn.Module):
    # define nn
    def __init__(self):
        super(Net, self).__init__()

        weight_shapes = {"weights": (n_layers, 2 * n_qubits)}
        qnode = qml.QNode(circuit, dev, interface = 'torch', diff_method = 'adjoint')
        self.ql1 = qml.qnn.TorchLayer(qnode, weight_shapes)
        
        qnn_weight_shapes = {"weights": (qnn_layers, 2 * qnn_qubits)}
        qnn_qnode = qml.QNode(qnn_circuit, dev_qnn, interface = 'torch', diff_method = 'adjoint')
        self.ql2 = qml.qnn.TorchLayer(qnn_qnode, qnn_weight_shapes)
        
        self.fc1 = nn.Linear(qnn_qubits, n_class)

    def forward(self, X):
        
        bs = X.shape[0]
        X = X.view(bs, image_x_y_dim, image_x_y_dim)
        XL = []
        
        for i in range(0, image_x_y_dim, stride):
            for j in range(0, image_x_y_dim, stride):
                XL.append(self.ql1(torch.flatten(X[:, i:i+kernel_size, j:j+kernel_size], start_dim = 1)))

        X = torch.cat(XL, dim = 1)
        X = self.ql2(X)
        X = self.fc1(X)
        return X

if __name__ == '__main__':
    network = Net()
    random_input = torch.rand(1, n_features)
    print(network(random_input))

import torch
import torch.nn as nn
import numpy as np
import pennylane as qml

torch.manual_seed(0)

n_qubits = 4
n_layers = 4
n_class = 3
n_features = 196
image_x_y_dim = 14
var_per_qubit = n_qubits
kernel_size = n_qubits 
stride = 4

dev = qml.device("default.qubit", wires = n_qubits)

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
        for j in range(n_qubits, 2*n_qubits):
            qml.RY(weights[l, j], wires = j % n_qubits)

    _expectations = [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]
    return _expectations
    #return qml.expval(qml.PauliZ(0))


class Net(nn.Module):
    # define nn
    def __init__(self):
        super(Net, self).__init__()

        weight_shapes = {"weights": (n_layers, 2 * n_qubits)}
        qnode = qml.QNode(circuit, dev, interface = 'torch', diff_method = 'adjoint')
        self.ql1 = qml.qnn.TorchLayer(qnode, weight_shapes)
        for p in self.ql1.parameters():
            p.requires_grad=False
        self.ql1.weights.data.uniform_(-np.pi, np.pi)

        self.fc1 = nn.Linear(64, n_class * 2)
        self.lr1 = nn.LeakyReLU(0.1)
        self.fc2 = nn.Linear(n_class * 2, n_class)

    def forward(self, X):
        
        bs = X.shape[0]
        X = X.view(bs, image_x_y_dim, image_x_y_dim)
        XL = []
        
        for i in range(0, image_x_y_dim, stride):
            for j in range(0, image_x_y_dim, stride):
                XL.append(self.ql1(torch.flatten(X[:, i:i+kernel_size, j:j+kernel_size], start_dim = 1)))

        X = torch.cat(XL, dim = 1)
        X = self.fc1(X)
        X = self.lr1(X)
        X = self.fc2(X)
        return X

if __name__ == '__main__':
    network = Net()
    random_input = torch.rand(1, n_features)
    print(network(random_input))

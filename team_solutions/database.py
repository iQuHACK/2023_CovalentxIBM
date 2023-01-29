import boto3
import covalent as ct
import uuid
import datetime

import numpy as np
import pandas as pd
# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, Aer, IBMQ, execute
from qiskit.visualization import *
from qiskit_ibm_runtime.program import UserMessenger
from scipy.optimize import dual_annealing
import statistics
from qiskit.compiler import transpile
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import Estimator, QiskitRuntimeService, Session

@ct.electron
def fetch_data(id):
	dynamodb = boto3.resource('dynamodb')

	table = dynamodb.Table('Work')

	response = table.get_item(Key={'id': id})

	scores = response['Item']['description']

	scores = scores.split(',')

	scores = [float(score) for score in scores]

	print(scores)

	return scores

@ct.electron
@ct.lattice
def predict_trouble(token, example, parameters = [0.8683269 , 0.39393166, 0.47681407, 0.30033276, 0.97830805, 0.52097628, 0.99194506, 0.92128744, 0.57695905, 0.36047569,0.83097868, 0.47035325]):
    qc = QuantumCircuit(3)
    embed_example(qc, example)
    apply_parameters(qc, parameters)
    evaluate_circuit(qc, token)
    result = run_circuit(qc, Aer.get_backend("aer_simulator"))
    return make_prediction(result)

@ct.electron(deps_pip=ct.DepsPip(["qiskit==0.40.0"]))
def evaluate_circuit(qc, token: str):
    QiskitRuntimeService.save_account(channel="ibm_quantum",
                                      token=token,
                                      instance="ibm-q-community/mit-hackathon/main",
                                      overwrite=True)

    with Session(service=QiskitRuntimeService(), backend="ibm_nairobi"):
        estimator = Estimator()
        return estimator.run(circuits=qc,
                             observables=[SparsePauliOp("IZ")],
                             shots=500).result()


def embed_example(circuit, example):
    circuit.rx(np.pi * example[0], 0)
    circuit.rx(np.pi * example[1], 1)
    circuit.rx(np.pi * example[2], 2)


def apply_parameters(circuit, parameters):
    # TODO: use full range
    layers = np.reshape(parameters, (int(len(parameters)/3), 3))
    layer_count = 1
    for layer in layers:
        for gate in range(len(layer)):
            if layer_count % 3 == 0:
                circuit.rx(np.pi * layer[gate], gate)
            elif layer_count % 3 == 1:
                circuit.ry(np.pi * layer[gate], gate)
            else:
                circuit.rz(np.pi * layer[gate], gate)
        circuit.cx(0,1)
        circuit.cx(1,2)
        circuit.cx(2,0)
        layer_count += 1
        circuit.barrier()
    circuit.measure_all()


def run_circuit(circuit, backend):
    num_shots = 500
    job = execute(circuit,
                  shots=num_shots,
                  backend=backend)

    # Return the measured counts
    return job.result().get_counts()


def make_prediction(result):
    count_0 = 0
    count_1 = 0
    for measurement in result:
        # Determine vote
        if measurement.count('1') > measurement.count('0'):
            count_1 += result[measurement]
        else:
            count0 += result[measurement]
    if count_1 > count_0:
        return 1
    else:
        return 0

@ct.electron
def upload_result(id, prediction):
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('Work')
    
    response = table.put_item(
        Item={
        'id': id,
        'description': prediction,
        }
    )

    print(response)


@ct.lattice
def workflow(power_line_id):
    example = fetch_data(power_line_id)
    result = predict_trouble(example)
    upload_result(power_line_id, result)
    
    return result


dispatch_id = ct.dispatch(workflow)("870cb0c5-6877-4c97-a0a0-188f57f444b9")
print(f"\n{dispatch_id}")

workflow_result = ct.get_result(dispatch_id, wait=True)
print(workflow_result.result)









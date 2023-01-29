from qiskit import (IBMQ, ClassicalRegister, QuantumCircuit, QuantumRegister,
                    execute)
from qiskit.tools.monitor import job_monitor


def qrng(n:int, api_token):
  IBMQ.enable_account(api_token)
  provider = IBMQ.get_provider(hub='ibm-q-community', group='mit-hackathon', project='main')
  
  q = QuantumRegister(16,'q')
  c = ClassicalRegister(16,'c')
  circuit = QuantumCircuit(q,c)
  circuit.h(q) # Applies hadamard gate to all qubits
  circuit.measure(q,c) # Measures all qubits 

  backend = provider.get_backend('ibmq_qasm_simulator')
  job = execute(circuit, backend, shots=1)

  print('Executing Job...\n')                 
  job_monitor(job)
  counts = job.result().get_counts()

  return counts

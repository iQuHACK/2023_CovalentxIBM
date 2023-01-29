import os

import covalent as ct
from qiskit import QuantumCircuit
from qiskit.compiler import transpile
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import Estimator, QiskitRuntimeService, Session, Sampler

from qiskit import IBMQ
token = "09428f6730538a20ee6382d16ca3461c758d0346cdd54071ff0ae8651f1f91c0fcac8bfdb998a7688ff6f751877cab2f038d33cbfd1b6e7dc1ec8cbcdfc72b95"
#IBMQ.save_account(token)
IBMQ.load_account() # Load account from disk
IBMQ.providers()    # List all available providers

def grover_function(s:str):

	import random
	from qiskit.quantum_info import Statevector

	#secret = random.randint(0,15)  # the owner is randomly picked
	#secret_string = format(secret, '04b')  # format the owner in 7-bit string
	secret_string = s
	oracle = Statevector.from_label(secret_string)  # let the oracle know the owner

	from qiskit.algorithms import AmplificationProblem

	problem = AmplificationProblem(oracle, is_good_state=secret_string)

	from qiskit.algorithms import Grover
	import math

	def grover(problem):
	    n = int(math.sqrt((len(s))))
	    grover = Grover(n)
	    circuit = grover.construct_circuit(problem)
	    circuit.measure_all() #NOTE THIS, REMOVED MEASUREALL BC OF OBSERVABLES, WILL SEE IF IT WORKS
	    #grover_circuits.append(circuit)
	    return circuit
	    
	@ct.electron(deps_pip=ct.DepsPip(["qiskit==0.40.0"]))
	def evaluate_circuit(token: str, shots=100):
	    #QiskitRuntimeService.save_account(channel="ibm_quantum",
	    #                                  token=token,
	    #                                  instance="ibm-q-community/mit-hackathon/main",
	    #                                  overwrite=True)

	    #with Session(service=QiskitRuntimeService(channel="ibm_quantum"), backend="ibmq_qasm_simulator"):#ibm_nairobi
		#estimator = Estimator()
		#sampler = Sampler()
		#job = sampler.run(grover(problem))
		#return job
		#observables = (
	    	#SparsePauliOp("ZZZ"),
		#)
		#job = estimator.run(circuits=grover(problem),
		#                     observables=observables,
		#                     shots=shots).result()
		#return job
	    
	    with Session(service=QiskitRuntimeService(channel="ibm_quantum"), backend="ibmq_qasm_simulator"):
	    	sampler = Sampler()
	    	job = sampler.run(circuits=grover(problem), shots=shots)
	    	result = job.result()
	    	result_dict = result.quasi_dists[0].binary_probabilities()
	    	answer = max(result_dict, key=result_dict.get)
	    	return answer
	    	#return result
	    	#print(result)
		                     
	@ct.lattice
	def test(token):
		return evaluate_circuit(token)
		#job = evaluate_circuit(token)
		#return job
		#result = job.get_result()
		#return result
		#result_dict = result.quasi_dists[0].binary_probabilities()
		#answer = max(result_dict, key=result_dict.get)
		#return answer
		
	dispatch_id = ct.dispatch(test)(token)
	print(f"\n{dispatch_id}" + " - Running")

	workflow_result = ct.get_result(dispatch_id, wait=True)
	print("Result")
	print(workflow_result.result)

	#result_dict = workflow_result.quasi_dists[0].binary_probabilities()
	#answer = max(result_dict, key=result_dict.get)
	#print(answer)

	print("Secret String: " + secret_string)
	
	return workflow_result.result

#grover_function("1100")
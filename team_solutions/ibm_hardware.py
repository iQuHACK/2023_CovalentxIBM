import qiskit
from qiskit import *
from qiskit import IBMQ
from qiskit.compiler import assemble, transpile
from qiskit.providers.fake_provider import FakeNairobiV2
from qiskit.providers.ibmq.managed import IBMQJobManager

""" 
Get account/backend (REAL)
"""
#Token = User's ID
#IBMQ.enable_account(TOKEN, hub='ibm-q-community', group='mit-hackathon', project='main')
#provider = IBMQ.get_provider(hub='ibm-q-community', group='mit-hackathon', project='main')
#backend = provider.get_backend('ibm-q-community')

"""
Get account/backend (Fake)
"""

backend = FakeNairobiV2

"""
Retrieving Job
"""

#Jobs
circs = transpile([circuit], backend=backend)

job_manager = IBMQJobManager()
job_set = job_manager.run(circs, backend=backend, name='entangled-entities')

job_set_id = job_set.job_set_id()
retrieved_job_set = job_manager.retrieve_job_set(job_set_id=job_set_id, provider=provider)
print(retrieved_job_set.report())

import torch
import torch.nn as nn
import numpy as np


# goal: 7 by 7 parameter "weights" need to be adjusted to minimize loss defined by the square of the trace of the weight matrix

# sigmas

sigma0 = torch.tensor([[1., 0.],
                       [0., 1.]], dtype=torch.cfloat)

sigmax = torch.tensor([[0., 1.],
                       [1., 0.]], dtype=torch.cfloat)

sigmay = torch.tensor([[0., -1j],
                       [1j, 0.]], dtype=torch.cfloat)

sigmaz = torch.tensor([[1, 0.],
                       [0., -1]], dtype=torch.cfloat)

I = sigma0

X = torch.randn(4, 4, requires_grad=True, dtype=torch.cfloat)
H_F = torch.randn(X.shape)
H_I = torch.randn(X.shape)
l = .5


def Htheta(theta):
	return -np.cos(theta)*(torch.kron(sigmaz,sigma0)+torch.kron(sigma0,sigmaz)) -np.sin(theta)*(torch.kron(sigmax,sigma0)+torch.kron(sigma0,sigmax)) -3*torch.kron(sigmaz,sigmaz)


def dHtheta(theta):
	return np.sin(theta)*(torch.kron(sigmaz,sigma0)+torch.kron(sigma0,sigmaz)) -np.cos(theta)*(torch.kron(sigmax,sigma0)+torch.kron(sigma0,sigmax))


H = Htheta(np.pi/2)
dtH = dHtheta(np.pi/2)

def G(H_F, H_I, l, X):
	return H_F-H_I+1j*(X@(l*H_F+(1-l)*H_I)-(l*H_F+(1-l)*H_I)@X)

def G_test(H, dtH, X):
	return dtH+1j*(X@H-H@X)

def Cost(H_F, H_I, l, X):
	X = 0.5*(X+X.conj().T)
	return torch.trace(G(H_F, H_I, l, X)@G(H_F, H_I, l, X))

def Cost_test(H, X):
	X = 0.5*(X+X.conj().T)
	return torch.trace(G_test(H, dtH, X)@G_test(H, dtH, X))


def minimize(X):
	opt = torch.optim.Adam([X], lr=0.01)
	for t in range(10000):
		if t % 100 == 0:
			print(Cost(H_F, H_I, l, X))
		loss = abs(Cost(H_F, H_I, l, X))
		opt.zero_grad()
		loss.backward()
		opt.step()
	return X

def minimize_test(X):
	# opt = torch.optim.Adadelta([X],lr=0.001)
	opt = torch.optim.Adam([X],lr=0.001)
	for t in range(20_000):
		if t % 1000 == 0:
			print(Cost_test(H, X))
		if torch.abs(Cost_test(H, X)) < 4.0323e-13:
			break
		loss = Cost_test(H, X)
		#print(Cost_test(H, X_curr))
		loss = torch.abs(loss)
		opt.zero_grad()
		loss.backward()
		opt.step()
	return X


#print("Initial cost: "+ str(abs(Cost(H_F, H_I, l, X_input))))
#X_output = minimize(X_input)
#print("Final cost: "+ str(abs(Cost(H_F, H_I, l, X_output))))

print("Initial cost: "+ str(abs(Cost_test(H, X))))
X = minimize_test(X)
print("Final cost: "+ str(abs(Cost_test(H, X))))

print("Here is the final X: ")
result = 0.5*(X+X.conj().T)
result = result.detach().numpy()
print('real')
for row in result:
	for element in row:
		print(element.real,end='\t')
	print()
print('imag')
for row in result:
	for element in row:
		print(element.imag,end='\t')
	print()
print(repr(result))

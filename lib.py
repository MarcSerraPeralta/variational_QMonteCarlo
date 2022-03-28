from sympy import simplify, lambdify, conjugate, integrate, oo
import numpy as np

#######################################
#	   PROCESS INPUT PARAMETERS
#######################################

def get_E_local_f(H, psi_t, var):
	"""
	Returns the function local energy given a Hamiltonian an trial wave function. 

	Parameters
	----------
	H : sympy expression
		Hamiltonian of the system
	psi_t : sympy expression
		Trial wavefunction
	var : sympy symbols
		Variables for position r and for parameters alpha

	Returns
	-------
	E_local_f : function(r, alpha)
		Local energy function depending on r and alpha
	"""

	E_local_f = H/psi_t
	E_local_f = simplify(E_local_f)
	E_local_f = lambdify(var, E_local_f)

	return E_local_f


def get_prob_density(psi_t, var):
	"""
	Returns the probability density function for metropolis algorithm given a trial wave function. 

	Parameters
	----------
	psi_t : sympy expression
		Trial wavefunction
	var : sympy symbols
		Variables for position r and for parameters alpha

	Returns
	-------
	prob_density : function(r, alpha)
		Probability density function for the specified trial wave function
	"""

	prob_density = conjugate(psi_t)*psi_t
	prob_density = simplify(prob_density)
	prob_density = lambdify(var, prob_density)

	return prob_density


#######################################
#			   EXAMPLES
#######################################

def prob_density(r, alpha):
	"""
	Returns the value of the probability density function at the specified positions r and parameters alpha. 

	Parameters
	----------
	r : np.ndarray(N*dim)
		Positions of N electrons in the form: r1x, r1y, ..., r2x, r2y, ... 
	alpha : np.ndarray
		Parameters of the trial wave functon

	Returns
	-------
	prob : float
		Probability density function at the specified r and alpha
	"""

	prob = 0

	return prob


def E_local_f(r, alpha):
	"""
	Returns the value of the local energy at the specified positions r and parameters alpha. 

	Parameters
	----------
	r : np.ndarray(dim = N*space_dim)
		Positions of N electrons in the form: r1x, r1y, r1z, r2x, r2y, r2z, ...
	alpha : np.ndarray
		Parameters of the trial wave functon

	Returns
	-------
	E_local : float
		Local energy at the specified r and alpha
	"""

	E_local = 0

	return E_local


#######################################
#	    MONTE CARLO INTEGRATION
#######################################

def random_walker(prob_density, alpha, N_steps, dim, init_point, tm_sigma):
	"""
	Returns steps of a random walker that follows a Markov chain given a probability
	density function using the Metropolis algorithm. 

	Parameters
	----------
	prob_density : function(r, alpha)
		Probability density function depending on position r and parameters alpha
	alpha : np.ndarray
		Parameters of the trial wave functon
	N_steps : int
		Number of steps that the random walker takes
	dim: int
		Dimension of the configuration space, i.e. number of degrees of freedom in the system
	init_point: np.ndarray(dim)
		Starting point of the random walker
	tm_sigma: float
		Standard deviation that defines the trial move according to a normal distribution

	Returns
	-------
	steps : np.ndarray(N_steps, dim)
		Steps of the random walker
	"""

	steps = np.zeros([N_steps,dim])
	steps[0] = init_point
	curr_point = init_point
	for i in range(N_steps):
		next_point = np.random.normal(loc=curr_point,scale=tm_sigma)
		rate = prob_density(next_point,alpha)/prob_density(curr_point)
		if np.random.rand(1) <= rate:
			steps[i] = next_point
			curr_point = next_point
		else:
			steps[i] = curr_point
	
	return steps

def rand_init_point(system_size,dim):
	"""
	Returns a random initial point for the random walkers given a typical size of the system according to a normal distribution. 

	Parameters
	----------
	system_size: float
		Typical size of the system, e.g. fro teh Hydrogen atom it could be 2a_0
	dim: int
		Dimension of the configuration space, i.e. number of degrees of freedom in the system

	Returns
	init_point = np.ndarray(dim)
		Random initial point for the random walkers
	"""
	init_point = np.random.normal(scale=system_size, size = dim)

	return init_point

def find_optimal_tm_sigma(prob_density, alpha, dim, tm_sigma_init, Niter = 500, tol = 0.05):
	"NOT FINISHED: Find an optimal trial move sigma that provides an average acceptance ratio of 0.5 +-tol using the steepest descent method. "
	curr_point = np.zeros(dim)
	curr_tm_sigma = tm_sigma_init
	iter = 1
	total_rate, rate_av = 0, 0
	while iter<=Niter:
		for i in range(100): 
			next_point = np.random.normal(loc=curr_point,scale=curr_tm_sigma)
			rate = prob_density(next_point,alpha)/prob_density(curr_point)
			total_rate += rate
			if np.random.rand(1) <= rate:
				curr_point = next_point
		rate_av = total_rate/100

		if abs(rate_av - 0.5)>tol & (rate_av - 0.5)>0:
			curr_tm_sigma = 0
		elif abs(rate_av - 0.5)>tol & (rate_av - 0.5)<0:
			curr_tm_sigma = 0
		else:
			exit
		iter += 1
	return curr_tm_sigma





def MC_integration(E_local_f, prob_density, alpha, N_steps=5000, N_walkers=250, N_skip=0, L_start=1):
	"""
	Returns ... using Monte Carlo integration. 

	Parameters
	----------
	E_local_f : function(r, alpha)
		Local energy function depending on r and alpha
	prob_density : function(r, alpha)
		Probability density function depending on position r and parameters alpha
	alpha : np.ndarray
		Parameters of the trial wave functon
	N_steps : int
		Number of steps that the random walker takes
	N_walkers : int
		Number of random walkers
	N_skip : int
		Number of initial steps to skip for the integration
	L_start : float
		Length of the box in which the random walkers are initialized randomly

	Returns
	-------
	...
	"""

	return 


#######################################
#	     NUMERICAL OPTIMIZATION
#######################################

class Optimizer:
	"""
	Wrapper for numerical optimization of alpha.

	Initial Parameters
	------------------
	method : str
		Method for optimizing alpha
		Options: "scan", "steepest_descent"
	init_alpha : np.ndarray
		Initial values of alpha

	Functions
	---------
	update_alpha
		Updates alpha using the specified method and checks if the 
		optimization has converged (stored in Optimizer.converged)
	"""

	def __init__(self, opt_args):
		self.method = opt_args["method"]
		self.converged = False
		self.alpha = opt_args["init_alpha"]
		return

	def update_alpha(self, args):
		if self.method == "scan":
			self.alpha = scan_alpha(self.alpha, step)
			if True:
				self.converged = True

		elif self.method == "steepest_descent":
			self.alpha = steepest_descent(self.alpha, self.args)
			if True:
				self.converged = True

		else: 
			self.converged = True
		
		return


def scan_alpha(alpha_old, step):
	"""
	Returns the new value of alpha corresponding of doing an scan.

	Parameters
	----------
	alpha_new : np.ndarray
		Old value of alpha
	step : np.ndarray
		Steps for alpha

	Returns
	-------
	alpha_new : np.ndarray
		New value of alpha
	"""

	alpha_new = 0

	return alpha_new


def steepest_descent(alpha_old, args):
	"""
	Returns the new value of alpha using the method of steepest descent.

	Parameters
	----------
	alpha_new : np.ndarray
		Old value of alpha
	args : dict
		Information about the steepest descent method

	Returns
	-------
	alpha_new : np.ndarray
		New value of alpha
	"""

	alpha_new = 0

	return alpha_new


#######################################
#			  SAVE RESULTS
#######################################

def save(file_name, alpha_list, data_list):
	"""
	Saves alpha and data results to file_name.

	Parameters
	----------
	file_name : str
		Name of the file to store the results
	alpha_list : list of np.ndarray
		List of alpha values
	alpha_list : list of list
		List of data values

	Returns
	-------
	None
	"""

	return 
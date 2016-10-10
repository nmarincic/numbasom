from timeit import repeat
import numpy as np
from numbasom.numbasom import pairwise, pairwise_squared, som_calc, normalize
from numba import jit, autojit
import sys


def main(argv=None):
	if argv is None:
		argv = sys.argv
	#norm(argv[1])
	# test()
	test_som()
	#normalize(argv)
	
def test():
	# Define our test array
	X = np.random.random((500, 3))
	a = timefunc("classic python" , pairwise_squared, X)
	b = timefunc("numba squared (1 thread)" , autojit(pairwise_squared), X)
	print ("\nsolution 2 is %s times faster\n" %(a/b))

def test_som():
	som_size = (10,10)
	no_iterations = 5000
	data = np.random.randint(0,256, size = (50000,10))
	print ("SOM lattice size: %ix%i" %(som_size[0],som_size[1]))
	print ("Number of iterations: %i" %no_iterations)
	print ("Data dimensionality ",data.shape)
	#b = timefunc("SOM calculation (numba - 1 thread) lasted: " , som_calc, som_size, no_iterations, data)
	print (som_calc(som_size, no_iterations, data))


def timefunc(s, func, *args, **kwargs):
	"""
	Benchmark *func* and print out its runtime.
	"""
	# This aligns the text on the left
	print(s.ljust(20), end=" ")
	# This runs function once and stores the result in res
	res = func(*args, **kwargs)
	# time it (repeats the timeit process 'repeat' times, and runs each 'number' times)
	timing = min(repeat(lambda: func(*args, **kwargs),
						   number=5, repeat=2)) * 1000
	print('{:>6.4f} ms'.format(timing))    
	# this returns the result of the function
	#return res
	# this returns the timing
	return timing
	
def norm(file):
	vector = np.load(file)
	normalized = normalize(vector)
	np.save(file+"z", normalized)


if __name__ == '__main__':
	main()
from numba import jit
import numpy as np
import math
import collections
from timeit import default_timer as timer


@jit(nopython=True)
def normalize(data, min_val=0, max_val=1):
	no_vectors, dim = data.shape
	D = np.empty((no_vectors,dim), dtype=np.float64)
	inf = 1.7976931348623157e+308
	min_arr = np.empty(dim, dtype=np.float64)
	min_arr[:] = inf
	max_arr = np.empty(dim, dtype=np.float64)
	max_arr[:] = -inf
	diff = np.empty(dim, dtype=np.float64)

	for vec in range(no_vectors):
		for d in range(dim):
			val = data[vec,d]
			if val < min_arr[d]:
				min_arr[d] = val
			if val > max_arr[d]:
				max_arr[d] = val

	for d in range(dim):
		diff[d] = max_arr[d] - min_arr[d]
   
	for i in range(no_vectors):
		for j in range(dim):
			D[i,j] = (data[i, j] - min_arr[j]) / diff[j]
	return D

def normalize2(list):
    max_arr = np.max((list), axis=0)
    min_arr = np.min((list), axis=0)
    return (list - min_arr) / (max_arr - min_arr)

def pairwise(X):
	M = X.shape[0]
	N = X.shape[1]
	D = np.empty((M, M), dtype=np.float64)
	for i in range(M):
		for j in range(M):
			d = 0.0
			for k in range(N):
				tmp = X[i, k] - X[j, k]
				d += tmp * tmp
			D[i, j] = np.sqrt(d)
	return D

def pairwise_squared(X):
	M = X.shape[0]
	N = X.shape[1]
	# type will depend on the size of the matrix
	D = np.empty((M, M), dtype=np.uint32)
	for i in range(M):
		for j in range(M):
			d = 0.0
			for k in range(N):
				tmp = X[i, k] - X[j, k]
				d += tmp * tmp
			D[i, j] = d
	return D
   

@jit(nopython=True)
def random_lattice(som_size, dimensionality):
	X, Y, Z = som_size[0], som_size[1], dimensionality
	D = np.empty((X,Y,Z), dtype=np.float64)
	for x in range(X):
		for y in range(Y):
			for z in range(Z):
				D[x,y,z] = np.random.random()
	return D

	
@jit
def get_all_BMU_indexes(BMU, X, Y):
	BMUx, BMUy = BMU[0], BMU[1]
	BMU2x, BMU3x, BMU4x = BMU[0], BMU[0], BMU[0]
	BMU2y, BMU3y, BMU4y = BMU[1], BMU[1], BMU[1]
	
	if BMUx > X / 2:
		BMU2x = BMUx - X
	else:
		BMU2x = BMUx + X
	if BMUy > Y / 2:
		BMU3y = BMUy - Y
	else:
		BMU3y = BMUy + Y
	BMU4x = BMU2x
	BMU4y = BMU3y 
	return BMU, (BMU2x, BMU2y), (BMU3x, BMU3y), (BMU4x, BMU4y)


@jit(nopython=True)
def som_calc(som_size, num_iterations, data_scaled, is_torus=False):
	#data_scaled = normalize(data)
	initial_radius = (max(som_size[0],som_size[1])/2)**2
	time_constant = num_iterations/math.log(initial_radius)
	start_lrate = 0.1
	lattice = random_lattice(som_size, data_scaled.shape[1])
	datalen = len(data_scaled)
	X, Y, Z = lattice.shape

	for current_iteration in range(num_iterations):
		current_radius = initial_radius * math.exp(-current_iteration/time_constant)
		current_lrate = start_lrate * math.exp(-current_iteration/num_iterations)
		rand_input = np.random.randint(datalen)
		rand_vector = data_scaled[rand_input]

		BMU_dist = 1.7976931348623157e+308
		BMU = (0,0)

		for x in range(X):
			for y in range(Y):
				d = 0.0
				for z in range(Z):
					val = lattice[x,y,z]-rand_vector[z]
					valsqr = val * val
					d += valsqr

				if d < BMU_dist:
					BMU_dist = d
					BMU = (x,y)
		
		if is_torus:
			BMUs = get_all_BMU_indexes(BMU, X, Y)
			
			for BMU in BMUs:
				adapt(lattice, rand_vector, BMU, current_radius, current_lrate)

		else:
			adapt(lattice, rand_vector, BMU, current_radius, current_lrate)

	return lattice


@jit(nopython=True)
def adapt(lattice, rand_vector, BMU, current_radius, current_lrate):
	X, Y, Z = lattice.shape
	for x in range(X):
		for y in range(Y):
			a = x-BMU[0]
			b = y-BMU[1]
			d = a*a + b*b
			if d < current_radius:
				up = d * d
				down = current_radius * current_radius
				res = -up / (2 * down)
				influence = math.exp(res)
				for z in range(Z):
					diff = (rand_vector[z] - lattice[x,y,z]) * influence * current_lrate
					lattice[x,y,z] += diff

@jit(nopython=True)
def euclidean(vec1, vec2):
	L = vec1.shape[0]
	dist = 0
	for l in range(L):
		val = vec2[l] - vec1[l]
		valsqr = val * val
		dist += valsqr
	return math.sqrt(dist)


@jit(nopython=True)
def euclidean_squared(vec1, vec2):
	L = vec1.shape[0]
	dist = 0
	for l in range(L):
		val = vec2[l] - vec1[l]
		valsqr = val * val
		dist += valsqr
	return dist


@jit(nopython=True)
def u_matrix(lattice):
	X, Y, Z = lattice.shape
	u_values = np.empty((X,Y), dtype=np.float64)
	
	for y in range(Y):
		for x in range(X):
			current = lattice[x,y]
			dist = 0
			num_neigh = 0
			# left
			if x-1 >= 0:
				#middle
				vec = lattice[x-1,y]
				dist += euclidean(current, vec)
				num_neigh += 1
				if y - 1 >= 0:
					#sup
					vec = lattice[x-1, y-1]
					dist += euclidean(current, vec)
					num_neigh += 1
				if y + 1 < Y:
					# down
					vec = lattice[x-1,y+1]
					dist += euclidean(current, vec)
					num_neigh += 1
			# middle        
			if y - 1 >= 0:
				# up
				vec = lattice[x,y-1]
				dist += euclidean(current, vec)
				num_neigh += 1
			# down
			if y + 1 < Y:
				vec = lattice[x,y+1]
				dist += euclidean(current, vec)
				num_neigh += 1
			# right
			if x + 1 < X:
				# middle
				vec = lattice[x+1,y]
				dist += euclidean(current, vec)
				num_neigh += 1
				if y - 1 >= 0:
					#up
					vec = lattice[x+1,y-1]
					dist += euclidean(current, vec)
					num_neigh += 1
				if y + 1 < lattice.shape[1]:
					# down
					vec = lattice[x+1,y+1]
					dist += euclidean(current, vec)
					num_neigh += 1       
			u_values[x,y] = dist / num_neigh
	return u_values


def project_on_som(data, lattice, data_scaled=False):
	start = timer()
	if data_scaled:
		data_scaled = data
	else:
		data_scaled = normalize(data)
		
	projected = collections.defaultdict(list)
	for index, vec in enumerate(data_scaled):
		winning_cell, wi = find_closest(index, vec, lattice)
		projected[winning_cell].append(wi)
	final = {key: [data[v] for v in value] for key, value in projected.items()}
	end = timer()
	print("Projecting on SOM took: %f seconds." %(end - start))  
	return final

@jit(nopython=True)
def find_closest_data(data, lattice):
	X, Y, Z = lattice.shape
	new_lattice = np.empty(lattice.shape, dtype=np.float64)

	for x in range(X):
		for y in range(Y):
			min_val = 1.7976931348623157e+308
			lattice_vec = lattice[x,y]
			for i in range(len(data)):
				data_point = data[i]
				dist = euclidean_squared(lattice_vec,data_point)
				if dist < min_val:
					min_val = dist
					new_lattice[x,y] = data_point
	return new_lattice


def lattice_closest_vectors(data, lattice, data_scaled=False):
	start = timer()
	if data_scaled:
		data_scaled = data
	else:
		data_scaled = normalize(data)
	
	result = find_closest_data(data_scaled, lattice)
	end = timer()
	print("Finding closest data points took: %f seconds." %(end - start)) 
	return result


@jit(nopython=True)
def find_closest(index, vec, lattice):
	X, Y, Z = lattice.shape
	min_val = 1.7976931348623157e+308
	win_index = -1
	win_cell = (-1,-1)
	for x in range(X):
		for y in range(Y):
			dist = euclidean_squared(vec, lattice[x,y])
			if dist < min_val:
				min_val = dist
				win_index = index
				win_cell = (x,y)
	return win_cell, win_index

def som(som_size, num_iterations, data, is_torus=False, is_scaled=False):
	data_scaled = data
	if not is_scaled:
		start = timer()
		data_scaled = normalize(data)
		end = timer()
		print("Data scaling took: %f seconds." %(end - start))
	start = timer()  
	lattice = som_calc(som_size, num_iterations, data_scaled, is_torus)
	end = timer()
	print("SOM training took: %f seconds." %(end - start))  
	return lattice

def save_lattice(lattice, filename):
	np.save(filename, lattice)
	print ("SOM lattice saved at %s" %filename)

def load_lattice(filename):
	lattice = np.load(filename)
	print ("SOM lattice loaded from %s" %filename)	
	return lattice

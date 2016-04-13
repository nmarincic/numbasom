import matplotlib.pyplot as plt
import matplotlib.cm as colormaps

def plot_u_matrix(u_mat, fig_size=(8,8), colormap='viridis_r'):
	fig, ax = plt.subplots(figsize=fig_size)
	ax.imshow(u_mat.T, interpolation='nearest', cmap=colormap) 
	aspect='auto'
	plt.show()
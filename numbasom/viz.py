# AUTOGENERATED! DO NOT EDIT! File to edit: 01_viz.ipynb (unless otherwise specified).

__all__ = ['plot_u_matrix']

# Internal Cell
import matplotlib.pyplot as plt
import matplotlib.cm as colormaps

# Cell
def plot_u_matrix(u_mat, fig_size=(4,4), colormap='viridis_r'):
    fig, ax = plt.subplots(figsize=fig_size)
    ax.imshow(u_mat.T, interpolation='nearest', cmap=colormap)
    aspect='auto'
    plt.show()
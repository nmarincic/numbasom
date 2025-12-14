__all__ = ['plot_u_matrix']

import matplotlib.pyplot as plt


def plot_u_matrix(u_mat, fig_size=(4,4), colormap='viridis_r'):
    """Plots the U-matrix in matplotlib."""
    fig, ax = plt.subplots(figsize=fig_size)
    ax.imshow(u_mat, interpolation='nearest', cmap=colormap)
    plt.show()

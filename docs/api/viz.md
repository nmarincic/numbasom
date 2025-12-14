# Visualization Module

API reference for NumbaSOM visualization functions.

## plot_u_matrix

::: numbasom.plot_u_matrix
    options:
      show_root_heading: true

### Example: Plotting a U-Matrix

```python
from numbasom import SOM, u_matrix, plot_u_matrix
import numpy as np

# Train a SOM
data = np.random.random([200, 3])
som = SOM(som_size=(50, 100))
lattice = som.train(data, num_iterations=15000)

# Compute and plot U-matrix
um = u_matrix(lattice)
plot_u_matrix(um, fig_size=(6.2, 6.2))
```

![U-Matrix Example](../images/output_34_0.png)

### Parameters

- **u_mat**: The U-matrix computed from a trained lattice using `u_matrix()`
- **fig_size**: Tuple specifying the figure size (width, height) in inches. Default is `(4, 4)`
- **colormap**: Matplotlib colormap name. Default is `'viridis_r'` (reversed viridis)

### Available Colormaps

You can use any matplotlib colormap. Some good options for U-matrices:

- `'viridis_r'` (default) - perceptually uniform, good for colorblind viewers
- `'plasma_r'` - similar to viridis with more contrast
- `'coolwarm'` - diverging colormap
- `'gray_r'` - simple grayscale

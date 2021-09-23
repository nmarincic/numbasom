# Welcome to NumbaSOM
> A fast Self-Organizing Map Python library implemented in Numba.


This is a **fast and simple to use** SOM library. It utilizes online training (one data point at the time) rather than batch training. The implemented topologies are a simple 2D lattice or a torus.

## How to Install

The installation is available at PyPI. Simply type:

`pip install numbasom`

## How to use

A **Self-Organizing Map** is often used to show the underlying structure in data. To show how to use the library, we will train it on 200 random 3-dimensional vectors (so we can render them as colors):

```
import numpy as np
from numbasom import SOM
```

#### Create 200 random colors

```
data = np.random.random([200,3])
```

#### Initialize the library

We initalize a large map with 50 rows and 100 columns. The default topology is a 2D lattice. We can also train it on a torus by setting `is_torus=True`

```
som = SOM(som_size=(50,100), is_torus=False)
```

#### Train the SOM

We will adapt the lattice by iterating 10.000 times through our data points. If we set `ìs_scaled=False`, data will be normalized before training. 

```
lattice = som.train(data, num_iterations=10000, is_scaled=True)
```

    SOM training took: 1.739157 seconds.


#### We can display a number of lattice cells to make sure they are 3-dimensional vectors

```
lattice[1::6,1]
```




    array([[0.8898463 , 0.50800545, 0.07200279],
           [0.94995645, 0.3065905 , 0.11594923],
           [0.93479887, 0.2773684 , 0.08419648],
           [0.68727976, 0.26837477, 0.09449021],
           [0.52862876, 0.2603103 , 0.10168457],
           [0.30479918, 0.0459141 , 0.05882781],
           [0.16544945, 0.06159906, 0.07049482],
           [0.14075432, 0.10885766, 0.03924538],
           [0.21722675, 0.24569948, 0.04674323]])



The shape of the lattice should be (50, 100, 3)

```
lattice.shape
```




    (50, 100, 3)



#### Visualizing the lattice

Since our lattice is made of 3-dimensional vectors, we can represent it as a lattice of colors.

```
import matplotlib.pyplot as plt

plt.imshow(lattice)
plt.show()
```


![png](docs/images/output_21_0.png)


#### Compute U-matrix

Since the most of the data will not be 3-dimensional, we can use the U-matrix (unified distance matrix by Alfred Ultsch) to visualise the map and the clusters emerging on it. 

```
from numbasom import u_matrix

um = u_matrix(lattice)
```

```
um.shape
```




    (50, 100)



#### Plot U-matrix

The library contains a function `plot_u_matrix` that can help visualise it.

```
from numbasom import plot_u_matrix

plot_u_matrix(um, fig_size=(6.2,6.2))
```


![png](docs/images/output_28_0.png)


# Welcome to NumbaSOM
> A fast Self-Organizing Map Python library implemented in Numba.


This is a **fast and simple to use** SOM library. It utilizes online training (one data point at the time) rather than batch training. The implemented topologies are a simple 2D lattice or a torus.

## How to Install

The installation is available at PyPI. Simply type:

`pip install numbasom`

## How to use

A **Self-Organizing Map** is often used to show the underlying structure in data. To show how to use the library, we will train it on 200 random 3-dimensional vectors (so we can render them as colors):

```python
import numpy as np
from numbasom import SOM
```

#### Create 200 random colors

```python
data = np.random.random([200,3])
```

#### Initialize the library

We initalize a large map with 50 rows and 100 columns. The default topology is a 2D lattice. We can also train it on a torus by setting `is_torus=True`

```python
som = SOM(som_size=(50,100), is_torus=False)
```

#### Train the SOM

We will adapt the lattice by iterating 10.000 times through our data points. If we set `ìs_scaled=False`, data will be normalized before training. 

```python
lattice = som.train(data, num_iterations=10000, is_scaled=True)
```

    SOM training took: 1.716320 seconds.


#### We can display a number of lattice cells to make sure they are 3-dimensional vectors

```python
lattice[1::6,1]
```




    array([[0.05169845, 0.94472638, 0.87443554],
           [0.19436005, 0.77288777, 0.75509872],
           [0.22945833, 0.75253613, 0.63984275],
           [0.13979542, 0.85606064, 0.48404585],
           [0.20973443, 0.80124035, 0.42341624],
           [0.22262145, 0.83282046, 0.32173263],
           [0.23051704, 0.73412993, 0.21886991],
           [0.05582659, 0.6904873 , 0.09945935],
           [0.10519506, 0.92841518, 0.10019958]])



The shape of the lattice should be (50, 100, 3)

```python
lattice.shape
```




    (50, 100, 3)



#### Visualizing the lattice

Since our lattice is made of 3-dimensional vectors, we can represent it as a lattice of colors.

```python
import matplotlib.pyplot as plt

plt.imshow(lattice)
plt.show()
```


![png](docs/images/output_21_0.png)


#### Compute U-matrix

Since the most of the data will not be 3-dimensional, we can use the U-matrix (unified distance matrix by Alfred Ultsch) to visualise the map and the clusters emerging on it. 

```python
from numbasom import u_matrix

um = u_matrix(lattice)
```

```python
um.shape
```




    (50, 100)



#### Plot U-matrix

The library contains a function `plot_u_matrix` that can help visualise it.

```python
from numbasom import plot_u_matrix

plot_u_matrix(um, fig_size=(6.2,6.2))
```


![png](docs/images/output_28_0.png)


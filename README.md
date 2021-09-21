# NumbaSOM
> A Fast Self-Organizing Map Python Library Implemented in Numba.


If you need a **fast and simple to use** SOM library implemented as a 2D lattice or torus, check this out. It utilizes online rather than batch training. 

## Install

`pip install numbasom`

## How to use

Train a SOM on 1000 random 3-dimensional vectors:

```python
import numpy as np
from numbasom.core import NumbaSOM, u_matrix, plot_u_matrix
```

#### Load some data

```python
data = np.random.randn(100,3)
```

#### Initialize the library

```python
som = NumbaSOM(som_size=(20,20))
```

#### Train

```python
lattice = som.train(data, num_iterations=1000)
```

    Data scaling took: 0.000263 seconds.
    SOM training took: 0.003851 seconds.


#### Display the value in the first row and first column of the lattice

```python
lattice[1::6,1]
```




    array([[0.26589568, 0.50836002, 0.49843773],
           [0.48841612, 0.22821334, 0.468278  ],
           [0.67837494, 0.35688215, 0.60746632],
           [0.47968079, 0.39957501, 0.8833814 ]])



#### Make U-matrix

```python
um = u_matrix(lattice)
```

#### Plot U-matrix

```python
plot_u_matrix(um, fig_size=(4,4))
```


![png](docs/images/output_17_0.png)


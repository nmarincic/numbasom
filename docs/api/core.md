# Core Module

API reference for the core NumbaSOM functionality.

## SOM Class

::: numbasom.SOM
    options:
      show_root_heading: true
      members:
        - __init__
        - train

### Example: Creating and Training a SOM

Let's create a SOM with 5 rows and 8 columns:

```python
from numbasom import SOM
import numpy as np

som = SOM(som_size=(5, 8))
```

Let's create 10 random 3-dimensional data points and train the SOM:

```python
my_data = np.random.random([10, 3])
lattice = som.train(my_data, 1000)
```

```
SOM training took: 0.882079 seconds.
```

Let's see what is in the lattice's cell (1,1):

```python
lattice[1, 1]
```

```
array([0.33745451, 0.78054122, 0.91251117])
```

---

## U-Matrix

::: numbasom.u_matrix
    options:
      show_root_heading: true

### Example: Computing U-Matrix

Let's create a U-matrix of the lattice and check its shape:

```python
from numbasom import u_matrix

um = u_matrix(lattice)
um.shape
```

```
(5, 8)
```

---

## Projection Functions

### project_on_lattice

::: numbasom.project_on_lattice
    options:
      show_root_heading: true

#### Example: Projecting Data onto the Lattice

```python
from numbasom import project_on_lattice

projection = project_on_lattice(my_data, lattice)
for p in projection:
    if projection[p]:
        print(p, projection[p][0])
```

```
Projecting on SOM took: 0.159090 seconds.
(0, 0) [0.45463541 0.86601644 0.91961619]
(0, 4) [0.67644781 0.56173361 0.57405225]
...
```

---

### lattice_activations

::: numbasom.lattice_activations
    options:
      show_root_heading: true

#### Example: Computing Lattice Activations

Let us compute how each data vector activates the lattice (Euclidean distance from each cell):

```python
from numbasom import lattice_activations

scaled = lattice_activations(my_data, lattice, exponent=8)
```

```
Computing SOM activations took: 0.330122 seconds.
```

Activations of the data point 0:

```python
scaled[0].round(2)
```

```
array([[0.  , 0.  , 0.01, 0.03, 0.03, 0.03, 0.  , 0.  ],
       [0.  , 0.  , 0.01, 0.03, 0.03, 0.02, 0.  , 0.  ],
       [0.11, 0.06, 0.02, 0.03, 0.02, 0.02, 0.02, 0.02],
       [0.99, 0.84, 0.66, 0.05, 0.01, 0.02, 0.19, 0.16],
       [1.  , 0.89, 0.68, 0.57, 0.01, 0.02, 0.39, 0.39]])
```

---

### lattice_closest_vectors

::: numbasom.lattice_closest_vectors
    options:
      show_root_heading: true

#### Example: Finding Closest Vectors

Let's find the closest data vectors to each lattice cell:

```python
from numbasom import lattice_closest_vectors

closest = lattice_closest_vectors(my_data, lattice)
for c in closest:
    print(c, closest[c])
```

```
Finding closest data points took: 0.067116 seconds.
(0, 0) [0.45463541 0.86601644 0.91961619]
(0, 1) [0.45463541 0.86601644 0.91961619]
...
```

---

## Persistence Functions

### save_lattice

::: numbasom.save_lattice
    options:
      show_root_heading: true

### load_lattice

::: numbasom.load_lattice
    options:
      show_root_heading: true

#### Example: Saving and Loading

```python
from numbasom import save_lattice, load_lattice

save_lattice(lattice, "my_som.npy")
# SOM lattice saved at my_som.npy

loaded = load_lattice("my_som.npy")
# SOM lattice loaded from my_som.npy
```

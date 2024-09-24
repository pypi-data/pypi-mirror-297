# SlurmiPy

Run python functions on a SLURM cluster as easy as:
```
@slurm_cluster.execute
def hello_world():
    print("YAY, I am running via SLURM!")
```

SlurmiPy provides a factory class for managing Dask clusters on SLURM-based systems and executing functions using Dask parallelization.

## Installation

- Navigate to the directory containing `setup.py`.
- Run the following command to build and install the package:

```bash
pip install .
```

## Usage

Here's a basic example of how to use `SlurmiPy` on Perlmutter:

```python
from slurmipy import SlurmiPy, configs

# Create a SLURM cluster with 4 jobs
slurm_cluster = SlurmiPy(jobs=4, **configs["perlmutter_debug"])

@slurm_cluster.execute
def process_data(data):
    return [x**2 for x in data]

# Execute the function using the SLURM cluster
result = process_data([1, 2, 3, 4])

print(result)  # Output: [1, 4, 9, 16]

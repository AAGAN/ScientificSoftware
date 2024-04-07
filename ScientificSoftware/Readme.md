# Solution to the Scientific Software Problem from CFS

To clone the repository:

```shell
git clone https://github.com/AAGAN/ScientificSoftware.git
```

Then change directory to the cloned location

```shell
cd ScientificSoftware
```

Build the project and its dependencies

```shell
pip install .
```

Use python3 to run the code as follows:

```python
from ScientificSoftware import ScientificSoftwareProblem  
sol = ScientificSoftwareProblem() #create the solution object and initialize
sol.solve_ivp() #solve the two equations and output the results
```
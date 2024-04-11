# Solution to the Scientific Software Problem from CFS

To make sure the enviroment for running the ScientificSoftware package is clean, it is advisable to create a new virtual environment

```powershell
python -m venv ./.venv
```

If working from Windows Powershell, you may need to change the ExecutionPolicy to allow scripts. This needs Administrator previlages. Start a Powershell prompt as an Anministrator and run the following command:

```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy Unrestricted
```
Now you can activate the virtual environment from Windows Powershell:

```powershell
./.venv/Scripts/Activate.ps1
```
or if working in linux:
```linuxshell
source ./venv/bin/activate
```

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

To run the program, you can either import the module in Python as follows:

```python
from ScientificSoftware import ScientificSoftwareProblem
sol = ScientificSoftwareProblem()  # create the solution object and initialize
sol.solve_ivp()  # solve the two equations and output the results

```

Or, run the provided `run.py` file:

```shell
python run.py
```

To run the tests using pytest, run the following command in the root of the project:

```shell
pytest -v
```

I created a video demonstration of this implementation and uploaded [here](https://youtu.be/R-khYo-CcW8)

To add additional source terms (like cooling power per unit volume), I added a new method (API) for the ScientificSoftwareProblem class that will gets multiple funcitons with units of $W/m^3$ using dependency injection pattern. To use this method you can use the following:

```python
def cooling(t, T):
     return - 10000 * T # desired source term
sol.addSourceTerms(cooling)
sol.solve_ivp() 
```
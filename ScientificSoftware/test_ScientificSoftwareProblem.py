import pytest
import numpy as np
from solution import ScientificSoftwareProblem

@pytest.fixture
def problem_instance():
    return ScientificSoftwareProblem()

def test_initialization_with_default_values(problem_instance):
    assert problem_instance.rho_m == 8960
    assert problem_instance.mu_0 == 1.25663706143e-6

def test_specific_heat_capacity_function(problem_instance):
    assert problem_instance._ScientificSoftwareProblem__SpecificHeatCapacityFunc(100) == 0  # Assuming 100 is within the range of TemperatureC and SpecificHeatCapacity

def test_cu_resistivity_electrical_resistivity_function(problem_instance):
    assert problem_instance._ScientificSoftwareProblem__CuResistivityElectricalResistivityFunc(100) == 0  # Assuming 100 is within the range of TemperatureRho_e and CuElectricalResistivity

def test_dT_dt(problem_instance):
    T = 100
    assert problem_instance._ScientificSoftwareProblem__dT_dt(0, T) == 0  # Assuming T is within the range of TemperatureRho_e and SpecificHeatCapacity

def test_magnetic_field_magnitude(problem_instance):
    assert problem_instance._ScientificSoftwareProblem__MagneticFieldMagnitude() == 0  # Assuming all parameters are set to 0 initially

def test_solve_RK4(problem_instance):
    problem_instance.solve_RK4()
    assert np.all(problem_instance.PulseDuration >= 0)
    assert np.all(problem_instance.MagneticField >= 0)

def test_solve_ivp(problem_instance):
    problem_instance.solve_ivp()
    assert np.all(problem_instance.PulseDuration >= 0)
    assert np.all(problem_instance.MagneticField >= 0)

import pytest
import numpy as np
from ScientificSoftware import ScientificSoftwareProblem

@pytest.fixture
def SSP_Instance():
    return ScientificSoftwareProblem()

def test_initialization_with_default_values(SSP_Instance):
    assert SSP_Instance.rho_m == 8960
    assert SSP_Instance.mu_0 == 1.25663706143e-6

def test_specific_heat_capacity_data(SSP_Instance):
    assert SSP_Instance.SpecificHeatCapacity[0] == 0.09

def test_cu_resistivity_data(SSP_Instance):
    assert SSP_Instance.CuElectricalResistivity[0] == 0.015

@pytest.mark.parametrize(
        ('Temperature', 'SpecificHeat'),
        (
            (77,192),
            (100,252),
            (150,323)
        )
)
def test_specific_heat_capacity_interpolation(SSP_Instance, Temperature, SpecificHeat):
    assert SSP_Instance._ScientificSoftwareProblem__SpecificHeatCapacityFunc(Temperature) == pytest.approx(SpecificHeat)  # testing the correctness of interpolation for specific heat capacity of copper

@pytest.mark.parametrize(
    ('Temperature', 'Resistivity'),
    (
        (77,0.21e-8),
        (100,0.34e-8),
        (150,0.7e-8)
    )
)
def test_cu_resistivity_interpolation(SSP_Instance, Temperature, Resistivity):
    assert SSP_Instance._ScientificSoftwareProblem__CuResistivityElectricalResistivityFunc(Temperature) == pytest.approx(Resistivity)

def test_dT_dt(SSP_Instance):
    T = 100
    SSP_Instance.jiterator = 1.5e8
    assert 33.8 < SSP_Instance._ScientificSoftwareProblem__dT_dt(0, T) < 33.9  # testing the conservation of energy's ODE quation

def test_magnetic_field_magnitude(SSP_Instance):
    SSP_Instance.jiterator = 1.5e8
    assert 8.815 < SSP_Instance._ScientificSoftwareProblem__MagneticFieldMagnitude() < 8.825  # testing the equation for Ampere's law

def test_solve_RK4(SSP_Instance): #Test that the calculation of Pulse Duration is done and values are > 0 when solving with RK4 method
    SSP_Instance.solve_RK4(False)
    assert np.all(SSP_Instance.PulseDuration > 0)
    assert np.all(SSP_Instance.MagneticField > 0)

def test_solve_ivp(SSP_Instance): #Test that the calculation of Pulse Duration is done and values are > 0 when solving with scipy.integrate.solve_ivp method
    SSP_Instance.solve_ivp(False)
    assert np.all(SSP_Instance.PulseDuration > 0)
    assert np.all(SSP_Instance.MagneticField > 0)

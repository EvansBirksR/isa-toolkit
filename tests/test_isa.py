from __future__ import annotations
import numpy as np
from isa_toolkit.isa import isa_atmosphere, T0, p0


def test_sea_level_matches_standards():
    s = isa_atmosphere(0.0)
    assert abs(s.temperature - T0) < 1e-9
    assert abs(s.pressure - p0) < 1e-6


def test_tropopause_values():
    # Tropopause base at 11 km geopotential altitude
    s = isa_atmosphere(11_000.0, geometric=False)
    assert abs(s.temperature - 216.65) < 1e-2
    assert abs(s.pressure - 22_632.0) < 50.0  # Pa, approx standard


def test_vectorized():
    z = np.array([0.0, 1_000.0, 5_000.0])
    s = isa_atmosphere(z)
    assert s.temperature.shape == z.shape
    assert np.all(s.pressure[1:] < s.pressure[:-1])


def test_against_reference_table():
    # Reference values from 1976 US Standard Atmosphere (rounded)
    # Altitude (m), Temperature (K), Pressure (Pa), Density (kg/m^3)
    table = [
        (0,      288.15, 101325, 1.2250),
        (1000,   281.65,  89874, 1.1120),
        (5000,   255.65,  54019, 0.7364),
        (11000,  216.65,  22632, 0.3639),
        (20000,  216.65,   5474, 0.08803),
        (32000,  228.65,    868, 0.01322),
    ]
    for alt, T_ref, p_ref, rho_ref in table:
        s = isa_atmosphere(alt)
        assert abs(s.temperature - T_ref) < 0.2
        assert abs(s.pressure - p_ref) < 150
        assert abs(s.density - rho_ref) < 0.01
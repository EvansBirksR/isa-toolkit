import numpy as np
from isa_toolkit.aerodynamics import aerodynamic_state
from isa_toolkit.isa import isa_atmosphere, sea_level_atmosphere

def test_tas_eas_mach_scalar():
    atm = isa_atmosphere(0)
    # TAS input
    state_tas = aerodynamic_state(100, speed_type="TAS", atmosphere_state=atm)
    assert abs(state_tas.TAS - 100) < 1e-9
    assert abs(state_tas.EAS - 100) < 1e-6
    assert abs(state_tas.mach - (100 / atm.speed_of_sound)) < 1e-6

    # EAS input
    state_eas = aerodynamic_state(100, speed_type="EAS", atmosphere_state=atm)
    assert abs(state_eas.EAS - 100) < 1e-9
    assert abs(state_eas.TAS - 100) < 1e-6

    # Mach input
    mach_val = 0.5
    state_mach = aerodynamic_state(mach_val, speed_type="mach", atmosphere_state=atm)
    assert abs(state_mach.mach - mach_val) < 1e-9
    assert abs(state_mach.TAS - (mach_val * atm.speed_of_sound)) < 1e-6

def test_vectorized_tas():
    atm = isa_atmosphere([0, 5000, 10000])
    tas = np.array([100, 200, 300])
    state = aerodynamic_state(tas, speed_type="TAS", atmosphere_state=atm)
    assert np.allclose(state.TAS, tas)
    assert state.EAS.shape == tas.shape
    assert state.mach.shape == tas.shape
    assert state.reynolds.shape == tas.shape

def test_reynolds_and_dynamic_pressure():
    atm = isa_atmosphere(0)
    state = aerodynamic_state(100, speed_type="TAS", atmosphere_state=atm, characteristic_length=2)
    # Reynolds number should be positive and finite
    assert state.reynolds > 0
    # Dynamic pressure should match 0.5 * rho * V^2
    expected_q = 0.5 * atm.density * 100**2
    assert abs(state.dynamic_pressure - expected_q) < 1e-6

def test_dynamic_pressure_against_table():
    # Reference: sea level, TAS = 100 m/s, rho = 1.225 kg/m^3
    s = isa_atmosphere(0)
    state = aerodynamic_state(100, speed_type="TAS", atmosphere_state=s)
    expected_q = 0.5 * 1.225 * 100**2  # 6125 Pa
    assert abs(state.dynamic_pressure - expected_q) < 1.0

def test_mach_against_table():
    # Reference: sea level, speed of sound ≈ 340.294 m/s
    s = isa_atmosphere(0)
    state = aerodynamic_state(340.294, speed_type="TAS", atmosphere_state=s)
    assert abs(state.mach - 1.0) < 0.01

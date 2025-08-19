from __future__ import annotations
from dataclasses import dataclass
from typing import Union
import numpy as np

from .constants import g0, R, gamma_air, T0, p0, R_EARTH
from .isa import ISAState, sea_level_atmosphere, Number, ArrayLike

@dataclass
class AerodynamicState:
    """Aerodynamic state of aircraft returned by aerodynamic_state.

    All values are SI: K, Pa, kg/m^3, m/s.
    For array inputs, each field is a NumPy array of matching shape."""
    TAS: ArrayLike
    EAS: ArrayLike
    mach: ArrayLike
    reynolds: ArrayLike
    dynamic_pressure: ArrayLike
    stagnation_pressure: ArrayLike

def aerodynamic_state(
    speed: ArrayLike,
    characteristic_length: ArrayLike = 1.0,
    *,
    speed_type: str = "TAS",
    atmosphere_state: Union[ISAState, list[ISAState], np.ndarray] = None,
) -> AerodynamicState:
    """Computes the aerodynamic state of an aircraft given a speed, speed type, and atmospheric conditions.

    Parameters
    ----------
    speed : ArrayLike
        The input speed value(s) in m/s or Mach number (if speed_type='mach').
    speed_type : str, optional
        The type of speed provided ('TAS', 'EAS', 'mach'), by default "TAS".
    atmosphere_state : ISAState or array of ISAState, optional
        The atmospheric state(s) at the aircraft's altitude(s), by default sea_level_atmosphere.
    characteristic_length : ArrayLike, optional
        Characteristic length (e.g., chord length) in meters, by default 1.

    Returns
    -------
    AerodynamicState
        Object containing computed aerodynamic parameters:
            TAS : True Airspeed [m/s]
            EAS : Equivalent Airspeed [m/s]
            mach : Mach number [-]
            reynolds : Reynolds number [-]
            dynamic_pressure : Dynamic pressure [Pa]
            stagnation_pressure : Stagnation (total) pressure [Pa]
        For array inputs, each field is a NumPy array of matching shape.
    """

    allowed_speed_types = {"TAS", "EAS", "mach"}
    if speed_type not in allowed_speed_types:
        raise ValueError(f"Invalid speed_type '{speed_type}'. Allowed values are: {allowed_speed_types}")

    # Assign default atmosphere_state if None
    if atmosphere_state is None:
        atmosphere_state = sea_level_atmosphere

    if isinstance(atmosphere_state, ISAState):
        rho = atmosphere_state.density
        sos = atmosphere_state.speed_of_sound
        mu = atmosphere_state.dynamic_viscosity
        p = atmosphere_state.pressure
    else:
        atmosphere_state = np.asarray(atmosphere_state)
        rho = np.array([atm.density for atm in atmosphere_state])
        sos = np.array([atm.speed_of_sound for atm in atmosphere_state])
        mu = np.array([atm.dynamic_viscosity for atm in atmosphere_state])
        p = np.array([atm.pressure for atm in atmosphere_state])

    rho0 = sea_level_atmosphere.density

    speed_arr = np.array(speed)
    char_len_arr = np.array(characteristic_length)

    if speed_type == "TAS":
        TAS = speed_arr
        EAS = TAS * np.sqrt(rho / rho0)
    elif speed_type == "EAS":
        EAS = speed_arr
        TAS = EAS * np.sqrt(rho0 / rho)
    elif speed_type == "mach":
        mach = speed_arr
        TAS = mach * sos
        EAS = TAS * np.sqrt(rho / rho0)
    else:
        TAS = np.array([0])
        EAS = np.array([0])

    mach = TAS / sos
    reynolds = TAS * rho * char_len_arr / mu
    dynamic_pressure = 0.5 * rho * TAS**2
    stagnation_pressure = dynamic_pressure + p

    return AerodynamicState(
        TAS=TAS,
        EAS=EAS,
        mach=mach,
        reynolds=reynolds,
        dynamic_pressure=dynamic_pressure,
        stagnation_pressure=stagnation_pressure
    )



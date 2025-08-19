from __future__ import annotations
from dataclasses import dataclass
from typing import Union
import numpy as np

from .constants import g0, R, gamma_air, T0, p0, R_EARTH

Number = Union[float, int]
ArrayLike = Union[Number, np.ndarray]


@dataclass(slots=True)
class ISAState:
    """Thermodynamic state returned by isa_atmosphere.

    All values are SI: K, Pa, kg/m^3, m/s.
    For array inputs, each field is a NumPy array of matching shape.
    """
    geometric_altitude: ArrayLike
    geopotential_altitude: ArrayLike
    temperature: ArrayLike
    pressure: ArrayLike
    density: ArrayLike
    speed_of_sound: ArrayLike
    dynamic_viscosity: ArrayLike
    kinematic_viscosity: ArrayLike


# Layer definitions for 1976 ISA up to 32 km geopotential altitude
# Base geopotential altitudes (m)
_Hb = np.array([0.0, 11_000.0, 20_000.0])
# Lapse rates L = dT/dH (K/m)
_lapserate = np.array([-0.0065, 0.0, 0.0010])

# Precompute base temperatures and pressures for each layer base
_Tb = np.empty_like(_Hb)
_pb = np.empty_like(_Hb)
_Tb[0] = T0
_pb[0] = p0
# layer 0 → base at 11 km
_Tb[1] = _Tb[0] + _lapserate[0] * (11_000.0 - _Hb[0])
_pb[1] = _pb[0] * (_Tb[1] / _Tb[0]) ** (-g0 / (R * _lapserate[0]))
# layer 1 → base at 20 km (isothermal)
_Tb[2] = _Tb[1]  # L == 0
_pb[2] = _pb[1] * np.exp(-g0 * (20_000.0 - 11_000.0) / (R * _Tb[1]))


def geometric2geopotential(z: ArrayLike) -> ArrayLike:
    """Convert geometric altitude z (m above mean sea level) to geopotential altitude H (m).

    H = R_EARTH * z / (R_EARTH + z)
    """

    z_arr = np.asarray(z, dtype=float)
    H = R_EARTH * z_arr / (R_EARTH + z_arr)
    if np.isscalar(z):
        return float(H)
    else:
        return H


def geopotential2geometric(H: ArrayLike) -> ArrayLike:
    """Convert geopotential altitude H (m) to geometric altitude z (m).

    Inverse of geometric_to_geopotential.
    z = R_EARTH * H / (R_EARTH - H)
    """

    H_arr = np.asarray(H, dtype=float)
    z = R_EARTH * H_arr / (R_EARTH - H_arr)
    if np.isscalar(H):
        return float(z)
    else:
        return z


def _isa_gradient(H: np.ndarray, Hb: float, Tb: float, pb: float, L: float):
    """Gradient layer: Lapse rate != 0."""
    T = Tb + L * (H - Hb)
    p = pb * (T / Tb) ** (-g0 / (R * L))
    return T, p


def _isa_isothermal(H: np.ndarray, Hb: float, Tb: float, pb: float):
    """Isothermal layer: Lapse rate == 0."""
    T = np.full_like(H, Tb)
    p = pb * np.exp(-g0 * (H - Hb) / (R * Tb))
    return T, p


def _maybe_scalar(x_in: ArrayLike, x_out: np.ndarray) -> ArrayLike:
    arr = np.asarray(x_out)
    if np.isscalar(x_in):
        if arr.size == 1:
            return float(arr.item())
        else:
            raise ValueError("Cannot convert array of size > 1 to scalar")
    else:
        return arr


def isa_atmosphere(
    altitude: ArrayLike,
    *,
    geometric: bool = True,
) -> ISAState:
    """Compute ISA state (1976) up to 32 km.

    Parameters
    ----------
    altitude : float | ndarray
        Input altitude in meters. By default interpreted as geometric altitude.
    geometric : bool, default True
        If True, `altitude` is geometric. If False, it's geopotential.

    Returns
    -------
    ISAState
        temperature [K], pressure [Pa], density [kg/m^3], speed_of_sound [m/s]

    Notes
    -----
    Validated for 0–32 km geopotential altitude. Calling outside this range raises ValueError.
    """

    H = geometric2geopotential(altitude) if geometric else np.asarray(altitude, dtype=float)
    H_arr = np.asarray(H, dtype=float)

    if np.any(H_arr < 0) or np.any(H_arr > 32_000.0):
        raise ValueError("This implementation supports 0–32 km geopotential altitude.")

    # Determine which layer each point is in
    layer = np.select(
        [H_arr < 11_000.0, (H_arr >= 11_000.0) & (H_arr < 20_000.0), H_arr >= 20_000.0],
        [0, 1, 2],
    )

    T = np.empty_like(H_arr)
    p = np.empty_like(H_arr)

    # Layer 0: 0–11 km, L = -0.0065
    idx0 = layer == 0
    if np.any(idx0):
        T[idx0], p[idx0] = _isa_gradient(H_arr[idx0], _Hb[0], _Tb[0], _pb[0], _lapserate[0])

    # Layer 1: 11–20 km, isothermal
    idx1 = layer == 1
    if np.any(idx1):
        T[idx1], p[idx1] = _isa_isothermal(H_arr[idx1], _Hb[1], _Tb[1], _pb[1])

    # Layer 2: 20–32 km, L = +0.001
    idx2 = layer == 2
    if np.any(idx2):
        T[idx2], p[idx2] = _isa_gradient(H_arr[idx2], _Hb[2], _Tb[2], _pb[2], _lapserate[2])

    rho = p / (R * T)
    a = np.sqrt(gamma_air * R * T)

    mu = 1.458e-6 * T ** 1.5 / (T + 110.4) # Sutherland's formula for dynamic viscosity of air
    nu = mu / rho # Kinematic viscosity

    # Preserve scalar inputs as scalars
    T_out = _maybe_scalar(altitude, T)
    p_out = _maybe_scalar(altitude, p)
    rho_out = _maybe_scalar(altitude, rho)
    a_out = _maybe_scalar(altitude, a)
    mu_out = _maybe_scalar(altitude, mu)
    nu_out = _maybe_scalar(altitude, nu)

    geometric_altitude_out = _maybe_scalar(altitude, np.asarray(altitude, dtype=float) if geometric else geopotential2geometric(H_arr))
    geopotential_altitude_out = _maybe_scalar(altitude, H_arr)
    
    return ISAState(
        geometric_altitude=geometric_altitude_out,
        geopotential_altitude=geopotential_altitude_out,
        temperature=T_out,
        pressure=p_out,
        density=rho_out,
        speed_of_sound=a_out,
        dynamic_viscosity=mu_out,
        kinematic_viscosity=nu_out,
    )

sea_level_atmosphere = isa_atmosphere(0)
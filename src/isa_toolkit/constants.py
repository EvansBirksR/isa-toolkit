from __future__ import annotations

# Physical constants (SI)
g0: float = 9.80665               # m/s^2, standard gravity
R: float = 287.05287              # J/(kg·K), specific gas constant for dry air
gamma_air: float = 1.4            # ratio of specific heats for air

# Sea-level standard conditions (1976)
T0: float = 288.15                # K
p0: float = 101_325.0             # Pa
rho0: float = p0 / (R * T0)       # kg/m^3, ideal gas law for air density at sea level
a0: float = (gamma_air * R * T0) ** 0.5

# Geopotential Earth radius used by the 1976 ISA
R_EARTH: float = 6_356_766.0      # m
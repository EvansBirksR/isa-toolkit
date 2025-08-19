# ISA Toolkit

A comprehensive Python library for International Standard Atmosphere (ISA) calculations and aerodynamic computations for aerospace applications.

## Overview

The ISA Toolkit provides accurate implementations of the 1976 International Standard Atmosphere model, along with essential aerodynamic calculations for aerospace engineering applications. This library is designed for researchers, engineers, and students working with atmospheric and flight dynamics calculations.

## Features

### Atmospheric Calculations
- **Complete ISA 1976 implementation** (0-32 km altitude range)
- **Geometric ⟷ Geopotential altitude conversion**
- **Temperature, pressure, density, and speed of sound**
- **Dynamic and kinematic viscosity** (Sutherland's formula)
- **Vectorized operations** for efficient batch calculations

### Aerodynamic Computations
- **Airspeed conversions** (TAS ⟷ EAS ⟷ Mach)
- **Reynolds number calculations**
- **Dynamic and stagnation pressure**
- **Multiple input speed types** (TAS, EAS, Mach number)

**Command-line interface** for quick calculations

## Installation

Clone the repository and install in development mode:

```bash
git clone https://github.com/EvansBirksR/isa-toolkit.git
cd isa-toolkit
pip install -e .
```

This will install the package and its dependencies, making the `isa-toolkit` command available system-wide.

## Quick Start

### Basic Atmospheric Calculations

```python
from isa_toolkit import isa_atmosphere, sea_level_atmosphere
import numpy as np

# Sea level conditions (pre-computed)
print(f"Sea level temperature: {sea_level_atmosphere.temperature:.2f} K")
print(f"Sea level pressure: {sea_level_atmosphere.pressure:.0f} Pa")

# Single altitude calculation
cruise_alt = isa_atmosphere(10_000)  # 10 km geometric altitude
print(f"Temperature at 10km: {cruise_alt.temperature:.2f} K")
print(f"Pressure at 10km: {cruise_alt.pressure:.0f} Pa")
print(f"Density at 10km: {cruise_alt.density:.4f} kg/m³")

# Vectorized calculations
altitudes = np.array([0, 5000, 10000, 15000, 20000])
atm_profile = isa_atmosphere(altitudes)
print(f"Temperatures: {atm_profile.temperature}")
```

### Aerodynamic Calculations

```python
from isa_toolkit import aerodynamic_state, isa_atmosphere

# Calculate aerodynamics at cruise conditions
altitude = 10_000  # meters
airspeed = 250     # m/s TAS
chord_length = 2.0 # meters

# Get atmospheric state
atm = isa_atmosphere(altitude)

# Calculate aerodynamic parameters
aero = aerodynamic_state(
    speed=airspeed,
    speed_type="TAS",
    atmosphere_state=atm,
    characteristic_length=chord_length
)

print(f"True Airspeed: {aero.TAS:.1f} m/s")
print(f"Equivalent Airspeed: {aero.EAS:.1f} m/s")
print(f"Mach number: {aero.mach:.3f}")
print(f"Reynolds number: {aero.reynolds:.2e}")
print(f"Dynamic pressure: {aero.dynamic_pressure:.0f} Pa")
```

### Speed Conversions

```python
# Convert from Mach number to TAS/EAS
mach_085 = aerodynamic_state(0.85, speed_type="mach", atmosphere_state=atm)
print(f"Mach 0.85 = {mach_085.TAS:.0f} m/s TAS, {mach_085.EAS:.0f} m/s EAS")

# Convert from EAS to TAS/Mach
eas_200 = aerodynamic_state(200, speed_type="EAS", atmosphere_state=atm)
print(f"200 m/s EAS = {eas_200.TAS:.0f} m/s TAS, Mach {eas_200.mach:.3f}")
```

## Command Line Interface

The toolkit includes a CLI for quick calculations:

```bash
# ISA atmosphere at 35,000 ft
isa-toolkit isa 35000 --units ft --output table

# Aerodynamic state at Mach 0.85, 10 km altitude
isa-toolkit aero 0.85 --speed-type mach --altitude 10000

# JSON output for integration with other tools
isa-toolkit isa 10000 --output json
```

## API Reference

### Core Classes

#### `ISAState`
Dataclass containing complete atmospheric state:
- `geometric_altitude`: Geometric altitude [m]
- `geopotential_altitude`: Geopotential altitude [m]  
- `temperature`: Temperature [K]
- `pressure`: Pressure [Pa]
- `density`: Density [kg/m³]
- `speed_of_sound`: Speed of sound [m/s]
- `dynamic_viscosity`: Dynamic viscosity [Pa·s]
- `kinematic_viscosity`: Kinematic viscosity [m²/s]

#### `AerodynamicState`
Dataclass containing aerodynamic parameters:
- `TAS`: True Airspeed [m/s]
- `EAS`: Equivalent Airspeed [m/s]
- `mach`: Mach number [-]
- `reynolds`: Reynolds number [-]
- `dynamic_pressure`: Dynamic pressure [Pa]
- `stagnation_pressure`: Stagnation pressure [Pa]

### Main Functions

#### `isa_atmosphere(altitude, *, geometric=True)`
Calculate ISA atmospheric conditions.

**Parameters:**
- `altitude`: Altitude [m] (float or array)
- `geometric`: If True, altitude is geometric; if False, geopotential

**Returns:** `ISAState` object

#### `aerodynamic_state(speed, characteristic_length=1.0, *, speed_type="TAS", atmosphere_state=None)`
Calculate aerodynamic state parameters.

**Parameters:**
- `speed`: Speed value [m/s or Mach]
- `characteristic_length`: Reference length [m] 
- `speed_type`: Speed type ("TAS", "EAS", or "mach")
- `atmosphere_state`: `ISAState` object (defaults to sea level)

**Returns:** `AerodynamicState` object

## Examples

Complete examples are available in the `examples/` directory:

- **`01_basic_isa.py`**: Basic atmospheric calculations and altitude profiles
- **`02_aerodynamics.py`**: Airspeed conversions and aerodynamic parameters

Run examples:
```bash
python examples/01_basic_isa.py
python examples/02_aerodynamics.py
```

## Requirements

- Python ≥ 3.8
- NumPy ≥ 1.19

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## Author

**Rory Evans Birks**

---

*For questions, suggestions, or issues, please visit the [GitHub repository](https://github.com/EvansBirksR/isa-toolkit).*

# ISA Toolkit Examples

This directory contains examples demonstrating the core capabilities of the ISA toolkit library.

## Examples Overview

### 1. Basic ISA Calculations (`01_basic_isa.py`)
- Sea level atmospheric conditions
- Single altitude calculations
- Vectorized calculations for altitude profiles
- Standard atmospheric ratios (δ, σ, θ)

**Run:** `python 01_basic_isa.py`

### 2. Aerodynamics (`02_aerodynamics.py`)
- Airspeed conversions (TAS, EAS, Mach)
- Altitude effects on aerodynamic properties
- Reynolds number calculations
- Dynamic and stagnation pressure analysis

**Run:** `python 02_aerodynamics.py`

## Prerequisites

### Required
- Python 3.8+
- NumPy
- ISA Toolkit

### Optional
- Matplotlib (for any future plotting extensions)

## Quick Start

1. Install the package in development mode:
   ```bash
   cd /path/to/isa-toolkit
   pip install -e .
   ```

2. Run any example:
   ```bash
   cd examples
   python 01_basic_isa.py
   ```

## Example Output

### Basic ISA Calculation
```
Temperature: 288.15 K (15.0 °C)
Pressure: 101325 Pa (101.33 kPa)
Density: 1.2250 kg/m³
Speed of sound: 340.3 m/s
```

### Aerodynamic Analysis
```
TAS = 150.0 m/s
EAS = 150.0 m/s  
Mach = 0.4408
Reynolds = 1.02e+07
q = 11250.0 Pa
```

## Extending the Examples

Feel free to modify and extend these examples for your specific applications:

- Add custom atmospheric calculations
- Integrate with structural solvers 
- Integrate with XFOIL 
- Create automated analysis scripts
- Build data processing pipelines


---

**Note**: All calculations use SI units (meters, Pascals, Kelvin) unless otherwise specified. The examples include unit conversions where appropriate for practical applications.

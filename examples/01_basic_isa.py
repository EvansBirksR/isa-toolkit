#!/usr/bin/env python3
"""
Basic ISA Atmosphere Examples
============================

This example demonstrates the fundamental usage of the ISA toolkit for
atmospheric calculations at different altitudes.
"""

from isa_toolkit import isa_atmosphere, sea_level_atmosphere
import numpy as np

def main():
    print("ISA Toolkit - Basic Atmosphere Examples")
    print("=" * 50)
    
    # 1. Sea level conditions
    print("\n1. Sea Level Conditions:")
    print("-" * 30)
    sea_level = sea_level_atmosphere  # Pre-computed for convenience
    print(f"Temperature: {sea_level.temperature:.2f} K ({sea_level.temperature - 273.15:.2f} °C)")
    print(f"Pressure: {sea_level.pressure:.0f} Pa ({sea_level.pressure/1000:.2f} kPa)")
    print(f"Density: {sea_level.density:.4f} kg/m³")
    print(f"Speed of sound: {sea_level.speed_of_sound:.1f} m/s")
    
    # 2. Single altitude calculation
    print("\n2. Atmosphere at 10,000 m (typical cruise altitude):")
    print("-" * 50)
    cruise_alt = isa_atmosphere(10_000)
    print(f"Geometric altitude: {cruise_alt.geometric_altitude:.0f} m")
    print(f"Geopotential altitude: {cruise_alt.geopotential_altitude:.0f} m")
    print(f"Temperature: {cruise_alt.temperature:.2f} K ({cruise_alt.temperature - 273.15:.2f} °C)")
    print(f"Pressure: {cruise_alt.pressure:.0f} Pa ({cruise_alt.pressure/1000:.2f} kPa)")
    print(f"Density: {cruise_alt.density:.4f} kg/m³")
    print(f"Speed of sound: {cruise_alt.speed_of_sound:.1f} m/s")
    print(f"Dynamic viscosity: {cruise_alt.dynamic_viscosity:.3e} Pa·s")
    print(f"Kinematic viscosity: {cruise_alt.kinematic_viscosity:.3e} m²/s")
    
    # 3. Multiple altitudes (vectorized calculation)
    print("\n3. Atmosphere Profile (0 to 20 km):")
    print("-" * 40)
    altitudes = np.array([0, 5_000, 10_000, 15_000, 20_000])  # meters
    atm_profile = isa_atmosphere(altitudes)
    
    print(f"{'Alt [m]':>8} {'T [K]':>8} {'p [kPa]':>10} {'ρ [kg/m³]':>12} {'a [m/s]':>9}")
    print("-" * 50)
    for i, alt in enumerate(altitudes):
        T = atm_profile.temperature[i]
        p = atm_profile.pressure[i] / 1000
        rho = atm_profile.density[i]
        a = atm_profile.speed_of_sound[i]
        print(f"{alt:8.0f} {T:8.2f} {p:10.2f} {rho:12.6f} {a:9.1f}")
    
    # 4. Pressure ratio and density ratio calculations
    print("\n4. Standard Ratios (relative to sea level):")
    print("-" * 45)
    test_altitudes = [5_000, 11_000, 15_000, 20_000]  # meters
    
    print(f"{'Alt [m]':>8} {'δ (p/p₀)':>12} {'σ (ρ/ρ₀)':>12} {'θ (T/T₀)':>12}")
    print("-" * 45)
    
    for alt in test_altitudes:
        atm = isa_atmosphere(alt)
        delta = atm.pressure / sea_level.pressure
        sigma = atm.density / sea_level.density
        theta = atm.temperature / sea_level.temperature
        print(f"{alt:8.0f} {delta:12.6f} {sigma:12.6f} {theta:12.6f}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Aerodynamics Calculations
=========================

This example demonstrates aerodynamic calculations including airspeed conversions,
Mach number, Reynolds number, and pressure calculations.
"""

from isa_toolkit import isa_atmosphere, aerodynamic_state, sea_level_atmosphere
import numpy as np

def main():
    print("ISA Toolkit - Aerodynamics Examples")
    print("=" * 40)
    
    # 1. Basic airspeed calculations at 10000m
    print("\n1. Airspeed Conversions at 10000m:")
    print("-" * 40)
    
    # Calculate different speed types
    speeds_ms = [50, 100, 150, 200, 250]  # m/s
    
    print(f"{'TAS [m/s]':>10} {'EAS [m/s]':>10} {'Mach':>8} {'Re (L=1m)':>12}")
    print("-" * 42)

    atm = isa_atmosphere(10_000)

    for speed in speeds_ms:
        aero = aerodynamic_state(speed, speed_type="TAS", atmosphere_state=atm, characteristic_length=1.0)
        print(f"{speed:10.0f} {aero.EAS:10.1f} {aero.mach:8.4f} {aero.reynolds:12.2e}")
    
    # 2. Altitude effects on aerodynamics
    print("\n2. Altitude Effects on Aerodynamics:")
    print("-" * 40)
    print("Fixed TAS = 150 m/s, varying altitude")
    
    altitudes = [0, 5_000, 10_000, 15_000, 20_000]  # meters
    tas_fixed = 150  # m/s
    
    print(f"{'Alt [m]':>8} {'TAS [m/s]':>10} {'EAS [m/s]':>10} {'Mach':>8} {'q [Pa]':>10}")
    print("-" * 48)
    
    for alt in altitudes:
        atm = isa_atmosphere(alt)
        aero = aerodynamic_state(tas_fixed, atmosphere_state=atm, speed_type="TAS")
        print(f"{alt:8.0f} {aero.TAS:10.1f} {aero.EAS:10.1f} {aero.mach:8.4f} {aero.dynamic_pressure:10.0f}")
    
    # 3. Mach number calculations
    print("\n3. Mach Number Calculations:")
    print("-" * 35)
    print("Various Mach numbers at 10,000 m altitude")
    
    mach_numbers = [0.3, 0.5, 0.7, 0.85, 0.95]
    cruise_altitude = 10_000  # meters
    atm_cruise = isa_atmosphere(cruise_altitude)
    
    print(f"{'Mach':>6} {'TAS [m/s]':>10} {'TAS [kt]':>10} {'q [kPa]':>10} {'p₀ [kPa]':>10}")
    print("-" * 48)
    
    for mach in mach_numbers:
        aero = aerodynamic_state(mach, atmosphere_state=atm_cruise, speed_type="mach")
        tas_knots = aero.TAS * 1.944  # Convert m/s to knots
        q_kpa = aero.dynamic_pressure / 1000
        p0_kpa = aero.stagnation_pressure / 1000
        print(f"{mach:6.2f} {aero.TAS:10.1f} {tas_knots:10.1f} {q_kpa:10.2f} {p0_kpa:10.2f}")
    
    # 4. Reynolds number analysis
    print("\n4. Reynolds Number Analysis:")
    print("-" * 35)
    print("Effect of characteristic length and altitude")
    
    chord_lengths = [0.5, 1.0, 2.0, 5.0]  # meters (wing chord lengths)
    test_altitudes = [0, 10_000]  # sea level and cruise
    test_speed = 100  # m/s TAS
    
    print(f"{'Chord [m]':>10} {'Alt [m]':>8} {'Reynolds':>12}")
    print("-" * 42)
    
    for alt in test_altitudes:
        atm = isa_atmosphere(alt)
        for chord in chord_lengths:
            aero = aerodynamic_state(test_speed, characteristic_length=chord, 
                                   atmosphere_state=atm, speed_type="TAS")
            print(f"{chord:10.1f} {alt:8.0f} {aero.reynolds:12.2e}")

if __name__ == "__main__":
    main()

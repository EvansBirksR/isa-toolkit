from __future__ import annotations
import argparse
import json
from .isa import isa_atmosphere, sea_level_atmosphere
from .aerodynamics import aerodynamic_state

FT_TO_M = 0.3048

def main() -> None:
    parser = argparse.ArgumentParser(description="ISA Toolkit CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ISA commands
    isa_parser = subparsers.add_parser("isa", help="Calculate ISA atmosphere state")
    isa_parser.add_argument("altitude", type=float, help="Altitude value")
    isa_parser.add_argument("--type", choices=["geometric", "geopotential"], default="geometric")
    isa_parser.add_argument("--units", choices=["m", "ft"], default="m")
    isa_parser.add_argument("--output", choices=["table", "json"], default="table")

    # Aerodynamics commands
    aero_parser = subparsers.add_parser("aero", help="Calculate aerodynamic state")
    aero_parser.add_argument("speed", type=float, help="Speed value (m/s or Mach)")
    aero_parser.add_argument("--speed-type", choices=["TAS", "EAS", "mach"], default="TAS")
    aero_parser.add_argument("--altitude", type=float, default=0.0, help="Altitude value")
    aero_parser.add_argument("--altitude-type", choices=["geometric", "geopotential"], default="geometric")
    aero_parser.add_argument("--altitude-units", choices=["m", "ft"], default="m")
    aero_parser.add_argument("--char-len", type=float, default=1.0, help="Characteristic length (m)")
    aero_parser.add_argument("--output", choices=["table", "json"], default="table")

    args = parser.parse_args()

    if args.command == "isa":
        alt_m = args.altitude * (FT_TO_M if args.units == "ft" else 1.0)
        state = isa_atmosphere(alt_m, geometric=(args.type == "geometric"))
        if args.output == "json":
            print(
                json.dumps(
                    {
                        "temperature_K": state.temperature,
                        "pressure_Pa": state.pressure,
                        "density_kg_per_m3": state.density,
                        "speed_of_sound_m_per_s": state.speed_of_sound,
                        "dynamic_viscosity_Pa_s": state.dynamic_viscosity,
                        "kinematic_viscosity_m2_per_s": state.kinematic_viscosity,
                    },
                    indent=2,
                )
            )
        else:
            print(f"T = {state.temperature:.2f} K")
            print(f"p = {state.pressure:.2f} Pa")
            print(f"rho = {state.density:.4f} kg/m^3")
            print(f"a = {state.speed_of_sound:.2f} m/s")
            print(f"mu = {state.dynamic_viscosity:.6e} Pa·s")
            print(f"nu = {state.kinematic_viscosity:.6e} m^2/s")
    elif args.command == "aero":
        alt_m = args.altitude * (FT_TO_M if args.altitude_units == "ft" else 1.0)
        atm_state = isa_atmosphere(alt_m, geometric=(args.altitude_type == "geometric"))
        aero = aerodynamic_state(
            speed=args.speed,
            speed_type=args.speed_type,
            atmosphere_state=atm_state,
            characteristic_length=args.char_len,
        )
        if args.output == "json":
            print(
                json.dumps(
                    {
                        "TAS_m_per_s": aero.TAS,
                        "EAS_m_per_s": aero.EAS,
                        "mach": aero.mach,
                        "reynolds": aero.reynolds,
                        "dynamic_pressure_Pa": aero.dynamic_pressure,
                        "stagnation_pressure_Pa": aero.stagnation_pressure,
                    },
                    indent=2,
                )
            )
        else:
            print(f"TAS = {aero.TAS:.2f} m/s")
            print(f"EAS = {aero.EAS:.2f} m/s")
            print(f"Mach = {aero.mach:.4f}")
            print(f"Reynolds = {aero.reynolds:.2e}")
            print(f"q = {aero.dynamic_pressure:.2f} Pa")
            print(f"p0 = {aero.stagnation_pressure:.2f} Pa")


if __name__ == "__main__":
    main()
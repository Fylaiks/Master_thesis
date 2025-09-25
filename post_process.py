from ase.calculators.orca import Orca
from ase.io import read

# Read geometry from your ORCA input or output
atoms = read("calc.out")   # ASE can parse final structure from ORCA out

# Attach ORCA calculator (pointing to your existing results)
calc = Orca(label="calc")  # ASE looks for calc.out, calc.gbw etc.
atoms.calc = calc

# Get properties
energy = atoms.get_potential_energy()   # Final SCF energy (in eV by default)
dipole = atoms.get_dipole_moment()      # Dipole vector [Dx, Dy, Dz] in Debye
charges = atoms.get_charges()           # Mulliken charges if available

print("=== ORCA Single Point via ASE ===")
print(f"Energy: {energy:.6f} eV")
print(f"Dipole moment: {dipole} Debye")

print("\nMulliken charges:")
for atom, q in zip(atoms.get_chemical_symbols(), charges):
    print(f"{atom:>2s} : {q: .3f}")

# generate_orca_input.py

def xyz_to_orca_inp(xyz_file, inp_file, method="B3LYP", basis="def2-SVP", charge=0, mult=1):
    """
    Convert an XYZ file into an ORCA input file for single point energy calculation.
    """
    # Read XYZ file
    with open(xyz_file, "r") as f:
        lines = f.readlines()

    # Skip the first two lines (atom count and comment)
    atom_lines = lines[2:]

    # Write ORCA input file
    with open(inp_file, "w") as f:
        f.write(f"! {method} {basis} SP\n\n")
        f.write(f"* xyz {charge} {mult}\n")
        for line in atom_lines:
            f.write(line)
        f.write("*\n")

if __name__ == "__main__":
    xyz_file = "Structures/Zn_Im_2_acetate_2/1148454.xyz"   # path to your .xyz file
    inp_file = "calc.inp"                # output ORCA input file

    xyz_to_orca_inp(xyz_file, inp_file)

    print(f"ORCA input file '{inp_file}' generated successfully.")

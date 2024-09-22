from ase import Atoms
from ase_extension import _ext
from ase.calculators.singlepoint import SinglePointCalculator

max_int = 2**31 - 1


def read_extxyz(filepath, start=None, end=None, step=1):
    results = _ext.read_extxyz(filepath, start, end, step)
    atoms_list = []
    for result in results:
        symbols, positions, cell, energy, forces, stress, momenta = result
        atoms = Atoms(symbols=symbols, positions=positions, cell=cell)
        if cell is not None:
            atoms.pbc = True

        if energy is not None:
            calc = SinglePointCalculator(
                atoms, energy=energy, forces=forces, stress=stress
            )
            atoms.set_calculator(calc)

        if momenta is not None:
            atoms.set_momenta(momenta)

        atoms_list.append(atoms)
    if len(atoms_list) == 1:
        return atoms_list[0]
    return atoms_list

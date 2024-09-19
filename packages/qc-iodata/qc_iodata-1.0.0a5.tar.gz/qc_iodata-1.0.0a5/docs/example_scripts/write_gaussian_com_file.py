#!/usr/bin/env python

from iodata import load_one, write_input

mol = load_one("water.pdb")
mol.lot = "B3LYP"
mol.obasis_name = "6-31g*"
mol.run_type = "opt"
with open("my_template.com") as fh:
    write_input(mol, "water.com", fmt="gaussian", template=fh.read())

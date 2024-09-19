# IODATA is an input and output module for quantum chemistry.
# Copyright (C) 2011-2019 The IODATA Development Team
#
# This file is part of IODATA.
#
# IODATA is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# IODATA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Gaussian Cube file format.

Cube files are generated by various QC codes these days, including
`Gaussian <http://www.gaussian.com/>`_, `CP2K <http://www.cp2k.org/>`_,
`GPAW <https://wiki.fysik.dtu.dk/gpaw/>`_, `Q-Chem <http://www.q-chem.com/>`_, ...

Note that the second column in the geometry specification of the cube file is interpreted
as the effective core charges.
"""

from typing import TextIO

import numpy as np
from numpy.typing import NDArray

from ..docstrings import document_dump_one, document_load_one
from ..iodata import IOData
from ..utils import Cube, LineIterator

__all__ = ()


PATTERNS = ["*.cube", "*.cub"]


def _read_cube_header(
    lit: LineIterator,
) -> tuple[str, NDArray[float], NDArray[int], NDArray[float], dict[str, NDArray], NDArray[float]]:
    """Load header data from a CUBE file object.

    Parameters
    ----------
    lit
        The line iterator to read the data from.

    Returns
    -------
    Tuple with ``title``, ``atcoords``, ``atnums``, ``cellvecs``, ``ugrid`` & ``atcorenums``.

    """
    # Read the title
    title = next(lit).strip()
    # skip the second line
    next(lit)

    def read_grid_line(line: str) -> tuple[int, NDArray[float]]:
        """Read a grid line from the cube file."""
        words = line.split()
        return (
            int(words[0]),
            np.array([float(words[1]), float(words[2]), float(words[3])], float),
            # all coordinates in a cube file are in atomic units
        )

    # number of atoms and origin of the grid
    natom, origin = read_grid_line(next(lit))
    # numer of grid points in A direction and step vector A, and so on
    shape0, axis0 = read_grid_line(next(lit))
    shape1, axis1 = read_grid_line(next(lit))
    shape2, axis2 = read_grid_line(next(lit))
    shape = np.array([shape0, shape1, shape2], int)
    axes = np.array([axis0, axis1, axis2])

    cellvecs = axes * shape.reshape(-1, 1)
    cube = {"origin": origin, "axes": axes, "shape": shape}

    def read_atom_line(line: str) -> tuple[int, float, NDArray[float]]:
        """Read an atomic number and coordinate from the cube file."""
        words = line.split()
        return (
            int(words[0]),
            float(words[1]),
            np.array([float(words[2]), float(words[3]), float(words[4])], float),
            # all coordinates in a cube file are in atomic units
        )

    atnums = np.zeros(natom, int)
    atcorenums = np.zeros(natom, float)
    atcoords = np.zeros((natom, 3), float)
    for i in range(natom):
        atnums[i], atcorenums[i], atcoords[i] = read_atom_line(next(lit))
        # If the atcorenum field is zero, we assume that no effective core
        # potentials were used.
        if atcorenums[i] == 0.0:
            atcorenums[i] = atnums[i]

    return title, atcoords, atnums, cellvecs, cube, atcorenums


def _read_cube_data(lit: LineIterator, cube: dict[str, NDArray[float]]):
    """Load cube data from a CUBE file object.

    Parameters
    ----------
    lit
        The line iterator to read the data from.

    Returns
    -------
    The cube data array.

    """
    cube["data"] = np.zeros(tuple(cube["shape"]), float)
    tmp = cube["data"].ravel()
    counter = 0
    words = []
    while counter < tmp.size:
        if not words:
            words = next(lit).split()
        tmp[counter] = float(words.pop(0))
        counter += 1


@document_load_one("Gaussian Cube", ["atcoords", "atcorenums", "atnums", "cellvecs", "cube"])
def load_one(lit: LineIterator) -> dict:
    """Do not edit this docstring. It will be overwritten."""
    title, atcoords, atnums, cellvecs, cube, atcorenums = _read_cube_header(lit)
    _read_cube_data(lit, cube)
    del cube["shape"]
    return {
        "title": title,
        "atcoords": atcoords,
        "atnums": atnums,
        "cellvecs": cellvecs,
        "cube": Cube(**cube),
        "atcorenums": atcorenums,
    }


def _write_cube_header(
    f: TextIO,
    title: str,
    atcoords: NDArray[float],
    atnums: NDArray[int],
    cube: dict[str, NDArray],
    atcorenums: NDArray[float],
):
    print(title, file=f)
    print("OUTER LOOP: X, MIDDLE LOOP: Y, INNER LOOP: Z", file=f)
    natom = len(atnums)
    x, y, z = cube.origin
    print(f"{natom:5d} {x: 11.6f} {y: 11.6f} {z: 11.6f}", file=f)
    for i in range(3):
        x, y, z = cube.axes[i]
        print(f"{cube.shape[i]:5d} {x: 11.6f} {y: 11.6f} {z: 11.6f}", file=f)
    for i in range(natom):
        q = atcorenums[i]
        x, y, z = atcoords[i]
        print(f"{atnums[i]:5d} {q: 11.6f} {x: 11.6f} {y: 11.6f} {z: 11.6f}", file=f)


def _write_cube_data(f: TextIO, cube_data: NDArray[float], block_size: int):
    counter = 0
    for value in cube_data.flat:
        f.write(f" {value: 12.5E}")
        # go to next line after adding 6 values on a line
        if counter % 6 == 5:
            f.write("\n")
        # go to next line after reaching the block_size & reset counter
        if block_size % 6 != 0 and counter % block_size == block_size - 1:
            f.write("\n")
            counter = 0
            continue
        counter += 1


@document_dump_one("Gaussian Cube", ["atcoords", "atnums", "cube"], ["title", "atcorenums"])
def dump_one(f: TextIO, data: IOData):
    """Do not edit this docstring. It will be overwritten."""
    title = data.title or "Created with IOData"
    _write_cube_header(f, title, data.atcoords, data.atnums, data.cube, data.atcorenums)
    _write_cube_data(f, data.cube.data, data.cube.shape[2])

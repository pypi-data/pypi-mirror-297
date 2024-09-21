#  SPDX-FileCopyrightText: 2024 EasyCrystallography contributors <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022-2023  Contributors to the EasyScience project <https://github.com/EasyScience/EasyCrystallography>

from __future__ import annotations

__author__ = 'github.com/wardsimon'
__version__ = '0.1.0'

from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar
from typing import Union

import numpy as np
from easyscience.Objects.Groups import BaseCollection
from easyscience.Objects.ObjectClasses import BaseObj
from easyscience.Objects.Variable import Descriptor
from easyscience.Objects.Variable import Parameter

from .AtomicDisplacement import AtomicDisplacement
from .Lattice import PeriodicLattice
from .Specie import Specie

if TYPE_CHECKING:
    from easyscience.Utils.typing import iF


_SITE_DETAILS = {
    "label": {
        "value": "H",
        "description": "A unique identifier for a particular site in the crystal",
        "url": "https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html",
    },
    "position": {
        "value": 0.0,
        "description": "Atom-site coordinate as fractions of the unit cell length.",
        "url": "https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html",
        "fixed": True,
    },
    "occupancy": {
        "value": 1.0,
        "description": "The fraction of the atom type present at this site.",
        "url": "https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html",
        "fixed": True,
    },
}

S = TypeVar("S", bound="Site")


class Site(BaseObj):

    label: ClassVar[Descriptor]
    specie: ClassVar[Specie]
    occupancy: ClassVar[Parameter]
    fract_x: ClassVar[Parameter]
    fract_y: ClassVar[Parameter]
    fract_z: ClassVar[Parameter]

    def __init__(
        self,
        label: Optional[Union[str, Descriptor]] = None,
        specie: Optional[Union[str, Specie]] = None,
        occupancy: Optional[Union[float, Parameter]] = None,
        fract_x: Optional[Union[float, Parameter]] = None,
        fract_y: Optional[Union[float, Parameter]] = None,
        fract_z: Optional[Union[float, Parameter]] = None,
        interface: Optional[iF] = None,
        **kwargs,
    ):

        b_iso_or_equiv = kwargs.get("b_iso_or_equiv", None)
        if b_iso_or_equiv is not None:
            adp = AtomicDisplacement("Biso", Biso=b_iso_or_equiv)
            kwargs["adp"] = adp

        super(Site, self).__init__(
            "site",
            label=Descriptor("label", **_SITE_DETAILS["label"]),
            specie=Specie(_SITE_DETAILS["label"]["value"]),
            occupancy=Parameter("occupancy", **_SITE_DETAILS["occupancy"]),
            fract_x=Parameter("fract_x", **_SITE_DETAILS["position"]),
            fract_y=Parameter("fract_y", **_SITE_DETAILS["position"]),
            fract_z=Parameter("fract_z", **_SITE_DETAILS["position"]),
            **kwargs,
        )
        if label is not None:
            self.label = label
        if specie is not None:
            self.specie = specie
        else:
            if label is not None:
                self.specie = label
        if occupancy is not None:
            self.occupancy = occupancy
        if fract_x is not None:
            self.fract_x = fract_x
        if fract_y is not None:
            self.fract_y = fract_y
        if fract_z is not None:
            self.fract_z = fract_z
        self.interface = interface

    def __repr__(self) -> str:
        return (
            f"Atom {self.name} ({self.specie.raw_value}) @"
            f" ({self.fract_x.raw_value}, {self.fract_y.raw_value}, {self.fract_z.raw_value})"
        )

    @property
    def name(self) -> str:
        return self.label.raw_value

    @property
    def fract_coords(self) -> np.ndarray:
        """
        Get the current sites fractional co-ordinates as an array

        :return: Array containing fractional co-ordinates
        :rtype: np.ndarray
        """
        return np.array(
            [self.fract_x.raw_value, self.fract_y.raw_value, self.fract_z.raw_value]
        )

    def fract_distance(self, other_site: S) -> float:
        """
        Get the distance between two sites

        :param other_site: Second site
        :param other_site: Second site
        :type other_site: Site
        :return: Distance between 2 sites
        :rtype: float
        """
        return np.linalg.norm(other_site.fract_coords - self.fract_coords)

    @property
    def x(self) -> Parameter:
        return self.fract_x

    @property
    def y(self) -> Parameter:
        return self.fract_y

    @property
    def z(self) -> Parameter:
        return self.fract_z

    @property
    def is_magnetic(self) -> bool:
        return getattr(self.specie, 'spin', None) is not None or hasattr(self, 'msp')


class PeriodicSite(Site):
    def __init__(
        self,
        lattice: Optional[PeriodicLattice] = None,
        label: Optional[Union[str, Descriptor]] = None,
        specie: Optional[Union[str, Specie]] = None,
        occupancy: Optional[Union[float, Parameter]] = None,
        fract_x: Optional[Union[float, Parameter]] = None,
        fract_y: Optional[Union[float, Parameter]] = None,
        fract_z: Optional[Union[float, Parameter]] = None,
        interface: Optional[iF] = None,
        **kwargs,
    ):
        super(PeriodicSite, self).__init__(
            label, specie, occupancy, fract_x, fract_y, fract_z, **kwargs
        )
        if lattice is None:
            lattice = PeriodicLattice()
        self.lattice = lattice
        self.interface = interface

    @staticmethod
    def _from_site_kwargs(lattice: PeriodicLattice, site: S) -> Dict[str, float]:
        return {
            "lattice": lattice,
            "label": site.label,
            "specie": site.specie,
            "occupancy": site.occupancy,
            "fract_x": site.fract_x,
            "fract_y": site.fract_y,
            "fract_z": site.fract_z,
            "interface": site.interface,
        }

    @classmethod
    def from_site(cls, lattice: PeriodicLattice, site: S) -> S:
        kwargs = cls._from_site_kwargs(lattice, site)
        return cls(**kwargs)

    def get_orbit(self) -> np.ndarray:
        """
        Generate all orbits for a given fractional position.

        """
        sym_op = self.lattice.spacegroup._sg_data.get_orbit
        return sym_op(self.fract_coords)

    @property
    def cart_coords(self) -> np.ndarray:
        """
        Get the atomic position in Cartesian form.
        :return:
        :rtype:
        """
        return self.lattice.get_cartesian_coords(self.fract_coords)


class Atoms(BaseCollection):

    _SITE_CLASS = Site

    def __init__(self, name: str, *args, interface: Optional[iF] = None, **kwargs):
        if not isinstance(name, str):
            raise TypeError("A `name` for this collection must be given in string form")
        super(Atoms, self).__init__(name, *args, **kwargs)
        self.interface = interface
        self._kwargs._stack_enabled = True

    def __repr__(self) -> str:
        return f"Collection of {len(self)} sites."

    def __getitem__(
        self, idx: Union[int, slice, str]
    ) -> Union[Parameter, Descriptor, BaseObj, "BaseCollection"]:
        if isinstance(idx, str) and idx in self.atom_labels:
            idx = self.atom_labels.index(idx)
        return super(Atoms, self).__getitem__(idx)

    def __delitem__(self, key: Union[int, str]):
        if isinstance(key, str) and key in self.atom_labels:
            key = self.atom_labels.index(key)
        return super(Atoms, self).__delitem__(key)

    def remove(self, key: Union[int, str]):
        self.__delitem__(key)

    def append(self, *args, **kwargs):
        """
        Add an atom to the crystal
        """
        if len(args) == 1 and isinstance(args[0], Site):
            atom = args[0]
        else:
            atom = Site(*args, **kwargs)
        super(Atoms, self).append(atom)

    # def append(self, item: S):
    #     if not issubclass(type(item), Site):
    #         raise TypeError("Item must be a Site")
    #     if item.label.raw_value in self.atom_labels:
    #         raise AttributeError(
    #             f"An atom of name {item.label.raw_value} already exists."
    #         )
    #     super(Atoms, self).append(item)

    @property
    def atom_labels(self) -> List[str]:
        return [atom.label.raw_value for atom in self]

    @property
    def atom_species(self) -> List[str]:
        return [atom.specie.raw_value for atom in self]

    @property
    def atom_occupancies(self) -> np.ndarray:
        return np.array([atom.occupancy.raw_value for atom in self])


A = TypeVar("A", bound=Atoms)


class PeriodicAtoms(Atoms):

    _SITE_CLASS = PeriodicSite

    def __init__(self, name: str, *args,
                 lattice: Optional[PeriodicLattice] = None,
                 interface: Optional[iF] = None, **kwargs):
        args = list(args)
        if lattice is None:
            for item in args:
                if hasattr(item, "lattice"):
                    lattice = item.lattice
                    break
        if lattice is None:
            raise AttributeError
        for idx, item in enumerate(args):
            if issubclass(type(item), Site):
                args[idx] = self._SITE_CLASS.from_site(lattice, item)
        super(PeriodicAtoms, self).__init__(name, *args, **kwargs, interface=interface)
        self.lattice = lattice

    @classmethod
    def from_atoms(cls, lattice: PeriodicLattice, atoms: Atoms) -> A:
        return cls(atoms.name, *atoms, lattice=lattice, interface=atoms.interface)

    def __repr__(self) -> str:
        return f"Collection of {len(self)} periodic sites."

    def append(self, item: S):
        if not issubclass(item.__class__, Site):
            raise TypeError("Item must be a Site or periodic site")
        if item.label.raw_value in self.atom_labels:
            raise AttributeError(
                f"An atom of name {item.label.raw_value} already exists."
            )
        # if isinstance(item, Site):
        item = self._SITE_CLASS.from_site(self.lattice, item)
        super(PeriodicAtoms, self).append(item)

    def get_orbits(self, magnetic_only: bool = False):
        orbit_dict = {}
        for item in self:
            if magnetic_only and not item.is_magnetic:
                continue
            orbit_dict[item.label.raw_value] = item.get_orbit()
        return orbit_dict

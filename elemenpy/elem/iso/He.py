"""
Helium chemical element isotopes.

Package:
  RoadNarrows elemenpy python package.

File:
  He.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

from elemenpy.core.format import (default_encoder)
from elemenpy.core.constants import (AYearOfSeconds)

from elemenpy.sm.electriccharge import (ElectricCharge)
from elemenpy.sm.spin import (SpinQuantumNumber)

from elemenpy.elem.elements import (ElementZ, z_to_z, z_to_name, z_to_symbol,
                                    ElementGroup, ElementPeriod, ElementBlock,
                                    ElementCategory, ElementSubcategory)
from elemenpy.elem.nucleardecay import (NuclearDecay)
from elemenpy.elem.orbital import (ElectronOrbital)
from elemenpy.elem.electroncloud import (ElectronCloud)

from elemenpy.elem.isotope import (Isotope)

# -----------------------------------------------------------------------------
# He4 Class
# -----------------------------------------------------------------------------
class He4(Isotope):
  """ Helium-4 isotope. """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = z_to_z(ElementZ.HELIUM)   # atomic number: number of protons
  A = 4                         # mass number: protons+neutrons(baryon number B)
  N = A - Z                     # number of neutrons

  ## fixed isotope properties
  Name        = z_to_name(Z)
  Symbol      = z_to_symbol(Z)
  SymbolA     = default_encoder(f'$sup({A}){Symbol}')
  Group       = ElementGroup(18)
  Period      = ElementPeriod(1)
  Block       = ElementBlock('s')
  Category    = ElementCategory.NONMETAL
  Subcategory = ElementSubcategory.NOBLE_GAS
  QSpin       = SpinQuantumNumber(0)

  ElectronCfgGroundState = [ElectronOrbital(1, 's', 2)]

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
 
  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_isotope_properties(indent=indent, **print_kwargs)
 
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
 
  def __init__(self, label=None):
    """
    Initializer.

    Parameters:
      label     Label this isotope instance. If None, then no label.
                If 'auto', then random string prefaced by symbol.
    """
    Isotope.__init__(self, label=label)

# -----------------------------------------------------------------------------
# He3 Class
# -----------------------------------------------------------------------------
class He3(He4):
  """ Helium-3 isotope. """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = He4.Z                     # atomic number: number of protons
  A = 3                         # mass number: protons+neutrons(baryon number B)
  N = A - Z                     # number of neutrons

  ## fixed isotope properties
  SymbolA   = default_encoder(f'$sup({A}){He4.Symbol}')
  AltName   = 'helion'
  QSpin     = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
 
  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_isotope_properties(indent=indent, **print_kwargs)
 
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
 
  def __init__(self, label=None):
    """
    Initializer.

    Parameters:
      label     Label this isotope instance. If None, then no label.
                If 'auto', then random string prefaced by symbol.
    """
    Isotope.__init__(self, label=label)


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  from os.path import (basename, splitext)
  import tests.utBolognium as ut

  this_iso_test = splitext(basename(__file__))[0].lower()

  sys.exit(ut.utmain(this_iso_test))

"""
Boron chemical element isotopes.

Package:
  RoadNarrows elemenpy python package.

File:
  B.py

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
# B11 Class
# -----------------------------------------------------------------------------
class B11(Isotope):
  """ Boron-11 isotope. """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = z_to_z(ElementZ.BORON)    # atomic number: number of protons
  A = 11                        # mass number: protons+neutrons(baryon number B)
  N = A - Z                     # number of neutrons

  ## fixed isotope properties
  Name        = z_to_name(Z)
  Symbol      = z_to_symbol(Z)
  SymbolA     = default_encoder(f'$sup({A}){Symbol}')
  Group       = ElementGroup(13)
  Period      = ElementPeriod(2)
  Block       = ElementBlock('p')
  Category    = ElementCategory.METALLOID
  Subcategory = ElementSubcategory.METALLOID
  QSpin       = SpinQuantumNumber(3, 2)

  ElectronCfgGroundState = [
    ElectronOrbital(1, 's', 2),
    ElectronOrbital(2, 's', 2),
    ElectronOrbital(2, 'p', 1)
  ]

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
# B10 Class
# -----------------------------------------------------------------------------
class B10(B11):
  """ Boron-10 isotope. """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = B11.Z                     # atomic number: number of protons
  A = 10                        # mass number: protons+neutrons(baryon number B)
  N = A - Z                     # number of neutrons

  ## fixed isotope properties
  SymbolA     = default_encoder(f'$sup({A}){B11.Symbol}')
  QSpin       = SpinQuantumNumber(3)

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

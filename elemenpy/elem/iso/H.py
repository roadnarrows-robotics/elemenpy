"""
Hydrogen chemical element isotopes.

Package:
  RoadNarrows elemenpy python package.

File:
  H.py

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
# H1 Class
# -----------------------------------------------------------------------------
class H1(Isotope):
  """ Hydrogen-1 isotope. """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = z_to_z(ElementZ.HYDROGEN) # atomic number: number of protons
  A = 1                         # mass number: protons+neutrons(baryon number B)
  N = A - Z                     # number of neutrons

  ## fixed isotope properties
  Name        = z_to_name(Z)
  Symbol      = z_to_symbol(Z)
  SymbolA     = default_encoder(f'$sup({A}){Symbol}')
  AltName     = 'protium'
  AltSymbol   = ''
  Group       = ElementGroup(1)
  Period      = ElementPeriod(1)
  Block       = ElementBlock('s')
  Category    = ElementCategory.NONMETAL
  Subcategory = ElementSubcategory.REACTIVE_NONMETAL
  QSpin       = SpinQuantumNumber(1, 2)

  ElectronCfgGroundState = [ElectronOrbital(1, 's', 1)]

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
# H2 Class
# -----------------------------------------------------------------------------
class H2(H1):
  """ Hydrogen-2 isotope. """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = H1.Z                      # atomic number: number of protons
  A = 2                         # mass number: protons+neutrons(baryon number B)
  N = A - Z                     # number of neutrons

  ## fixed isotope properties
  SymbolA   = default_encoder(f'$sup({A}){H1.Symbol}')
  AltName   = 'deuterium'
  AltSymbol = 'D'
  QSpin     = SpinQuantumNumber(1)

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
# H3 Class
# -----------------------------------------------------------------------------
class H3(H1):
  """ Hydrogen-3 isotope. """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = H1.Z                      # atomic number: number of protons
  A = 3                         # mass number: protons+neutrons(baryon number B)
  N = A - Z                     # number of neutrons

  ## fixed isotope properties
  SymbolA   = default_encoder(f'$sup({A}){H1.Symbol}')
  AltName   = 'tritium'
  AltSymbol = 'T'
  QSpin     = SpinQuantumNumber(1, 2)
  Decay     = NuclearDecay(mode='beta_decay', halflife=12.32*AYearOfSeconds)

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

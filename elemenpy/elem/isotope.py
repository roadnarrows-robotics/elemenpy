"""
Chemical isotope archetype base class.

Package:
  RoadNarrows elemenpy python package.

File:
  isotope.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

from enum import (Enum)

from elemenpy.core.common import (enum_to_str, enumfactory, randomstring)
from elemenpy.core.format import (Format, default_encoder, Format4Some)
from elemenpy.core.prettyprint import (print2cols, print_to_str)

from elemenpy.sm.electriccharge import (ElectricCharge)
from elemenpy.sm.spin import (SpinQuantumNumber)

from elemenpy.elem.elements import (ElementZ, ElementGroup, ElementPeriod,
                                    ElementBlock, ElementCategory,
                                    ElementSubcategory, z_to_z)
from elemenpy.elem.atomicnucleus import (AtomicNucleus)
from elemenpy.elem.nucleardecay import (NuclearDecay)
from elemenpy.elem.orbital import (ElectronOrbital)
from elemenpy.elem.electroncloud import (ElectronCloud)

# -----------------------------------------------------------------------------
# Isotope Class
# -----------------------------------------------------------------------------
class Isotope:
  """
  The element isotop archetype base class. All elemental isotopes
  are derived from this class.
  """
  #
  # Class Fixed Properties
  #

  # isotope defining numbers
  Z = z_to_z(ElementZ.UNKNOWN)  # atomic number: number of protons
  A = 0                       # mass number: protons+neutrons (baryon number B)
  N = A - Z                   # number of neutrons

  ## fixed isotope properties
  Name        = 'unobtainium'               # standard name of element
  Symbol      = default_encoder(f'$greek(Upsilon)')   # element symbol
  SymbolA     = default_encoder(f'$sup({A}){Symbol}') # symbol with super
  AltName     = ''                          # alternative name
  AltSymbol   = ''                          # alternative symbol
  Group       = ElementGroup.UNKNOWN        # element group (column)
  Period      = ElementPeriod.UNKNOWN       # element period (row)
  Block       = ElementBlock.UNKNOWN        # element block (region)
  Category    = ElementCategory.UNKNOWN     # element chemical category
  Subcategory = ElementSubcategory.UNKNOWN  # element chemical subcategory
  QSpin       = SpinQuantumNumber(0)        # intrinsic spin quantum number
  Decay       = NuclearDecay()              # spontaneous decay

  ElectronCfgGroundState = [] # electron ground state configuration (min energy)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def default_fqname(klass):
    """
    Return class default fully-qualified standard name of element.

    fully-qualified name: Name-A
    """
    return f"{klass.Name}-{klass.A}"

  @classmethod
  def default_group_name(klass):
    """ Return class default group name. """
    return enum_to_str(klass.Group, sep=' ')

  @classmethod
  def default_period_name(klass):
    return enum_to_str(klass.Period, sep=' ')

  @classmethod
  def default_block_name(klass):
    return f"{klass.Block.value}-block"

  @classmethod
  def default_category_name(klass):
    return enum_to_str(klass.Category, sep='-')

  @classmethod
  def default_subcategory_name(klass):
    return enum_to_str(klass.Subcategory, sep='-')

  @classmethod
  def symbol_notation(klass, charge=0, count=1, fmt=Format.UNICODE):
    """
    Create isotopic element full symbol notation formatted string.

    Output format:
      A  q
       Sy 
      Z  n

      where:
        Sy  - standard 1/2 letter element symbol
        A   - atomic mass
        Z   - atomic number
        q   - charge
        n   - count

    Parameters:
      klass   Isotope (derived) class.
      charge  If not zero, include cation/anion right superscript.
      count   If > 1, include right count subscript.
      fmt     Output string format. See the enum Format. The value
              may also be the Formate integer or string equivalent
              (e.g. 1, 'html', "HTML").

    Returns:
      Formatted string.
    """
    fmt = enumfactory(Format, fmt)

    lsup = f"$sup({klass.A})"
    lsub = f"$sub({klass.Z})"

    if charge < -1:
      rsup = f"$sup({-charge}-)"
    elif charge == -1:
      rsup = "$sup(-)"
    elif charge == 1:
      rsup = "$sup(+)"
    elif charge > 1:
      rsup = f"$sup({charge}+)"
    else:
      rsup = ""

    if count > 1:
      rsub = f"$sub({count})"
    else:
      rsub = ""

    encode = Format4Some(lsup+lsub+f"{klass.Symbol}"+rsup+rsub)

    return encode[fmt]

  @classmethod
  def print_isotope_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed element isotope base properties using 
    the default encoder.

    Parameters:
      klass         Isotope (derived) class.
      indent        Line indentation.
      print_kwargs  Python3 print() keyword arguments.
    """
    if str(klass.Decay) == 'stable':
      decaylines = 'stable'
    else:
      decaylines = print_to_str(klass.Decay.print_properties,
                                indent=indent+2, **print_kwargs)

    print2cols([
      ('Name(s)',       f"{klass.default_fqname()} {klass.AltName}"),
      ('Symbol(s)',     f"{klass.SymbolA} {klass.AltSymbol}"),
      ('Atomic Mass',   klass.A),
      ('Atomic Number', klass.Z),
      ('Neutrons',      klass.N),
      ('Group',         f"group {klass.Group.value} "\
                        f"({klass.default_group_name()})"),
      ('Period',        f"{klass.default_period_name()}"),
      ('Block',         klass.default_block_name()),
      ('Category',      klass.default_category_name()),
      ('Subcategory',   klass.default_subcategory_name()),
      ('Spin',          klass.QSpin.notation()),
      ('Decay',         f"{decaylines}"),
      ('Ground State',  ElectronCloud.electron_config_notation(
                                              klass.ElectronCfgGroundState)),
      ], indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, label=None):
    """
    Initializer.

    Parameters:
      label     Label this isotope instance.
                If None, then no label.
                If 'auto', then random string prefaced by symbol.
    """
    if not label:
      self._label = ''
    elif label == 'auto':
      self._label = randomstring(12, prefix=self.Symbol+'_')
    else:
      self._label = label

    self._nucleus = AtomicNucleus(self.Z, self.A)
    self._cloud   = ElectronCloud(self.ElectronCfgGroundState)

  def __repr__(self):
    """ Note use var!r for arguments to preserve strings, list, etc. """
    return f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return self.fqname

  @property
  def atomic_number(self):
    """ Return atomic number. """
    return self.Z

  @property
  def mass_number(self):
    """ Return mass number. """
    return self.A

  @property
  def neutrons(self):
    """ Return neutron number. """
    return self.N

  @property
  def name(self):
    """
    Return standard name of element.

    Returns:
      String.
    """
    return self.Name

  @property
  def fqname(self):
    """
    Return fully-qualified standard name of element.

    Name-A

    Returns:
      String.
    """
    return f"{self.Name}-{self.A}"

  @property
  def symbol(self):
    """
    Return standard symbol of element.

    Returns:
      String.
    """
    return self.Symbol

  @property
  def symbola(self):
    """
    Return standard element symbol adorned with mass number A.

    Returns:
      String.
    """
    return self.SymbolA

  @property
  def altname(self):
    """
    Return alternative name of element.

    Returns:
      String (empty string if no alternative).
    """
    return self.AltName

  @property
  def altsymbol(self):
    """
    Return alternative symbol of element.

    Returns:
      String (empty string if no alternative).
    """
    return self.AltSymbol

  @property
  def group(self):
    return self.Group.value

  @property
  def group_name(self):
    return self.default_group_name()

  @property
  def period(self):
    return self.Period.value

  @property
  def period_name(self):
    return self.default_period_name()

  @property
  def block(self):
    return self.Block.value

  @property
  def block_name(self):
    return self.default_block_name()

  @property
  def category(self):
    return self.Category.value

  @property
  def category_name(self):
    return self.default_category_name()

  @property
  def subcategory(self):
    return self.Subcategory.value

  @property
  def subcategory_name(self):
    return self.default_subcategory_name()

  @property
  def label(self):
    return self._label

  @property
  def nucleus(self):
    return self._nucleus

  @property
  def electron_cloud(self):
    return self._cloud

  def electric_charge(self):
    """ Return current ElectricCharge(). """
    return self.electron_cloud.electric_charge() + self.Z

  def print_state(self, indent=0,**print_kwargs):
    """
    Print the current state of this instance (atom).

    Parameters:
      indent        Line indentation.
      print_kwargs  Python3 print() keyword arguments.
    """
    cloudlines = print_to_str(self.electron_cloud.print_state,
                              indent=indent+2, **print_kwargs)

    print2cols([
      ('Label',           f"{self.label}"),
      ('Electric Charge', f"{self.electric_charge()}"),
      ('Nucleus',         f"{self.nucleus}"),
      ('Electron Cloud',  '\n'+cloudlines),
      ], indent=indent, **print_kwargs)


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utisotope as ut

  sys.exit(ut.utmain())

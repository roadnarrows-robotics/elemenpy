"""
Atomic Nucleus.

See:
  https://en.wikipedia.org/wiki/Atomic_nucleus
  https://en.wikipedia.org/wiki/Nuclear_structure
  https://en.wikipedia.org/wiki/Nuclear_isomer

Package:
  RoadNarrows elemenpy package.

File:
  atomicnucleus.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

import sys
import math
from enum import (Enum)
from copy import (copy)

from elemenpy.core.common import (enumfactory)
from elemenpy.core.format import (Format, Format4Some, default_encoder)
from elemenpy.core.prettyprint import (print2cols)

from elemenpy.elem.elements import (z_to_name, z_to_symbol)

# -----------------------------------------------------------------------------
# AtomicNucleus Class
# -----------------------------------------------------------------------------
class AtomicNucleus:
  """ Atomic nucleus class. """

  def __init__(self, Z, A, name='auto', symbol='auto', embedded=None):
    """
    Initializer.

    RDK: excited states, energies?

    Parameters:
      Z           Atomic number.
      A           Mass number.
      name        Assigned name to nucleus (e.g 'alpha').
                  If auto, then try element name with Z value.
                  Fallback is 'nucleus'
      symbol      Assinged symbol.
                  If auto, then try element symobol with Z value.
                  Fallback is the script capital N.
      embedded    Nucleus embedded in given isotope. Default is a free nucleus.
    """
    self._Z = Z
    self._A = A
    self._N = self._A -  self._Z  # number of neutrons
   
    if name == 'auto':
      try:
        self._name = z_to_name(self._Z)
      except:
        self._name = 'nucleus'
    else:
      self._name = name

    if symbol == 'auto':
      try:
        self._symbol = z_to_symbol(self._Z)
      except:
        self._symbol = default_encoder('$script(N)')
    else:
      self._symbol = symbol

    self._fqsymbol  = self.notation()
    self._embedded  = embedded

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self._Z!r}, {self._A!r}, name={self._name!r}, "\
            f"symbol={self._symbol!r}, embedded={self._embedded!r})"

  def __str__(self):
    return self.fqname

  @property
  def Z(self):
    """ Return atomic number. """
    return self._Z

  @property
  def A(self):
    """ Return mass number. """
    return self._A

  @property
  def N(self):
    """ Return neutron number. """
    return self._N

  @property
  def name(self):
    """ Return assigned name of the nucleus. """
    return self._name

  @property
  def fqname(self):
    """
    Return fully-qualified standard name of nucleus.

    Name-A

    Returns:
      String.
    """
    return f"{self.name}-{self.A}"

  @property
  def symbol(self):
    """ Return symbol of the nucleus. """
    return self._symbol

  @property
  def fqsymbol(self):
    """ Return symbol of the nucleus. """
    return self._fqsymbol

  @property
  def embedded(self):
    """ Return nucleus embedding. """
    return self._embedded

  def copy(self):
    """ AtomicNucleus.copy() -> shallow copy of AtomicNucleus. """
    return copy(self)

  def notation(self, fmt=Format.UNICODE):
    """
    Create nucleus notation formatted string.

    Output format:
      zB   (plain)

      a
        B
      z    (unicode, html, latex)

      where:
        B   - symbol base string
        z   - atomic number
        a   - mass number

    Parameters:
      fmt   - Output string format. See the enum Format. The value may also
              be the Format integer or string equivalent (e.g. 1, 'html')

    Returns:
      Formatted string.
    """
    fmt = enumfactory(Format, fmt)
    encode = Format4Some(f"$sup({self._A})$sub({self._Z}){self._symbol}")
    return encode[fmt]

  def print_properties(self, indent=0, **print_kwargs):
    """
    Print nucleus fixed properties.

    Paramters:
      indent          Line indentation.
      print_kwargs    Python3 print() keyword arguments.
    """
    print2cols([
      ('Name',          self.name),
      ('Symbol',        self.fqsymbol),
      ('Atomic Mass',   self.A),
      ('Atomic Number', self.Z),
      ('Neutrons',      self.N),
      ], indent=indent, **print_kwargs)

  def print_state(self, indent=0, **print_kwargs):
    """
    Print the current state of the nucleus.

    Parameters:
      indent        Line indentation.
      print_kwargs  Python3 print() keyword arguments.
    """
    pass

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utatomicnucleus as ut

  sys.exit(ut.utmain())

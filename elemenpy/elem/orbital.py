"""
Electron orbitals.

Package:
  RoadNarrows elemenpy package.

File:
  orbitals.py

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

from elemenpy.core.common import (enumfactory)
from elemenpy.core.format import (Format, Format4Some)

# -----------------------------------------------------------------------------
# Subshell Enumeration
# -----------------------------------------------------------------------------
class Subshell(Enum):
  """ Electron orbital subshell azimuthal quantum number. """
  s   = 0
  p   = 1
  d   = 2
  f   = 3
  g   = 4
  h   = 5
  i   = 6

# -----------------------------------------------------------------------------
# ElectronOrbital Class
# -----------------------------------------------------------------------------
class ElectronOrbital:
  """ Electron subshell orbital class. """

  def __init__(self, n, l, e):
    """
    Initializer.

    Parameters:
      n   Principle quantum number. Integer > 0.
      l   Azimuthal quantum number (ell). [0,6].
      e   Number of electrons in subshell.
    """
    self.n = n
    self.l = l
    self.e = e

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self._n!r}, {self._l.name!r}, {self._e!r})"

  def __str__(self):
    return self.notation()

  def max_shell_electrons(self, n):
    """ Return maximum number of electrons for this shell. """
    return 2 * self._n * self._n

  def max_subshell_electrons(self):
    """ Return maximum number of electrons for this subshell. """
    return 2 * (2 * self._l.value + 1)

  def principle_quantum_number(self, n=None):
    """
    Get/set the shell principle quantum number.
    
    An alternative route to the n getter/setter property.

    Parameters:
      n   If not None, then the new value of n.

    Returns:
      The (new) principle quantum number.
    """
    if n is not None:
      self.n = n
    return self.n

  def azimuthal_quantum_number(self, l=None):
    """
    Get/set the subshell azimuthal quantum number.
    
    An alternative route to the l getter/setter property.

    Parameters:
      l   If not None, then the new value of l.

    Returns:
      The (new) azimuthal quantum number.
    """
    if l is not None:
      self.l = l
    return self.l

  def electrons(self, e=None):
    """
    Get/set the number of subshell electrons.
    
    An alternative route to the e getter/setter property.

    Parameters:
      e   If not None, then the new value of e.

    Returns:
      The (new) electron count.
    """
    if e is not None:
      self.e = e
    return self.e

  def notation(self, fmt=Format.UNICODE):
    """
    Create electron orbital notation formatted string.

    Output format:
      nle   (plain)

        e
      nl    (unicode, html, latex)

      where:
        n   shell number (principle quantum number)
        l   subshell designation (maps to azimuthal quantom number)
        e   number of electrons in subshell

    Parameters:
      fmt   Output string format. See the enum Format. The value may also
            be the Format integer or string equivalent (e.g. 3, 'latex')

    Returns:
      Formatted string.
    """
    fmt = enumfactory(Format, fmt)
    encode = Format4Some(f"{self._n}{self._l.name}$sup({self._e})")
    return encode[fmt]

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Get/set properties
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  @property
  def n(self):
    """ Get the principle quantum number. """
    return self._n

  @n.setter
  def n(self, n):
    """ Set the principle quantum number. """
    i = int(n)
    if i < 1:
      raise ValueError(f"{i} invalid principle quantum number")
    self._n = n

  @property
  def l(self):
    """ Get the azimuthal quantum number. """
    return self._l

  @l.setter
  def l(self, l):
    """ Set the azimuthal quantum number. """
    self._l = enumfactory(Subshell, l)

  @property
  def e(self):
    """ Get subshell's current electron count. """
    return self._e

  @e.setter
  def e(self, e):
    """ Set subshell's new electron count. """
    if e < 0 or e > self.max_subshell_electrons():
      raise ValueError(
          f"{e} electrons out-of-range for {self._l.name} subshell")
    self._e = e

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utorbital as ut

  sys.exit(ut.utmain())

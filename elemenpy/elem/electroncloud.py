"""
Atomic orbital model - the electron cloud.

See:
  https://en.wikipedia.org/wiki/Atomic_orbital
  https://en.wikipedia.org/wiki/Ionization

Package:
  RoadNarrows elemenpy package.

File:
  electroncloud.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

from copy import (copy, deepcopy)

from elemenpy.core.format import (Format)
from elemenpy.core.prettyprint import (print2cols)

from elemenpy.sm.electriccharge import (ElectricCharge)

from elemenpy.elem.orbital import (Subshell, ElectronOrbital)

# -----------------------------------------------------------------------------
# ElectronCloud Class
# -----------------------------------------------------------------------------
class ElectronCloud:
  """ Atomic electron cloud class. """

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
 
  @classmethod
  def electron_config_notation(klass, cfg, fmt=Format.UNICODE):
    """
    Create electron configuration notation formatted string.

    Output format:
      orb_0orb_1...

      where:
        orb_k - kth orbital subshell of form:

        nle   (plain)

          e
        nl    (unicode, html, latex)

      with:
        n   shell number (principle quantum number)
        l   subshell designation (maps to azimuthal quantom number)
        e   number of electrons in subshell

    Parameters:
      cfg   Iterable object of ElectronOrbital instances.
      fmt   Output string format. See the enum Format. The value
            may also be the Format integer or string equivalent.

    Returns:
      Formatted string.
    """
    s = ''
    for subshell in cfg:
      s += subshell.notation(fmt)
    return s

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def __init__(self, ground_state):
    """
    Initializer.

    Parameters:
      ground_state    Atomic (ion) orbitals ground state list.
    """
    self._ground_state = ground_state
    self._orbitals  = deepcopy(self._ground_state) 

  def __repr__(self):
    gs = self.electron_config_notation(self._ground_state)
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({gs!r})"

  def __str__(self):
    return self.electron_config_notation(self._orbitals)

  @property
  def ground_state(self):
    return self._ground_state

  @property
  def orbitals(self):
    return self._orbitals

  def copy(self):
    """ ElectronCloud.copy() -> just deep enough copy of ElectronCloud. """
    # TODO
    return copy(self)

  def electric_charge(self):
    q = 0
    for orb in self.orbitals:
      q -= orb.e
    return ElectricCharge(q)

  def ionize(self, de):
    """
    Ionize.

    TODO: Lots of work to do here.

    Parameters:
      de    Plus/minus delta electrons.
    """
    pass

  def excite(self, x):
    """
    Excite the cloud.

    TODO: Lots of work to do here.

    Parameters:
      x     Rah, rah, rah.
    """
    pass

  def print_properties(self, indent=0, **print_kwargs):
    """
    Print cloud fixed properties.

    Paramters:
      indent          Line indentation.
      print_kwargs    Python3 print() keyword arguments.
    """
    print2cols([
      ('Ground State',  self.electron_config_notation(self.ground_state)),
      ], indent=indent, **print_kwargs)

  def print_state(self, indent=0,**print_kwargs):
    """
    Print the current state of the cloud.

    Parameters:
      indent        Line indentation.
      print_kwargs  Python3 print() keyword arguments.
    """
    print2cols([
      ('Orbitals',  self.electron_config_notation(self.orbitals)),
      ('Electrons', self.electric_charge().inverse()),
      ], indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utelectroncloud as ut

  sys.exit(ut.utmain())

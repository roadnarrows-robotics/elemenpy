"""
Spin Quantum Number.

TODO:
  1. Add check() function to test if spin transition is valid.

Package:
  RoadNarrows elemenpy package.

File:
  spin.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

from elemenpy.core.format import (Format)
from elemenpy.core.rational import (Q)

# -----------------------------------------------------------------------------
# SpinQuantumNumber Class
# -----------------------------------------------------------------------------
class SpinQuantumNumber(Q):
  """ Intrinsic spin quantum number class. """

  iseven = lambda k: k % 2 == 0
  isodd  = lambda k: k % 2 == 1

  def __init__(self, n, d=1):
    """
    Initializer.

    Parameters:
      n   - Spin integer numerator.
      d   - Spin integer denomenator.
    """
    Q.__init__(self, n, d) 

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.p!r}, {self.q!r})"

  def __str__(self):
    return self.notation()

  @classmethod
  def from_nucleons(klass, protons, neutrons):
    """
    QuantumSpin class instance factory method.

    Note: This doesn't really work yet. I need more research.

    Parameters:
      protons   - Number of nucleus protons.
      neutrons  - Number of nucleus neutrons.

    Returns:
      (Derived) QuantumSpin class instance.
    """
    # no spin
    if klass.iseven(protons) and klass.iseven(neutrons):
      return klass(0)
    # half spin
    elif klass.isodd(protons + neutrons):
      return klass(1, 2)
    # integral spin
    elif klass.isodd(protons) and klass.isodd(neutrons):
      return klass(1)
    else:
      raise ValueError(
        f"cannot determine spin from {protons} protons and {neutrons} neutrons")

  def notation(self, fmt=Format.UNICODE):
    """
    Create electron orbital notation formatted string.

    Output format:
      +n/d   (plain)

       n
      + /    (unicode, html, latex)
        d 

      where:
        n   - numerator
        d   - denomenator

    Parameters:
      fmt   - Output string format. See the enum Format. The value may also
              be the Format integer or string equivalent
              (e.g. 1, 'plain').

    Returns:
      Formatted string.
    """
    if self > 0:
      return '+' + Q.notation(self, fmt)
    else:
      return Q.notation(self, fmt)

  #def delta(self, i):
  #  """ Change spin quantum number by an integral amount. """
  #  self._sqn += int(i)

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utspin as ut

  sys.exit(ut.utmain())

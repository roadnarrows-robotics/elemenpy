"""
Electric charge.

TODO:
  1. Add check() function to test if charge transition is valid.

Package:
  RoadNarrows elemenpy package.

File:
  electriccharge.py

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
# ElectricCharge Class
# -----------------------------------------------------------------------------
class ElectricCharge(Q):
  """ Electric charge class. """

  def __init__(self, n, d=1):
    """
    Initializer.

    Parameters:
      n   Electric charge integer numerator.
      d   Electric charge integer denomenator.
    """
    Q.__init__(self, n, d) 

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.p!r}, {self.q!r})"

  def __str__(self):
    return self.notation()

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
      fmt   Output string format. See the enum Format. The value may also
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
  import tests.utelectriccharge as ut

  sys.exit(ut.utmain())

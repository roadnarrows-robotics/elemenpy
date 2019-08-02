"""
Quantum Chromodynamics (QCD) color charge of quarks and gluons.

Package:
  RoadNarrows elemenpy package.

File:
  colorcharge.py

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

from elemenpy.sm.standardmodel import (StandardModel as sm)
from elemenpy.core.common import (enumfactory, static_vars)
from elemenpy.core.format import (Format, Format4Some, default_encoder)

# -----------------------------------------------------------------------------
# QCD ColorCharge Class
# -----------------------------------------------------------------------------
class ColorCharge:
  """ Color charge class. """

  class QCDColor(Enum):
    """ QCD color. """
    UNKNOWN   = '?'

    RED       = 'R' # red
    GREEN     = 'G' # green
    BLUE      = 'B' # blue

    ANTIRED   = 'C' # antired
    ANTIGREEN = 'M' # antigreen
    ANTIBLUE  = 'Y' # antiblue 

    CYAN      = 'C' # antired synonym
    MAGENTA   = 'M' # antigreen synonym
    YELLOW    = 'Y' # antiblue synonym

    @staticmethod
    def from_value(value):
      """
      QCD ColorCharge.QCDColor factory enumeration method.

      Create color enumeration from value.

      Parameters:
        value   Value object used to map to enum. One of type:
                  enum, str, int.
                For str, long or short spellings in upper or lower
                case are supported.
                Example values for mapped ColorCharge.QCDColor.BLUE:
                  'B', 'blue', ord('B'), ColorCharge.QCDColor.BLUE

      Returns:
        ColorCharge.QCDColor enum.
      """
      if isinstance(value, Enum):
        return enumfactory(ColorCharge.QCDColor, value)
      elif isinstance(value, str):
        return ColorCharge.Name2Color[value.lower()]
      else:
        return enumfactory(ColorCharge.QCDColor, chr(value))

    @staticmethod
    def is_primary_color(value):
      """ Test if value is a QCD primary color. """
      color = ColorCharge.QCDColor.from_value(value)
      return color in ColorCharge.PrimaryColors

    @staticmethod
    def is_anticolor(value):
      """ Test if value is a QCD anticolor. """
      color = ColorCharge.QCDColor.from_value(value)
      return color in ColorCharge.AntiColors

    @staticmethod
    def complement(value):
      """ Return the QCD color complement of value. """
      color = ColorCharge.QCDColor.from_value(value)
      return ColorCharge.ColorPairs[color]

  # set of primary colors
  PrimaryColors = [QCDColor.RED, QCDColor.GREEN, QCDColor.BLUE]

  # set of anticolors
  AntiColors = [QCDColor.ANTIRED, QCDColor.ANTIGREEN, QCDColor.ANTIBLUE]

  # color-anticolor complementary pairs
  ColorPairs = {
    QCDColor.UNKNOWN:     QCDColor.UNKNOWN,
    QCDColor.RED:         QCDColor.ANTIRED,
    QCDColor.GREEN:       QCDColor.ANTIGREEN,
    QCDColor.BLUE:        QCDColor.ANTIBLUE,
    QCDColor.ANTIRED:     QCDColor.RED,
    QCDColor.ANTIGREEN:   QCDColor.GREEN,
    QCDColor.ANTIBLUE:    QCDColor.BLUE,
  }

  # color to standard name lookup dictionary
  Color2Name = {
    QCDColor.UNKNOWN:     'unknown',
    QCDColor.RED:         'red',
    QCDColor.GREEN:       'green',
    QCDColor.BLUE:        'blue',
    QCDColor.ANTIRED:     'antired',
    QCDColor.ANTIGREEN:   'antigreen',
    QCDColor.ANTIBLUE:    'antiblue',
  }

  # name to color lookup dictionary
  Name2Color = {
    # standard long names
    'red':        QCDColor.RED,
    'green':      QCDColor.GREEN,
    'blue':       QCDColor.BLUE,
    'antired':    QCDColor.ANTIRED,
    'antigreen':  QCDColor.ANTIGREEN,
    'antiblue':   QCDColor.ANTIBLUE,

    # short names
    'r':  QCDColor.RED,
    'g':  QCDColor.GREEN,
    'b':  QCDColor.BLUE,
    'c':  QCDColor.ANTIRED,
    'm':  QCDColor.ANTIGREEN,
    'y':  QCDColor.ANTIBLUE,

    # alternate anticolor long names
    'cyan':     QCDColor.ANTIRED,
    'magenta':  QCDColor.ANTIGREEN,
    'yellow':   QCDColor.ANTIBLUE,
  }

  # color to symbol key used in symbol lookups
  Color2SymKey = {
    QCDColor.UNKNOWN:    '?',
    QCDColor.RED:        '$sm(R)',
    QCDColor.GREEN:      '$sm(G)',
    QCDColor.BLUE:       '$sm(B)',
    QCDColor.ANTIRED:    '$sm(R-bar)',
    QCDColor.ANTIGREEN:  '$sm(G-bar)',
    QCDColor.ANTIBLUE:   '$sm(B-bar)',
  }

  def __init__(self, color):
    """
    Initializer.

    Parameters:
      color   QCD charge color.
    """
    self.color = color

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.name!r})"

  def __str__(self):
    return self.symbol

  def __eq__(self, value):
    """ Equal to. self == value. """
    v = ColorCharge(value)
    return self.color == v.color

  def __ne__(self, value):
    """ Not equal to. self == value. """
    v = ColorCharge(value)
    return self.color != v.color

  @property
  def name(self):
    """ Return color standard name string. """
    return ColorCharge.Color2Name[self.color]

  @property
  def symbol(self):
    """ Return color symbol encoded in default encoding. """
    return default_encoder(ColorCharge.Color2SymKey[self.color])

  @property
  def color(self):
    """ Return color charge. """
    return self._color

  @color.setter
  def color(self, value):
    """
    Set color charge.

    Parameters:
      value   Valid string, enum, or numeric value that can be mapped
              to a color charge enumeration.
    """
    if isinstance(value, ColorCharge):
      self._color = value.color
    else:
      self._color = ColorCharge.QCDColor.from_value(value)

  @property
  def complement(self):
    """ Return complement of this color charge. """
    return ColorCharge(ColorCharge.ColorPairs[self._color])

  def is_primary_color(self):
    """ Test if this charge is a QCD primary color. """
    return self._color in ColorCharge.PrimaryColors

  def is_anticolor(self):
    """ Test if this charge is a QCD anticolor. """
    return self._color in ColorCharge.AntiColors

  def notation(self, fmt=Format.UNICODE):
    """
    Create color charge notation formatted string.

    Output format:
      C 

      where:
        C   - Color R,G,B or R,G,C bar

    Parameters:
      fmt   Output string format. See the enum Format. The value may also
            be the Format integer or string equivalent
            (e.g. 1, 'plain').

    Returns:
      Formatted string.
    """
    encode = Format4Some(ColorCharge.Color2SymKey[self.color])
    return encode[enumfactory(Format, fmt)]


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utcolorcharge as ut

  sys.exit(ut.utmain())

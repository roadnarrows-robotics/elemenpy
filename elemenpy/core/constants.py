"""
Physics, chemistry, and some math constants.

Package:
  RoadNarrows elemenpy package.

File:
  constants.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

import math

from elemenpy.core.format import (latex_encoder,
                                  unicode_encoder,
                                  default_encoder)


AYearOfSeconds = 31556952.0 # based on an average year of 365.2425 days

# -----------------------------------------------------------------------------
# Class Constant
# -----------------------------------------------------------------------------
class Constant(float):
  """
  Constant class.

  Basically a Constant is a float with read-only attributes.
  Also note that some float operation will replace a Constant
  (delete Constant then create new non-Constant object).
    Examples: self = 5  self += 99.9, etc
  """
  def __new__(klass, *args, **kwargs):
    """
    Contructor.

    Parameters:
      args    Arguments. First argument is the float value.
      kwargs  Optional keyword arguments

    Returns:
      Constant instance.
    """
    instance = super(Constant, klass).__new__(klass, args[0])
    return instance

  def __init__(self, value, symbol, **kwargs):
    """
    Initializer.

    Parameters:
      value   The value of the constant.
      symbol  The plain-text symbol of the constant.
      kwargs  Optional keyword arguments:
        desc      Descriptive string of constant.
        units     The units of the constant.
    """
    float.__init__(value)

    # read-only attributes
    self._value   = value   # shadow value
    self._symbol  = symbol
    self._desc    = kwargs.get('desc', 'no description')
    self._units   = kwargs.get('units', 'unspecified')

  def __call__(self):
    """ Return constant value. """
    return self.value

  def print_info(self, **print_kwargs):
    """
    Print constant information.

    Parameters:
      print_kwargs  Any print() control keyword arguments.
    """
    print(f"""\
symbol:       {self.symbol}
constant:     {self}
description:  {self.desc}
units:        {self.units}""", **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Properties
  # Note: Without a setter property, a property is read-only.
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  @property
  def value(self):
    """ Return constant value v. """
    return self._value

  @property
  def symbol(self):
    """ Return constant default symbol. """
    return self._symbol

  @property
  def units(self):
    """ Return units of the constant. """
    return self._units

  @property
  def desc(self):
    """ Return description of the constant. """
    return self._desc

  # pre-parsed physics symbols table
  PhyMappingPre = {
    'c':      'c',                      # speed of light
    'G':      'G',                      # gravitational constant
    'k_B':    'k$sub(B)',               # Boltmann constant
    'e_0':    '$greek(epsilon)$sub(0)', # permittivity of vacuum
    'h':      '\u210e',                 # Planck constant
    'h-bar':  '\u210f',                 # reduced Planck constant
    'l_P':    'l$sub(p)',               # Planck length
    't_P':    't$sub(p)',               # Planck time
    'm_P':    'm$sub(p)',               # Planck mass
    'q_P':    'q$sub(p)',               # Planck charge
    'T_P':    'T$sub(p)',               # Planck temperature
    'alpha':  '$greek(alpha)',          # fine-structure constant
  }

  def make_mapping(pre):
    post  = {}
    for key,expr in pre.items():
      post[key] = default_encoder(expr)
    if default_encoder.encoding == 'latex':
      # latex fixups
      PhyMapping['h']      = 'h'
      PhyMapping['h-bar']  = '\\hbar'
    return post

  if not default_encoder.has_table('phy'):
    PhyMapping = make_mapping(PhyMappingPre)
    default_encoder.install_encoder('phy', 'physics symbols',
                                  mapping=PhyMapping)

# -----------------------------------------------------------------------------
# The Constants of Physics
# -----------------------------------------------------------------------------

# speed of light in vacuum
#   m/s   (meters per second)
c = Constant(299792458.0,
        default_encoder('$phy(c)'),
        desc='speed of light in vacuum',
        units='m/s')

# gravitational constant
#   m^3/(kg*s^2) (meters cubed per kilogram seconds squared)
#   N*m^2/s^2    (newton meters squared per seconds squared)
G = Constant(6.67408e-11,
        default_encoder('$phy(G)'),
        desc='gravitational constant',
        units='m^3/(kg*s^2)')

# Boltzmann constant
# The constant k_B relates average kinetic engergy of particles to
# temperature.
#   J/K (joules per kelvin) 
k_B = Constant(1.38064852e-23,
        default_encoder('$phy(k_B)'),
        desc='Boltzmann constant',
        units='J/K')

# epsilon naught
# The absolute dielectric permittivity of classical vacuum.
#   F/m (farads per meter) 
e_0 = Constant(8.854187817e-12,
        default_encoder('$phy(e_0)'),
        desc='absolute dielectric permittivity of classical vacuum',
        units='F/m')

# Planck constant
# The quantum of electromagnetic action.
#   J-s  (joule seconds)
h = Constant(6.62607015e-34,
        default_encoder('$phy(h)'),
        desc='Planck constant - quantum of electromagnetic action',
        units='J-s')

# reduced Planck constant
#   J-s (joule seconds)
h_bar = Constant(h / math.tau,
        default_encoder('$phy(h-bar)'),
        desc='reduced Planck constant',
        units='J-s/rad')

# Planck length
# Unit of length light travels in one unit of Planck time.
#   m (meters)
l_P = Constant(math.sqrt(h_bar * G / math.pow(c, 3)),
        default_encoder('$phy(l_P)'),
        desc='Planck length - '\
              'unit of lenght light travels in one unit of Planck time',
        units='m')


# Planck time
# Unit of time light travels in one unit of Planck length.
#   s (seconds)
t_P = Constant(l_P / c,
        default_encoder('$phy(t_P)'),
        desc='Planck length - '\
              'unit of time light travels in one unit of Planck length',
        units='s')

# Planck mass
#   kg (kilograms)
m_P = Constant(math.sqrt((h_bar * c) / G),
        default_encoder('$phy(m_P)'),
        desc='Planck mass',
        units='kg')

# Planck charge
#   C (coulombs)
q_P = Constant(math.sqrt(4 * math.pi * e_0 * h_bar * c),
        default_encoder('$phy(q_P)'),
        desc='Planck charge',
        units='C') 

# Planck temperature
#   K (kelvins)
T_P = Constant((m_P * math.pow(c, 2))/k_B,
        default_encoder('$phy(T_P)'),
        desc='Planck temperature',
        units='K')

# fine-structure constant
# Characterizes the strength of the electromagnetic interaction between
# particles. And the true Rick C-137
#   dimensionless
alpha = Constant(1/137,
          default_encoder('$phy(alpha)'), 
          desc='characterizes the strength of the electromagnetic '\
                'interaction between particles (and the true Rick C-137)',
          units='dimensionless')

# The list of all constants in this module.
constants = [c, G, k_B, e_0, h, h_bar, l_P, t_P, m_P, q_P, T_P, alpha]

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utconstants as ut

  sys.exit(ut.utmain())

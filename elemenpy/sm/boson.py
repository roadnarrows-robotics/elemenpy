"""
Bosons.

Package:
  RoadNarrows elemenpy package.

File:
  boson.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""
from copy import copy
from enum import Enum

from elemenpy.core.common import (isderivedclass)
from elemenpy.core.format import (Format, default_encoder)
from elemenpy.core.prettyprint import (print2cols)

from elemenpy.sm.standardmodel import (StandardModel as sm, SubatomicParticle)
from elemenpy.sm.spin import (SpinQuantumNumber)
from elemenpy.sm.electriccharge import (ElectricCharge)
from elemenpy.sm.colorcharge import (ColorCharge)

# -----------------------------------------------------------------------------
# Boson Base Class
# -----------------------------------------------------------------------------
class Boson(SubatomicParticle):
  """ Boson base class. """
  class BosonSubfamily(Enum):
    """ Boson subfamily enumeration. """
    UNKNOWN = 0
    SCALAR  = 1 # scalar
    VECTOR  = 2 # vector

  Classification  = sm.Classification.BOSON
  Family          = sm.Family.BOSON
  Statistics      = sm.Statistics.BOSONIC
  Name            = 'boson'
  Symbol          = 'boson'

  Subfamily       = BosonSubfamily.UNKNOWN

  # registered boson subclasses by the @Boson.subclass decorator
  Subclasses = {} 

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def subclass(klass):
    """
    Boson subclass decorator to add a subclass to an internal list.
    """
    def wrap(D):
      """
      Store derived subclass.

      Parameters:
        D   Prospective derived class.
      """
      if isderivedclass(D, klass):
        klass.Subclasses[D.__name__] = D
      return D
    return wrap

  @classmethod
  def finalize_boson_family(klass):
    """
    Finalize all registered boson subclass attributes.

    Bosons are interdependent.
    """
    for qname, qklass in klass.Subclasses.items():
      qklass.finalize_boson()

  @classmethod
  def boson_family(klass):
    """
    Get the dictionary of all registered boson subclasses.

    Returns:
      {qname: qclass, ...}
    """
    return klass.Subclasses

  @classmethod
  def boson_class(klass, qname):
    """
    Get the boson subclass.

    Parameters:
      qname    Boson subclass name.

    Returns:
      qclass
    """
    return klass.Subclasses[qname]

  @classmethod
  def subfamily(klass):
    """ Return boson subfamily. """
    return klass.Subfamily

  @classmethod
  def print_boson_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed meson particle properties to output stream.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_subatomic_properties(indent=indent, **print_kwargs)

    #print(f"{'':<{indent+2}}Boson", **print_kwargs)
    print2cols([
      ('Subfamily', klass.Subfamily.name),],
          c1width=16, indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Boson initializer. """
    SubatomicParticle.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.name

  @property
  def subfamily(self):
    """ Return boson subfamily. """
    return self.Subfamily

  def print_state(self, indent=0, **print_kwargs):
    """
    Print boson state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    SubatomicParticle.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Photon Class
# -----------------------------------------------------------------------------
@Boson.subclass()
class Photon(Boson):
  """ Photon class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.PHOTON
  Name        = "photon"
  Symbol      = default_encoder('$sm(gamma)')
  RestMass    = 0.0
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1)    # intrinsic spin number

  Subfamily   = Boson.BosonSubfamily.VECTOR

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_boson(klass):
    """
    Finalize boson's class attibutes.

    Finalization can only proceed when all boson classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.boson_class('Photon')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_boson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Photon initializer. """
    Boson.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print photon state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Boson.print_state(self, indent=indent, **print_kwargs)


# -----------------------------------------------------------------------------
# WBosonN Class
# -----------------------------------------------------------------------------
@Boson.subclass()
class WBosonN(Boson):
  """ WBosonN class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.W_BOSON_N
  Name        = "W-boson-"
  Symbol      = default_encoder('$sm(W-)')
  RestMass    = 80.385e3
  ElecCharge  = ElectricCharge(-1)
  QSpin       = SpinQuantumNumber(1)    # intrinsic spin number

  Subfamily   = Boson.BosonSubfamily.VECTOR

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_boson(klass):
    """
    Finalize boson's class attibutes.

    Finalization can only proceed when all boson classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.boson_class('WBosonP')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_boson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ W- boson initializer. """
    Boson.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print W- boson state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Boson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# WBosonP Class
# -----------------------------------------------------------------------------
@Boson.subclass()
class WBosonP(Boson):
  """ WBosonP class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.W_BOSON_P
  Name        = "W-boson+"
  Symbol      = default_encoder('$sm(W+)')
  RestMass    = 80.385e3
  ElecCharge  = ElectricCharge(1)
  QSpin       = SpinQuantumNumber(1)    # intrinsic spin number

  Subfamily   = Boson.BosonSubfamily.VECTOR

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_boson(klass):
    """
    Finalize boson's class attibutes.

    Finalization can only proceed when all boson classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.boson_class('WBosonN')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_boson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ W+ boson initializer. """
    Boson.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print W+ boson state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Boson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# ZBoson Class
# -----------------------------------------------------------------------------
@Boson.subclass()
class ZBoson(Boson):
  """ ZBoson class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.Z_BOSON
  Name        = "Z-boson"
  Symbol      = default_encoder('$sm(Z)')
  RestMass    = 91.1875e3
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1)    # intrinsic spin number

  Subfamily   = Boson.BosonSubfamily.VECTOR

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_boson(klass):
    """
    Finalize boson's class attibutes.

    Finalization can only proceed when all boson classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.boson_class('ZBoson')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_boson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Z boson initializer. """
    Boson.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print Z boson state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Boson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Gluon Class
# -----------------------------------------------------------------------------
@Boson.subclass()
class Gluon(Boson):
  """ Gluon class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.GLUON
  Name        = "gluon"
  Symbol      = default_encoder('$sm(g)')
  RestMass    = 0.0
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1)    # intrinsic spin number

  Subfamily   = Boson.BosonSubfamily.VECTOR

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_boson(klass):
    """
    Finalize boson's class attibutes.

    Finalization can only proceed when all boson classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.boson_class('Gluon')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_boson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color, anticolor):
    """
    Gluon initializer.

    Parameters:
      color       Primary color charge.
      anticolor   Anticolor charge.
    """
    Boson.__init__(self)

    self._color_charge     = ColorCharge(color)
    self._anticolor_charge = ColorCharge(anticolor)

    if not self.color_charge.is_primary_color():
      raise ValueError(
          f"{self.name} '{self.color_charge.name}' is not a primary color")

    if not self.anticolor_charge.is_anticolor():
      raise ValueError(
          f"{self.name} '{self.anticolor_charge.name}' is not an anticolor")

    if self.color_charge == self.anticolor_charge.complement:
      raise ValueError(f"{self.name} " +
        f"'{self.color_charge.name}-{self.anticolor_charge.name}' " +
        "defines a meson")

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"{self.color_charge!r}, {self.anticolor_charge!r})"

  def __str__(self):
    return self.fqname

  def __eq__(self, gluon):
    """
    Equal to. self == gluon.

    Two gluons are considered equal if they are of the same kind.
    That is, gluons with the same color charges.
    """
    return  self.color_charge == gluon.color_charge and \
            self.anticolor_charge == gluon.anticolor_charge

  def __ne__(self, gluon):
    """
    Not equal to. self != gluon.

    Two gluons are considered not equal if they are not of the same kind.
    That is, gluons that do not have the same color charges.
    """
    return  self.color_charge != gluon.color_charge or \
            self.anticolor_charge != gluon.anticolor_charge

  @property
  def fqname(self):
    return f"{self.color_charge.name}-{self.anticolor_charge.name} {self.name}"

  @property
  def color_charge(self):
    """ Return primary color charge. """
    return self._color_charge

  @property
  def anticolor_charge(self):
    """ Return anticolor charge. """
    return self._anticolor_charge

  def print_state(self, indent=0, **print_kwargs):
    """
    Print gluon state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Boson.print_state(self, indent=indent, **print_kwargs)

    print2cols([
      ('FQ Name', self.fqname),
      ('Color Charge', 
            f"{self.color_charge.symbol} {self.color_charge.name}"),
      ('Anticolor Charge', 
            f"{self.anticolor_charge.symbol} {self.anticolor_charge.name}"),],
          indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# HiggsBoson Class
# -----------------------------------------------------------------------------
@Boson.subclass()
class HiggsBoson(Boson):
  """ HiggsBoson class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.HIGGS_BOSON
  Name        = "higgs-boson"
  Symbol      = default_encoder('$sm(H0)')
  RestMass    = 125.09e3
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(0)

  Subfamily   = Boson.BosonSubfamily.SCALAR

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_boson(klass):
    """
    Finalize boson's class attibutes.

    Finalization can only proceed when all boson classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.boson_class('HiggsBoson')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_boson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Higgs boson initializer. """
    Boson.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print Higgs boson state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Boson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# On module load execution
# -----------------------------------------------------------------------------
Boson.finalize_boson_family()

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utboson as ut

  sys.exit(ut.utmain())

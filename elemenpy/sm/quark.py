"""
Quarks - quirks of nature.

Package:
  RoadNarrows elemenpy package.

File:
  quark.py

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

from elemenpy.core.common import (isderivedclass)
from elemenpy.core.format import (Format, default_encoder)
from elemenpy.core.prettyprint import (print2cols)

from elemenpy.sm.standardmodel import (StandardModel as sm, SubatomicParticle)
from elemenpy.sm.spin import (SpinQuantumNumber)
from elemenpy.sm.electriccharge import (ElectricCharge)
from elemenpy.sm.colorcharge import (ColorCharge)

from elemenpy.sm.boson import (Gluon)

# -----------------------------------------------------------------------------
# Quark Base Class
# -----------------------------------------------------------------------------
class Quark(SubatomicParticle):
  """ Quark base class. """
  Classification  = sm.Classification.FERMION
  Family          = sm.Family.QUARK
  Statistics      = sm.Statistics.FERMIONIC
  Name            = 'quark'
  Symbol          = 'q'

  Generation      = 0   # quark generation I, II, III
  Strangeness     = 0
  Charm           = 0
  Topness         = 0
  Beauty          = 0

  # registered quark subclasses by the @Quark.subclass decorator
  Subclasses = {} 

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def subclass(klass):
    """
    Quark subclass decorator to add a subclass to an internal list.
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
  def finalize_quark_family(klass):
    """
    Finalize all registered quark subclass attributes.

    Quarks are interdependent.
    """
    for qname, qklass in klass.Subclasses.items():
      qklass.finalize_quark()

  @classmethod
  def quark_family(klass):
    """
    Get the dictionary of all registered quark subclasses.

    Returns:
      {qname: qclass, ...}
    """
    return klass.Subclasses

  @classmethod
  def quark_class(klass, qname):
    """
    Get the quark subclass.

    Parameters:
      qname    Quark subclass name.

    Returns:
      qclass
    """
    return klass.Subclasses[qname]

  @classmethod
  def count_electric_charge(klass, quarks):
    """
    Count electric charge from quark list.

    Parameters:
      quarks  Iterable holding quark class objects.

    Returns:
      Electric charge.
    """
    charge = ElectricCharge(0)
    for q in quarks:
      charge += q.ElecCharge
    charge.canonical()
    return charge

  @classmethod
  def count_strangeness(klass, quarks):
    """
    Count meson's strangeness from quark list.

    strangeness := -(n_strange - n_antistrang)

    Parameters:
      quarks  Iterable holding quark class objects.

    Returns:
      Strangeness.
    """
    cnt = 0
    for q in quarks:
      cnt += q.Strangeness
    return cnt

  @classmethod
  def count_charm(klass, quarks):
    """
    Count meson's charm from quark list.

    charm := n_charm - n_anticharm

    Parameters:
      quarks  Iterable holding quark class objects.

    Returns:
      Charm.
    """
    cnt = 0
    for q in quarks:
      cnt += q.Charm
    return cnt

  @classmethod
  def count_beauty(klass, quarks):
    """
    Count meson's beauty (bottomness) from quark list.

    beauty := -(n_bottom - n_antibottom)
    Parameters:
      quarks  Iterable holding quark class objects.

    Returns:
      Beauty.
    """
    cnt = 0
    for q in quarks:
      cnt += q.Beauty
    return cnt

  @classmethod
  def print_quark_properties(klass, indent=0, **print_kwargs):
    """
    Print intrinsic quark particle properties to output stream using
    default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_subatomic_properties(indent=indent, **print_kwargs)

    print2cols([
      ('Generation',  klass.Generation),
      ('Charm',       klass.Charm),
      ('Strangeness', klass.Strangeness),
      ('Topness',     klass.Topness),
      ('Beauty',      klass.Beauty),],
          c1width=16, indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color=ColorCharge.QCDColor.UNKNOWN):
    """
    Quark initializer.

    Parameters:
      color   QCD color charge.
    """
    SubatomicParticle.__init__(self)
    self._color_charge = ColorCharge(color)

    if self.is_antimatter():
      chk = self.color_charge.is_anticolor()
    else:
      chk = self.color_charge.is_primary_color()

    if not chk:
      raise ValueError(f"Quark '{self.name}' cannot be assigned " + \
                       f"color charge '{self._color_charge.name}'")

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.fqname

  def __eq__(self, quark):
    """
    Equal to. self == quark.

    Two quarks are considered equal if they are of the same flavor
    and color.
    """
    return  self.pid == quark.pid and self.color == quark.color

  def __ne__(self, quark):
    """
    Not equal to. self != quark.

    Two quarks are considered not equal if they are not of the same
    flavor or color.
    """
    return  self.pid != quark.pid or self.color != quark.color

  @property
  def fqname(self):
    return f"{self.color_charge.name} {self.name}"

  @property
  def generation(self):
    """ Return quark generation 1, 2, or 3. """
    return self.Generation

  @property
  def strangeness(self):
    """ Return quark's strangeness. """
    return self.Strangeness

  @property
  def charm(self):
    """ Return quark's charm. """
    return self.Charm

  @property
  def topness(self):
    """ Return quark's topness. """
    return self.Topness

  @property
  def beauty(self):
    """ Return quark's beauty (bottomness). """
    return self.Beauty

  @property
  def color_charge(self):
    """ Return color charge. """
    return self._color_charge

  @color_charge.setter
  def color_charge(self, color):
    """
    Set color charge.

    Parameters:
      color   Valid string, enum, or numeric value that can be mapped
              to a color charge enumeration.
    """
    self._color_charge.color = color

  def emit_gluon(self, color_bar):
    """
    Emit a gluon. Gluons carry one color charge and one anticolor charge.
    The current color of this quark provides one of the gluon's colors,
    while the provided color_bar must be a complement color. That is,
    for quarks color_bar is an anticolor while for antiquarks it is a
    color.

    Side Effect:
      By emitting the gluon, this quark changes color.

    Parameters:
      color_bar   Valid string, enum, or numeric value that can be mapped
                  to a QCD color enumeration.
                  The color_bar must specify an anticolor/primary color
                  depending on whether this quark is primary/anticolor,
                  respectively.

    Returns:
      Gluon of appropriate color.
  """
  #if self.is_primary_color():
  #  return Gluon(self.color, ColorCharge.QCDColor.from_value(color_bar))
  #else:
  #  return Gluon(ColorCharge.QCDColor.from_value(color_bar), self.color)
  pass

  def absorb_gluon(self, gluon):
    """
    Absorb a gluon. Gluons carry one color charge and one anticolor charge.
    The gluon must carry the complement of this quark current color.

    Side Effect:
      By asorbing the gluon, this quark changes color.

    Parameters:
      gluon       Boson gluon particle.
  """
    #if self.complement(gluon.anticolor) != self.color:
    #  raise ValueError()
    #self.color = gluon.color
    pass

  def print_state(self, indent=0, **print_kwargs):
    """
    Print quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    SubatomicParticle.print_state(self, indent=indent, **print_kwargs)

    print2cols([
      ('FQ Name', self.fqname),
      ('Color Charge', 
                  f"{self._color_charge.symbol} {self._color_charge.name}"),],
          indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Up Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class Up(Quark):
  """ Up quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.UP_QUARK
  Name        = "up"
  Symbol      = default_encoder('$sm(u)')
  RestMass    = 2.3                     # MeV/c^2
  ElecCharge  = ElectricCharge(2, 3)    #
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.

    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('AntiUp')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Up quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print up quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AnitUp Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class AntiUp(Quark):
  """ AntiUp quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.UP_ANTIQUARK
  Name        = "antiup"
  Symbol      = default_encoder('$sm(u-bar)')
  RestMass    = 2.3                     # MeV/c^2
  ElecCharge  = ElectricCharge(-2, 3)   # 
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.
    
    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('Up')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Antiup quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print anitup quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Down Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class Down(Quark):
  """ Down quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.DOWN_QUARK
  Name        = "down"
  Symbol      = default_encoder('$sm(d)')
  RestMass    = 4.6                     # MeV/c^2
  ElecCharge  = ElectricCharge(-1, 3)
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.

    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('AntiDown')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Down quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print down quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AnitDown Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class AntiDown(Quark):
  """ AntiDown quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.DOWN_ANTIQUARK
  Name        = "antidown"
  Symbol      = default_encoder('$sm(d-bar)')
  RestMass    = 4.6                     # MeV/c^2
  ElecCharge  = ElectricCharge(1, 3) 
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.
    
    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('Down')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Antidown quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print antidown quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Charm Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class Charm(Quark):
  """ Charm quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.CHARM_QUARK
  Name        = "charm"
  Symbol      = default_encoder('$sm(c)')
  RestMass    = 1280.0                  # MeV/c^2
  ElecCharge  = ElectricCharge(2, 3)    #
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 2
  Charm       = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.

    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('AntiCharm')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Charm quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print charm quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AnitCharm Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class AntiCharm(Quark):
  """ AntiCharm quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.CHARM_ANTIQUARK
  Name        = "anticharm"
  Symbol      = default_encoder('$sm(c-bar)')
  RestMass    = 1280.0                  # MeV/c^2
  ElecCharge  = ElectricCharge(-2, 3)   # 
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 2
  Charm       = -1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.
    
    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('Charm')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Anticharm quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print anticharm quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Strange Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class Strange(Quark):
  """ Strange quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.STRANGE_QUARK
  Name        = "strange"
  Symbol      = default_encoder('$sm(s)')
  RestMass    = 96.0                    # MeV/c^2
  ElecCharge  = ElectricCharge(-1, 3)   #
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 2
  Strangeness = -1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.

    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('AntiStrange')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Strange quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print strange quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AnitStrange Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class AntiStrange(Quark):
  """ AntiStrange quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.STRANGE_ANTIQUARK
  Name        = "antistrange"
  Symbol      = default_encoder('$sm(s-bar)')
  RestMass    = 96.0                    # MeV/c^2
  ElecCharge  = ElectricCharge(1, 3)    # 
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 2
  Strangeness = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.
    
    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('Strange')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Antistrange quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print antistrange quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Top Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class Top(Quark):
  """ Top quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.TOP_QUARK
  Name        = "top"
  Symbol      = default_encoder('$sm(t)')
  RestMass    = 173100.0
  ElecCharge  = ElectricCharge(2, 3)    #
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 3
  Topness     = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.

    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('AntiTop')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Top quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print top quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AnitTop Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class AntiTop(Quark):
  """ AntiTop quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.TOP_ANTIQUARK
  Name        = "antitop"
  Symbol      = default_encoder('$sm(t-bar)')
  RestMass    = 173100.0
  ElecCharge  = ElectricCharge(-2, 3)   # 
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 3
  Topness     = -1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.
    
    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('Top')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Antitop quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print antitop quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Bottom Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class Bottom(Quark):
  """ Bottom quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.BOTTOM_QUARK
  Name        = "bottom"
  Symbol      = default_encoder('$sm(b)')
  RestMass    = 4180.0                  # MeV/c^2
  ElecCharge  = ElectricCharge(-1, 3)   #
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 3
  Beauty      = -1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.

    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('AntiBottom')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Bottom quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print bottom quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AnitBottom Class
# -----------------------------------------------------------------------------
@Quark.subclass()
class AntiBottom(Quark):
  """ AntiBottom quark class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.BOTTOM_ANTIQUARK
  Name        = "antibottom"
  Symbol      = default_encoder('$sm(b-bar)')
  RestMass    = 4180.0                  # MeV/c^2
  ElecCharge  = ElectricCharge(1, 3)
  QSpin       = SpinQuantumNumber(1, 2) # intrinsic spin number

  Generation  = 3
  Beauty      = 1

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_quark(klass):
    """
    Finalize quark's class attibutes.
    
    Finalization can only proceed when all quark classes have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.quark_class('Bottom')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_quark_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Antibottom quark initializer.

    Parameters:
      color   QCD color charge.
    """
    Quark.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.Name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print antibottom quark state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Quark.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# On module load execution
# -----------------------------------------------------------------------------
Quark.finalize_quark_family()

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utquark as ut

  sys.exit(ut.utmain())

"""
Baryons - a menagerie a trois.

Package:
  RoadNarrows elemenpy package.

File:
  baryon.py

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
import random

from elemenpy.core.common import (isderivedclass)
from elemenpy.core.format import (Format, default_encoder)
from elemenpy.core.prettyprint import (print2cols)

from elemenpy.sm.standardmodel import (StandardModel as sm,
                                      NullParticle,
                                      SubatomicParticle)
from elemenpy.sm.spin import (SpinQuantumNumber)
from elemenpy.sm.electriccharge import (ElectricCharge)
from elemenpy.sm.colorcharge import (ColorCharge)
import elemenpy.sm.quark as quark
import elemenpy.sm.lepton as lepton

# -----------------------------------------------------------------------------
# Baryon Base Class
# -----------------------------------------------------------------------------
class Baryon(SubatomicParticle):
  """ Baryon base class. """
  Classification  = sm.Classification.HADRON | sm.Classification.FERMION
  Family          = sm.Family.BARYON
  Statistics      = sm.Statistics.FERMIONIC
  Name            = "baryon"
  Symbol          = 'baryon'

  # fixed quark triple template
  QuarkTriple     = (quark.Quark, quark.Quark, quark.Quark)

  # registered baryon subclasses by the @Baryon.subclass decorator
  Subclasses = {} 

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def subclass(klass):
    """
    Baryon subclass decorator to add a subclass to an internal list.

    Note: TBD investigate multiple loadings.
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
  def finalize_baryon_family(klass):
    """
    Finalize all registered baryon subclass attributes.

    Baryons are interdependent.
    """
    for bname, bklass in klass.Subclasses.items():
      bklass.finalize_baryon()

  @classmethod
  def baryon_family(klass):
    """
    Get the dictionary of all registered baryon subclasses.

    Returns:
      {bname: qclass, ...}
    """
    return klass.Subclasses

  @classmethod
  def baryon_class(klass, bname):
    """
    Get the baryon subclass.

    Parameters:
      bname    Baryon subclass name.

    Returns:
      qclass
    """
    return klass.Subclasses[bname]

  @classmethod
  def quark_notation(klass, quarks):
    """
    Generate a baryon's quark composition notation with default encoder.

    Parameters:
      quarks    Quark triple.

    Return:
      String.
    """
    triple = ''
    for q in quarks:
      triple += q.Symbol
    return triple

  @classmethod
  def print_baryon_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed intrinsic meson subatomic particle properties to
    output stream.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_subatomic_properties(indent=indent, **print_kwargs)

    print2cols([
      ('Quark Triple', klass.quark_notation(klass.QuarkTriple)),],
          c1width=16, indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, randcolor=False):
    """
    Baryon initializer.

    Parameters:
      randcolor   Each quark in the quark triplet will be assigned
                  a random color with the restriction that the
                  three colors create white.
    """
    SubatomicParticle.__init__(self)

    if self.is_matter():
      colors = ColorCharge.PrimaryColors
    else:
      colors = ColorCharge.AntiColors

    if randcolor:
      random.shuffle(colors)

    self._quarks = []
    for i in range(len(self.QuarkTriple)):
      self._quarks.append(self.QuarkTriple[i](colors[i%len(colors)]))

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(randcolor={randcolor})"

  def __str__(self):
    return self.name

  @property
  def quarks(self):
    """ Return baryon's quark triple. """
    return self._quarks

  def print_state(self, indent=0, **print_kwargs):
    """
    Print baryon state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    SubatomicParticle.print_state(self, indent=indent, **print_kwargs)

    print2cols([
        ('Quark Triple', ', '.join(f"{q.fqname}" for q in self.quarks)), ],
          indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Proton Class
# -----------------------------------------------------------------------------
@Baryon.subclass()
class Proton(Baryon):
  """ Proton class. """

  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.PROTON
  Name        = "proton"
  Symbol      = default_encoder('$sm(p)')
  AltSymbol   = default_encoder('$sm(p+)')
  QuarkTriple = (quark.Up, quark.Up, quark.Down)
  RestMass    = 938.2720813
  ElecCharge  = ElectricCharge(1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_baryon(klass):
    """
    Finalize baryon's class attibutes.

    Finalization can only proceed when all baryon subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.baryon_class('AntiProton')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed intrinsic proton subatomic particle properties to
    output stream.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_baryon_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, randcolor=False):
    """
    Proton initializer.

    Parameters:
      randcolor   Each quark in the quark triplet will be assigned
                  a random color with the restriction that the
                  three colors create white.
    """
    Baryon.__init__(self, randcolor=randcolor)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(randcolor={randcolor})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print proton state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Baryon.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AntiProton Class
# -----------------------------------------------------------------------------
@Baryon.subclass()
class AntiProton(Baryon):
  """ AntiProton class. """

  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.ANTIPROTON
  Name        = "antiproton"
  Symbol      = default_encoder('$sm(p-bar)')
  QuarkTriple = (quark.AntiUp, quark.AntiUp, quark.AntiDown)
  RestMass    = 938.2720813
  ElecCharge  = ElectricCharge(-1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_baryon(klass):
    """
    Finalize baryon's class attibutes.

    Finalization can only proceed when all baryon subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.baryon_class('Proton')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed intrinsic antiproton subatomic particle properties to
    output stream.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_baryon_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, randcolor=False):
    """
    AntiProton initializer.

    Parameters:
      randcolor   Each quark in the quark triplet will be assigned
                  a random color with the restriction that the
                  three colors create white.
    """
    Baryon.__init__(self, randcolor=randcolor)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(randcolor={randcolor})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print antiproton state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Baryon.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Neutron Class
# -----------------------------------------------------------------------------
@Baryon.subclass()
class Neutron(Baryon):
  """ Neutron class. """

  #
  # Class Fixed Properties
  #
  Pid           = sm.ParticleId.NEUTRON
  Name          = "neutron"
  Symbol        = default_encoder('$sm(n)')
  AltSymbol     = default_encoder('$sm(n0)')
  QuarkTriple   = (quark.Up, quark.Down, quark.Down)
  RestMass      = 939.5654133
  ElecCharge    = ElectricCharge(0)
  QSpin         = SpinQuantumNumber(1, 2)
  MeanLifetime  = 881.5   # free neutron
  DecayProducts = [ (Proton, lepton.Electron, lepton.ElectronNeutrino) ]

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_baryon(klass):
    """
    Finalize baryon's class attibutes.

    Finalization can only proceed when all baryon subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.baryon_class('AntiNeutron')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed intrinsic neutron subatomic particle properties to
    output stream.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_baryon_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, randcolor=False):
    """
    Neutron initializer.

    Parameters:
      randcolor   Each quark in the quark triplet will be assigned
                  a random color with the restriction that the
                  three colors create white.
    """
    Baryon.__init__(self, randcolor=randcolor)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(randcolor={randcolor})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print neutron state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Baryon.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# AntiNeutron Class
# -----------------------------------------------------------------------------
@Baryon.subclass()
class AntiNeutron(Baryon):
  """ AntiNeutron class. """

  #
  # Class Fixed Properties
  #
  Pid           = sm.ParticleId.ANTINEUTRON
  Name          = "antineutron"
  Symbol        = default_encoder('$sm(n-bar)')
  QuarkTriple   = (quark.AntiUp, quark.AntiDown, quark.AntiDown)
  RestMass      = 939.565560
  ElecCharge    = ElectricCharge(0)
  QSpin         = SpinQuantumNumber(1, 2)
  MeanLifetime  = 881.5   # free antineutron
  DecayProducts = [ (AntiProton, lepton.Positron, lepton.ElectronNeutrino) ]

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_baryon(klass):
    """
    Finalize baryon's class attibutes.

    Finalization can only proceed when all baryon subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.baryon_class('Neutron')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed intrinsic antineutron subatomic particle properties to
    output stream.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_baryon_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, randcolor=False):
    """
    AntiNeutron initializer.

    Parameters:
      randcolor   Each quark in the quark triplet will be assigned
                  a random color with the restriction that the
                  three colors create white.
    """
    Baryon.__init__(self, randcolor=randcolor)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(randcolor={randcolor})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print antineutron state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Baryon.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# On module load execution
# -----------------------------------------------------------------------------
Baryon.finalize_baryon_family()

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utbaryon as ut

  sys.exit(ut.utmain())

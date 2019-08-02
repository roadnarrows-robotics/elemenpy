"""
Mesons - they march two by two.

Package:
  RoadNarrows elemenpy package.

File:
  meson.py

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
import elemenpy.sm.quark as quark
import elemenpy.sm.lepton as lepton
import elemenpy.sm.boson as boson

# -----------------------------------------------------------------------------
# Meson Base Class
# -----------------------------------------------------------------------------
class Meson(SubatomicParticle):
  """ Meson base class. """
  Classification  = sm.Classification.HADRON | sm.Classification.BOSON
  Family          = sm.Family.MESON
  Statistics      = sm.Statistics.BOSONIC
  Name            = 'meson'
  Symbol          = 'meson'

  QuarkPair       = (quark.Quark, quark.Quark)
  Strangeness     = 0
  Charm           = 0
  Beauty          = 0

  # registered meson subclasses by the @Meson.subclass decorator
  Subclasses = {} 

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def subclass(klass):
    """
    Meson subclass decorator to add a subclass to an internal list.

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
  def finalize_meson_family(klass):
    """
    Finalize all registered meson subclass attributes.

    Mesons are interdependent.
    """
    for bname, bklass in klass.Subclasses.items():
      bklass.finalize_meson()

  @classmethod
  def meson_family(klass):
    """
    Get the dictionary of all registered meson subclasses.

    Returns:
      {bname: qclass, ...}
    """
    return klass.Subclasses

  @classmethod
  def meson_class(klass, bname):
    """
    Get the meson subclass.

    Parameters:
      bname    Meson subclass name.

    Returns:
      Meson class.
    """
    return klass.Subclasses[bname]

  @classmethod
  def quark_notation(klass, quarks):
    """
    Generate a meson's quark composition notation with default encoder.

    Parameters:
      quarks    Quark pair.

    Return:
      String.
    """
    pair = ''
    for q in quarks:
      pair += q.Symbol
    return pair

  @classmethod
  def print_meson_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed meson particle properties to output stream.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    klass.print_subatomic_properties(indent=indent, **print_kwargs)

    print2cols([
      ('Quark Pair',  klass.quark_notation(klass.QuarkPair)),
      ('Strangeness', klass.Strangeness),
      ('Charm',       klass.Charm),
      ('Beauty',      klass.Beauty),],
          c1width=16, indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Meson initializer.

    Mesons hold complementary color charges.

    Parameters:
      color   Primary color charge.
    """
    SubatomicParticle.__init__(self)

    color_charge     = ColorCharge(color)
    anticolor_charge = color_charge.complement

    self._quarks = [self.QuarkPair[0](color_charge),
                    self.QuarkPair[1](anticolor_charge)]

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.name

  @property
  def quarks(self):
    """ Return meson's quark pair. """
    return self._quarks

  @property
  def strangeness(self):
    """ Return meson's strangeness. """
    return self.Strangeness

  @property
  def charm(self):
    """ Return meson's charm. """
    return self.Charm

  @property
  def beauty(self):
    """ Return meson's beauty (bottomness). """
    return self.Beauty

  def print_state(self, indent=0, **print_kwargs):
    """
    Print meson state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    SubatomicParticle.print_state(self, indent=indent, **print_kwargs)

    print2cols([
        ('Quark Pair', ', '.join(f"{q.fqname}" for q in self.quarks)), ],
          indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# PionP Class
# -----------------------------------------------------------------------------
@Meson.subclass()
class PionP(Meson):
  """ PionP class. """
  #
  # Class Fixed Properties
  #
  Pid           = sm.ParticleId.PION_P
  Name          = "pion+"
  Symbol        = default_encoder('$sm(pi+)')
  RestMass      = 139.57018               # MeV/c^2
  Spin          = SpinQuantumNumber(0)    # intrinsic spin number
  MeanLifetime  = 2.6033e-8               # seconds
  DecayProducts = [(lepton.AntiMuon, lepton.MuonNeutrino)]

  QuarkPair     = (quark.Up, quark.AntiDown)
  ElecCharge    = quark.Quark.count_electric_charge(QuarkPair)
  Strangeness   = quark.Quark.count_strangeness(QuarkPair)
  Charm         = quark.Quark.count_charm(QuarkPair)
  Beauty        = quark.Quark.count_beauty(QuarkPair)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_meson(klass):
    """
    Finalize meson's class attibutes.

    Finalization can only proceed when all meson subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.meson_class('PionN')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_meson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    PionP initializer.

    Mesons hold complementary color charges.

    Parameters:
      color   Primary color charge.
    """
    Meson.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print pion+ state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Meson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# PionN Class
# -----------------------------------------------------------------------------
@Meson.subclass()
class PionN(Meson):
  """ PionN class. """
  #
  # Class Fixed Properties
  #
  Pid           = sm.ParticleId.PION_N
  Name          = "pion-"
  Symbol        = default_encoder('$sm(pi-)')
  RestMass      = 139.57018               # MeV/c^2
  Spin          = SpinQuantumNumber(0)    # intrinsic spin number
  MeanLifetime  = 2.6033e-8               # seconds
  DecayProducts = [(lepton.Muon, lepton.MuonAntiNeutrino)]

  QuarkPair     = (quark.Down, quark.AntiUp)
  ElecCharge    = quark.Quark.count_electric_charge(QuarkPair)
  Strangeness   = quark.Quark.count_strangeness(QuarkPair)
  Charm         = quark.Quark.count_charm(QuarkPair)
  Beauty        = quark.Quark.count_beauty(QuarkPair)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_meson(klass):
    """
    Finalize meson's class attibutes.

    Finalization can only proceed when all meson subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.meson_class('PionP')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_meson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    PionN initializer.

    Mesons hold complementary color charges.

    Parameters:
      color   Primary color charge.
    """
    Meson.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print pion- state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Meson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Pion0 Class
# -----------------------------------------------------------------------------
@Meson.subclass()
class Pion0(Meson):
  """ Pion0 class. """
  #
  # Class Fixed Properties
  #
  Pid           = sm.ParticleId.PION_0
  Name          = "pion0"
  Symbol        = default_encoder('$sm(pi0)')
  RestMass      = 134.9766
  Spin          = SpinQuantumNumber(0)
  MeanLifetime  = 8.4e-17
  DecayProducts   = [(boson.Photon, boson.Photon)]

  QuarkPair     = (quark.Up, quark.AntiUp)  # not really
  ElecCharge    = quark.Quark.count_electric_charge(QuarkPair)
  Strangeness   = quark.Quark.count_strangeness(QuarkPair)
  Charm         = quark.Quark.count_charm(QuarkPair)
  Beauty        = quark.Quark.count_beauty(QuarkPair)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_meson(klass):
    """
    Finalize meson's class attibutes.

    Finalization can only proceed when all meson subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.meson_class('Pion0')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_meson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    Pion0 initializer.

    Mesons hold complementary color charges.

    Parameters:
      color   Primary color charge.
    """
    Meson.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print pion0 state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Meson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# KaonP Class
# -----------------------------------------------------------------------------
@Meson.subclass()
class KaonP(Meson):
  """ KaonP class. """
  #
  # Class Fixed Properties
  #
  Pid           = sm.ParticleId.KAON_P
  Name          = "kaon+"
  Symbol        = default_encoder('$sm(K+)')
  RestMass      = 493.677
  Spin          = SpinQuantumNumber(0)
  MeanLifetime  = 1.238e-8
  DecayProducts = [ (lepton.AntiMuon, lepton.MuonNeutrino),
                    (PionP, Pion0),
                    (PionP, PionP, PionN),
                    (Pion0, lepton.Positron, lepton.ElectronNeutrino),
                  ]

  QuarkPair     = (quark.Up, quark.AntiStrange)
  ElecCharge    = quark.Quark.count_electric_charge(QuarkPair)
  Strangeness   = quark.Quark.count_strangeness(QuarkPair)
  Charm         = quark.Quark.count_charm(QuarkPair)
  Beauty        = quark.Quark.count_beauty(QuarkPair)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_meson(klass):
    """
    Finalize meson's class attibutes.

    Finalization can only proceed when all meson subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.meson_class('KaonN')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_meson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    KaonP initializer.

    Mesons hold complementary color charges.

    Parameters:
      color   Primary color charge.
    """
    Meson.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print kaon+ state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Meson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# KaonN Class
# -----------------------------------------------------------------------------
@Meson.subclass()
class KaonN(Meson):
  """ KaonN class. """
  #
  # Class Fixed Properties
  #
  Pid           = sm.ParticleId.KAON_N
  Name          = "kaon-"
  Symbol        = default_encoder('$sm(K-)')
  RestMass      = 493.677
  Spin          = SpinQuantumNumber(0)    # intrinsic spin number
  MeanLifetime  = 1.238e-8
  DecayProducts = [ (lepton.Muon, lepton.MuonAntiNeutrino),
                    (PionN, Pion0),
                    (PionN, PionN, PionP),
                    (Pion0, lepton.Electron, lepton.ElectronNeutrino),
                  ]

  QuarkPair     = (quark.Strange, quark.AntiUp)
  ElecCharge    = quark.Quark.count_electric_charge(QuarkPair)
  Strangeness   = quark.Quark.count_strangeness(QuarkPair)
  Charm         = quark.Quark.count_charm(QuarkPair)
  Beauty        = quark.Quark.count_beauty(QuarkPair)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_meson(klass):
    """
    Finalize meson's class attibutes.

    Finalization can only proceed when all meson subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.meson_class('KaonP')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_meson_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self, color):
    """
    KaonN initializer.

    Mesons hold complementary color charges.

    Parameters:
      color   Primary color charge.
    """
    Meson.__init__(self, color)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.color_charge!r})"

  def __str__(self):
    return self.name

  def print_state(self, indent=0, **print_kwargs):
    """
    Print pion- state to output stream using default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    Meson.print_state(self, indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# On module load execution
# -----------------------------------------------------------------------------
Meson.finalize_meson_family()

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utmeson as ut

  sys.exit(ut.utmain())

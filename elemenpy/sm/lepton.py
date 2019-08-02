"""
Leptons.

Package:
  RoadNarrows elemenpy package.

File:
  lepton.py

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

# -----------------------------------------------------------------------------
# Lepton Base Class
# -----------------------------------------------------------------------------
class Lepton(SubatomicParticle):
  """ Lepton base class. """
  Classification  = sm.Classification.FERMION
  Family          = sm.Family.LEPTON
  Statistics      = sm.Statistics.FERMIONIC
  Name            = 'lepton'
  Symbol          = 'lepton'

  # registered lepton subclasses by the @Lepton.subclass decorator
  Subclasses = {} 

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def subclass(klass):
    """
    Lepton.subclass decorator to add a subclass to an internal list.

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
  def finalize_lepton_family(klass):
    """
    Finalize all registered lepton subclass attributes.

    Leptons are interdependent.
    """
    for bname, bklass in klass.Subclasses.items():
      bklass.finalize_lepton()

  @classmethod
  def lepton_family(klass):
    """
    Get the dictionary of all registered lepton subclasses.

    Returns:
      {bname: qclass, ...}
    """
    return klass.Subclasses

  @classmethod
  def lepton_class(klass, bname):
    """
    Get the lepton subclass.

    Parameters:
      bname    Lepton subclass name.

    Returns:
      qclass
    """
    return klass.Subclasses[bname]

  @classmethod
  def print_lepton_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed meson particle properties to output stream.

    Parameters:
      print_kwargs  Print control keyword arguments.
    """
    klass.print_subatomic_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    SubatomicParticle.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# Electron Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class Electron(Lepton) :
  """ Electron class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.ELECTRON
  Name        = "electron"
  Symbol      = default_encoder('$sm(e-)')
  AltSymbol   = default_encoder('$sm(e)')
  RestMass    = 0.511
  ElecCharge  = ElectricCharge(-1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('Positron')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# Positron Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class Positron(Lepton) :
  """ Positron class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.POSITRON
  Name        = "positron"
  Symbol      = default_encoder('$sm(e+)')
  RestMass    = 0.511
  ElecCharge  = ElectricCharge(+1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('Electron')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# Muon Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class Muon(Lepton) :
  """ Muon class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.MUON
  Name        = "muon"
  Symbol      = default_encoder('$sm(mu-)')
  RestMass    = 105.7
  ElecCharge  = ElectricCharge(-1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('AntiMuon')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# AntiMuon Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class AntiMuon(Lepton) :
  """ AntiMuon class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.ANTIMUON
  Name        = "antimuon"
  Symbol      = default_encoder('$sm(mu+)')
  RestMass    = 105.7
  ElecCharge  = ElectricCharge(+1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('Muon')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# Tau Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class Tau(Lepton) :
  """ Tau class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.TAU
  Name        = "tau"
  Symbol      = default_encoder('$sm(tau-)')
  RestMass    = 1776.86
  ElecCharge  = ElectricCharge(-1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('AntiTau')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# AntiTau Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class AntiTau(Lepton) :
  """ AntiTau class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.ANTITAU
  Name        = "antitau"
  Symbol      = default_encoder('$sm(tau+)')
  RestMass    = 1776.86
  ElecCharge  = ElectricCharge(+1)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('Tau')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# ElectronNeutrino Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class ElectronNeutrino(Lepton) :
  """ ElectronNeutrino class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.ELECTRON_NEUTRINO
  Name        = "electron-neutrino"
  Symbol      =  default_encoder('$sm(nu_e)')
  RestMass    = 0.0000022   # upper limit; might be zero
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('ElectronAntiNeutrino')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# ElectronAntiNeutrino Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class ElectronAntiNeutrino(Lepton) :
  """ ElectronAntiNeutrino class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.ELECTRON_ANTINEUTRINO
  Name        = "electron-antineutrino"
  Symbol      = default_encoder('$sm(nu_e-bar)')
  RestMass    = 0.0000022   # upper limit; might be zero
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('ElectronNeutrino')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# MuonNeutrino Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class MuonNeutrino(Lepton) :
  """ MuonNeutrino class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.MUON_NEUTRINO
  Name        = "muon-neutrino"
  Symbol      = default_encoder('$sm(nu_mu)')
  RestMass    = 0.170   # upper limit; might be zero
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('MuonAntiNeutrino')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# MuonAntiNeutrino Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class MuonAntiNeutrino(Lepton) :
  """ MuonAntiNeutrino class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.MUON_ANTINEUTRINO
  Name        = "muon-antineutrino"
  Symbol      = default_encoder('$sm(nu_mu-bar)')
  RestMass    = 0.170   # upper limit; might be zero
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('MuonNeutrino')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# TauNeutrino Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class TauNeutrino(Lepton) :
  """ TauNeutrino class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.TAU_NEUTRINO
  Name        = "tau-neutrino"
  Symbol      = default_encoder('$sm(nu_tau)')
  RestMass    = 15.5   # upper limit; might be zero
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('TauAntiNeutrino')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# TauAntiNeutrino Class
# -----------------------------------------------------------------------------
@Lepton.subclass()
class TauAntiNeutrino(Lepton) :
  """ TauAntiNeutrino class. """
  #
  # Class Fixed Properties
  #
  Pid         = sm.ParticleId.TAU_ANTINEUTRINO
  Name        = "tau-antineutrino"
  Symbol      = default_encoder('$sm(nu_tau-bar)')
  RestMass    = 15.5   # upper limit; might be zero
  ElecCharge  = ElectricCharge(0)
  QSpin       = SpinQuantumNumber(1, 2)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def finalize_lepton(klass):
    """
    Finalize lepton's class attibutes.

    Finalization can only proceed when all lepton subclasses have been
    defined due to interdependencies. 
    """
    klass.AntiParticle = klass.lepton_class('TauNeutrino')

  @classmethod
  def print_properties(klass, indent=0, **print_kwargs):
    klass.print_lepton_properties(indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    Lepton.__init__(self)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"()"

  def __str__(self):
    return self.Name

# -----------------------------------------------------------------------------
# On module load execution
# -----------------------------------------------------------------------------
Lepton.finalize_lepton_family()

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utlepton as ut

  sys.exit(ut.utmain())

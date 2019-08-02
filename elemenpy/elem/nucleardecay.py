"""
Spontaneous nuclear decay.

Package:
  RoadNarrows elements package.

File:
  nucleardecay.py

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
from enum import Enum
import random

from elemenpy.core.common import (enumfactory, isderivedinstance, enum_to_str)
from elemenpy.core.format import (default_encoder, fInfNum)
from elemenpy.core.prettyprint import (print2cols)

from elemenpy.sm.lepton import (Electron, Positron,
                                ElectronNeutrino, ElectronAntiNeutrino)
from elemenpy.sm.boson import (Photon)
from elemenpy.sm.baryon import (Proton, Neutron)

from elemenpy.elem.atomicnucleus import (AtomicNucleus)

# -----------------------------------------------------------------------------
# DecayMode Enumeration
# -----------------------------------------------------------------------------
class DecayMode(Enum):
  """
  Spontaneous nuclear radioactive decay modes of a radionuclide.

  See: https://en.wikipedia.org/wiki/Radioactive_decay
       https://en.wikipedia.org/Nuclear_fission
  """
  UNKNOWN = 0   # unknown
  STABLE  = 1   # stable isotope

  # decays with emission of nucleons
  ALPHA_DECAY             = 2   # alpha partical emitted
  PROTON_EMISSION         = 3   # proton ejected
  NEUTRON_EMISSION        = 4   # neutron ejected
  DOUBLE_PROTON_EMISSION  = 5   # two protons simultaneously ejected
  SPONTANEOUS_FISSION     = 6   # Nucleus disintegration
  CLUSTER_DECAY           = 7   # Small nucleus larger than alph emitted

  # beta decays
  BETA_DECAY              = 8   # electron and electron anitneutrino emitted
  POSITRON_DECAY          = 9   # positron and electron neutrino emitted (beta+)
  ELECTRON_CAPTURE        = 10  # nucleus captures electron
  BOUND_STATE_BETA_DECAY  = 11  # beta decay with electron shell capture
  DOUBLE_BETA_DECAY       = 12  # 2 electrons and 2 electron anitneutrinos
  DOUBLE_ELECTRON_CAPTURE = 13  # nucleus absorbs 2 electrons, emits 2 neutrinos
  ELECTRON_CAPUTRE_POSITRON_EMISSION = 14 # nucleus absorms electron, emits pos
  DOUBLE_POSITRON_EMISSION = 15 # 2 positrons and 2 neutrions emitted

  # transitions
  ISOMERIC_TRANSITION     = 16  # excited nucleus release high-energy photon
  INTERNAL_TRANSITION     = 17  # excited nucleus transfers energy to ejected e 

# -----------------------------------------------------------------------------
# Beta- Class
# -----------------------------------------------------------------------------
class BetaN(Electron):
  Name    = 'Beta-'
  Symbol  = default_encoder('$greek(beta)$sup(-)')

  def __init__(self):
    Electron.__init__(self)

# -----------------------------------------------------------------------------
# Beta+ Class
# -----------------------------------------------------------------------------
class BetaP(Positron):
  Name    = 'Beta+'
  Symbol  = default_encoder('$greek(beta)$sup(+)')

  def __init__(self):
    Positron.__init__(self)

# -----------------------------------------------------------------------------
# Alpha Class
# -----------------------------------------------------------------------------
class Alpha(AtomicNucleus):
  def __init__(self):
    AtomicNucleus.__init__(self, 2, 4, name='alpha', symbol='$greek(alpha)')

# -----------------------------------------------------------------------------
# Baked Pre-Computed Decay Information
# -----------------------------------------------------------------------------
BakedInfo = {
  DecayMode.STABLE: {
    'dAdZ': (0, 0), 'emission': [], 'capture': []
  },
  
  # decays with emission of nucleons
  DecayMode.ALPHA_DECAY: {
    'dAdZ': (-4, -2), 'emission': [Alpha], 'capture': []
  },
  DecayMode.PROTON_EMISSION: {
    'dAdZ': (-1, -1), 'emission': [Proton], 'capture': []
  },
  DecayMode.NEUTRON_EMISSION: {
    'dAdZ': (-1, 0), 'emission': [Neutron], 'capture': []
  },
  DecayMode.DOUBLE_PROTON_EMISSION: {
    'dAdZ': (-2, -2), 'emission': [Proton] * 2, 'capture': []
  },
  DecayMode.SPONTANEOUS_FISSION: {
    'dAdZ': (0, 0),
    'emission': [], # calculated on required daughter nuclei
    'capture': [],
  }, # calculated
  DecayMode.CLUSTER_DECAY: {
    'dAdZ': (0, 0),
    'emission': [], # calculated on required daughter nuclei
    'capture': [],
  },
  
  # beta decays
  DecayMode.BETA_DECAY: {
    'dAdZ': (0, 1), 'emission': [BetaN, ElectronAntiNeutrino], 'capture': []
  },
  DecayMode.POSITRON_DECAY: {
    'dAdZ': (0, -1), 'emission': [BetaP, ElectronNeutrino], 'capture': []
  },
  DecayMode.ELECTRON_CAPTURE: {
    'dAdZ': (0, -1), 'emission': [ElectronNeutrino], 'capture': [Electron]
  },
  DecayMode.BOUND_STATE_BETA_DECAY: {
    'dAdZ': (0, 1),
    'emission': [ElectronAntiNeutrino],
    'capture': [Electron]  # captured into empty K-shell
  },
  DecayMode.DOUBLE_BETA_DECAY: {
    'dAdZ': (0, 2),
    'emission': [Electron, ElectronAntiNeutrino] * 2,
    'capture': []
  },
  DecayMode.DOUBLE_ELECTRON_CAPTURE: {
    'dAdZ': (0, -2),
    'emission': [ElectronNeutrino] * 2,
    'capture': [Electron] * 2  # from orbital electron
  },
  DecayMode.ELECTRON_CAPUTRE_POSITRON_EMISSION: {
    'dAdZ': (0, -2),
    'emission': [Positron, ElectronNeutrino, ElectronNeutrino],
    'capture': [Electron]  # from orbital electron
  },
  DecayMode.DOUBLE_POSITRON_EMISSION: {
    'dAdZ': (0, -2),
    'emission': [Positron, ElectronNeutrino] * 2,
    'capture': []
  },
  
  # transitions
  DecayMode.ISOMERIC_TRANSITION: {
    'dAdZ': (0, 0), 'emission': [Photon], 'capture': []
  },
  DecayMode.INTERNAL_TRANSITION: {
    'dAdZ': (0, 0), 'emission': [Electron], 'capture': []
  },
}

# -----------------------------------------------------------------------------
# NuclearDecay Class
# -----------------------------------------------------------------------------
class NuclearDecay:
  """ Spontaneous nuclear radioactive decay class. """

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
 
  @classmethod
  def emission_notation(klass, emission):
    sep = ' ' + default_encoder('$math(+)') + ' '
    return sep.join([p.symbol for p in emission])

  @classmethod
  def capture_notation(klass, capture):
    sep = ' ' + default_encoder('$math(+)') + ' '
    return sep.join([p.symbol for p in capture])

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
 
  def __init__(self,  mode=DecayMode.STABLE,
                      halflife=math.inf,
                      emission=[],
                      capture=[],
                      energy=0.0,
                      name=None):
    """
    Initializer.

    Parameters:
      mode        Decay mode. See DecayMode enumeration. May also be
                  string or integer enum equivalent.
      halflife    Halflife of embedding nucleus in seconds.
      emission    Decay emssions of subatomic and atomic particles.    
      capture     Captured subatomic particles.
      energy      Disintegraion engergy.
      name        Assigned name to decay. If None, then mode's name.
    """
    self._mode      = enumfactory(DecayMode, mode)
    self._halflife  = halflife
    self._emission  = emission
    self._capture   = capture
    self._energy    = energy
    if name is None:
      self._name = enum_to_str(self._mode, sep='-')
    else:
      self._name = default_encoder(name)
    self.check_and_set()

  def check_and_set(self):
    """
    Check and set decay data.

    Raises ValueError or TypeError exception on error.
    """
    info = BakedInfo[self.mode]

    self._dAdZ = info['dAdZ']

    # special decay cases
    if self.mode in [DecayMode.SPONTANEOUS_FISSION, DecayMode.CLUSTER_DECAY]:
      if len(self._emission) != 1:
        raise ValueError(f"{self.mode.name} requires an emitted "\
                          "isotope or nucleus to be specfied")
      p = self._emission[0]
      if not isderivedinstance(p, AtomicNucleus):
        raise TypeError(f"{self.p} is not a nucleus nor an isotope")
      lspec = len(self._capture)
      lexpt = len(info['capture'])
      if lspec != lexpt:
        raise ValueError(f"{self.mode.name} expected capture of "\
                         f"{lexpt} particle(s), {lspec} specified")
      self._dAdZ = (-p.A, -p.Z)

    else:
      # defaulting
      if len(self._emission) == 0: # create emmision defaults from baked info
        self._emission = []
        for p in info['emission']:
          self._emission.append(p())
      if len(self._capture) == 0: # create capture defaults from baked info
        self._capture = []
        for p in info['capture']:
          self._capture.append(p())

      # cross-check specifed against expected
      self.check_particle_list('emission', info['emission'], self._emission)
      self.check_particle_list('capture', info['capture'], self._capture)

  def check_particle_list(self, what, expected, specified):
    """
    Check specified particle list against expect.

    Raises ValueError or TypeError exception on error.

    Parameters:
      what      What is being checked string.
      expected  Expected particles.
      specified Specified particles.
    """
    expt  = expected.copy()
    lexpt = len(expt)
    lspec = len(specified)

    if lspec != lexpt:
      raise ValueError( f"{self.mode.name} expected {what} of "\
                        f"{lexpt} particle(s), {lspec} specified" )
    for p in specified:
      good = False
      for i in range(len(expt)):
        if isderivedinstance(p, expt[i]):
          del expt[i]
          good = True
          break
      if not good:
        raise TypeError(f"invalid {self.mode.name} {what} particle type {p}")

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(mode={self._mode.name!r}, halflife={self._halflife}, "\
            f"name={self._name!r})"

  def __str__(self):
    return self.name

  @property
  def mode(self):
    """ Return decay mode enum. """
    return self._mode

  @property
  def halflife(self):
    """ Return decay halflife in seconds. """
    return self._halflife

  @property
  def emission(self):
    """ Return list of decay emission particles. """
    return self._emission

  @property
  def capture(self):
    """ Return list of decay capture particles. """
    return self._capture

  @property
  def energy(self):
    """ Return decay TBD energy. """
    return self._energy

  @property
  def name(self):
    """ Return assigned name of this decay. """
    return self._name

  @property
  def dAdZ(self):
    """ Return the delta nuclide for decay daughter nucleus. """ 
    return self._dAdZ

  # fission:  N << n
  # fusion:   F = M * N
  # chemical: MN2 = M + 2 * N
  def decay(self, parent):
    """
    Decay parent nucleus using this decay properties.

    TODO: RDK this needs serious work. No captured particles
          or energies calculated, etc.

    Parameters:
      parent    Parent nucleus (AtomicNucleus (derived) instance).

    Returns:
      Tuple of any emitted particles plus daughter nucleus
      (emitted),daughter.
    """
    out = []
    for p in self.emission:
      out.append(p.copy())
    daughter = AtomicNucleus(parent.Z+self.dAdZ[1], parent.A+self.dAdZ[0]) 
    return tuple(out),daughter

  def print_properties(self, indent=0, **print_kwargs):
    """
    Print nucleus properties.

    Paramters:
      print_kwargs    Python3 print() keyword arguments.
    """
    emi = self.emission_notation(self.emission)
    cap = self.capture_notation(self.capture)

    print2cols([
      ('Name',     self.name),
      ('Mode',     self.mode.name),
      ('Halflife', fInfNum(self.halflife) + ' seconds'),
      ('Emission', emi),
      ('Capture',  cap),
      ('dAdZ',     self.dAdZ),
      ('Energy',   self.energy),],
        indent=indent, **print_kwargs)

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utnucleardecay as ut

  sys.exit(ut.utmain())

"""
The Standard Model of fundamental and composite particles.

Package:
  RoadNarrows elemenpy package.

File:
  standardmodel.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

import sys
import math
from enum import (Enum, IntFlag)
from copy import copy

from elemenpy.core.common import (enumfactory, enum_to_str, isiterable)
from elemenpy.core.format import (Format, Format4Some, default_encoder, fInfNum)
from elemenpy.core.prettyprint import (print2cols)
from elemenpy.core.rational import (Q)

from elemenpy.sm.spin import (SpinQuantumNumber)
from elemenpy.sm.electriccharge import (ElectricCharge)

OnlyThis = 42 # testing hook

# -----------------------------------------------------------------------------
# StandardModel Class
# -----------------------------------------------------------------------------
class StandardModel:
  """ The Standard Model class. """

  class Classification(IntFlag):
    """ Subatomic particle classification enumeration. """
    UNKNOWN = 0x0
    BOSON   = 0x1 # photon, gluon, ...
    HADRON  = 0x2 # composite quarks (not actually a part of the standard model)
    FERMION = 0x4 # electron, neutrino, ...

  class Family(Enum):
    """ Subatomic particle family enumeration. """
    UNKNOWN       = 0
    QUARK         = 1 # quarks
    LEPTON        = 2 # leptons
    BOSON         = 3 # bosons
    BARYON        = 4 # composite triquarks (not part of the standard model)
    MESON         = 5 # composite biquarks (not part of the standard model)

  class Statistics(Enum):
    """ Particle collective state statistics. """
    UNKNOWN   = 0
    FERMIONIC = 1 # Fermi-Dirac
    BOSONIC   = 2 # Bose-Einstein 

  class Interaction(IntFlag):
    """ Fundamental interactions (forces). """
    UNKNOWN         = 0x0
    GRAVITATION     = 0x1
    WEAK            = 0x2
    ELECTROMAGNETIC = 0x4
    STRONG          = 0x8

  class ParticleId(Enum):
    """ Subatomic particle identifiers. """
    UNKNOWN = 0
  
    #
    # Quark elementary particles.
    #
    UP_QUARK            = 1                   # u 
    DOWN_QUARK          = 2                   # d
    CHARM_QUARK         = 3                   # c
    STRANGE_QUARK       = 4                   # s
    TOP_QUARK           = 5                   # t
    BOTTOM_QUARK        = 6                   # b

    UP_ANTIQUARK        = -UP_QUARK           # u-bar
    DOWN_ANTIQUARK      = -DOWN_QUARK         # d-bar
    CHARM_ANTIQUARK     = -CHARM_QUARK        # c-bar
    STRANGE_ANTIQUARK   = -STRANGE_QUARK      # s-bar
    TOP_ANTIQUARK       = -TOP_QUARK          # t-bar
    BOTTOM_ANTIQUARK    = -BOTTOM_QUARK       # b-bar
  
    #
    # Lepton elementary particles.
    #
    ELECTRON              = 11                # e-
    MUON                  = 12                # mu-
    TAU                   = 13                # tau-
    ELECTRON_NEUTRINO     = 14                # nu_e
    MUON_NEUTRINO         = 15                # nu_mu
    TAU_NEUTRINO          = 16                # nu_tau

    POSITRON              = -ELECTRON         # e+
    ANTIMUON              = -MUON             # mu+
    ANTITAU               = -TAU              # tau+
    ELECTRON_ANTINEUTRINO = -ELECTRON_NEUTRINO # nu_e-bar
    MUON_ANTINEUTRINO     = -MUON_NEUTRINO    # nu_mu-bar
    TAU_ANTINEUTRINO      = -TAU_NEUTRINO     # nu_tau-bar
  
    #
    # Bosons scalar and vector elementary particles.
    #
    PHOTON            = 21                    # gamma
    GLUON             = 22                    # g
    W_BOSON_N         = 23                    # W-
    Z_BOSON           = 24                    # Z
    HIGGS_BOSON       = 25                    # H0

    W_BOSON_P         = -W_BOSON_N            # W+
  
    #
    # Hadron baryon composite particles.
    #
    PROTON            = 31                    # p
    NEUTRON           = 32                    # n

    ANTIPROTON        = -PROTON               # p-bar
    ANTINEUTRON       = -NEUTRON              # n-bar
  
    #
    # Hadron pseudoscalar meson composite particles.
    # Note: Not all are listed. Only those pseudoscalars with definitive
    #       quark pairs or decay product by some other particle.
    #
    PION_P                = 41                  # pi+
    PION_0                = 42                  # pi0
    CHARMED_ETA_MESON     = 43                  # eta_c
    BOTTOM_ETA_MESON      = 44                  # eta_b
    KAON_P                = 45                  # K+
    KAON_0                = 46                  # K0
    D_P_MESON             = 47                  # D+
    D_0_MESON             = 48                  # D0
    STRANGE_D_P_MESON     = 49                  # D+_s
    B_P_MESON             = 50                  # B+
    B_0_MESON             = 51                  # B0
    STRANGE_B_0_MESON     = 52                  # B0_s
    CHARMED_B_P_MESON     = 53                  # B+_c

    PION_N                = -PION_P             # pi-
    PION_0_BAR            = -PION_0             # pi0-bar
    KAON_N                = -KAON_P             # K-
    KAON_0_BAR            = -KAON_0             # K0-bar
    D_N_MESON             = -D_P_MESON          # D-
    D_0_BAR_MESON         = -D_0_MESON          # D0-bar
    STRANGE_D_N_MESON     = -STRANGE_D_P_MESON  # D-_s
    B_N_MESON             = -B_P_MESON          # B-
    B_0_BAR_MESON         = -B_0_MESON          # B0-bar
    STRANGE_B_0_BAR_MESON = -STRANGE_B_0_MESON  # B0_s-bar
    CHARMED_B_N_MESON     = -CHARMED_B_P_MESON  # B-_c

    NULL = 100                                  # null particle

  _instance = None

  def __new__(klass, *args, **kwargs):
    """
    Constructor.

    Parameters:
      args    Arguments passed to __init__()
      kwargs  Keyword arguments passed to __init__()

    Returns:
      StandardModel instance.
    """
    if not StandardModel._instance:
      StandardModel._instance = super(StandardModel, klass).__new__(klass)
    return StandardModel._instance

  def __init__(self):
    pass

  def __repr__(self):
    return f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return "Standard Model"

  # pre-parsed standard model symbols table
  SMMappingPre = {
    # quarks
    'u':        'u',                            # up
    'd':        'd',                            # down
    'c':        'c',                            # charm
    's':        's',                            # strange
    't':        't',                            # top
    'b':        'b',                            # bottom
    'u-bar':    'u$math(bar)',                  # antiup
    'd-bar':    'd$math(bar)',                  # antidown
    'c-bar':    'c$math(bar)',                  # anticharm
    's-bar':    's$math(bar)',                  # antistrange
    't-bar':    't$math(bar)',                  # antitop
    'b-bar':    'b$math(bar)',                  # antibottom
  
    # QCD color charge
    'R':          'R',                          # red
    'G':          'G',                          # green
    'B':          'B',                          # blue
    'R-bar':      'R$math(bbar)',               # antired
    'G-bar':      'G$math(bbar)',               # antigreen
    'B-bar':      'B$math(bbar)',               # antiblue

    # leptons
    'e':          'e',                          # electron alternative
    'e-':         'e$sup(-)',                   # electron
    'mu-':        '$greek(mu)$sup(-)',          # muon
    'tau-':       '$greek(tau)$sup(-)',         # tau
    'nu_e':       '$greek(nu)$sub(e)',          # electron neutrino
    'nu_mu':      '$greek(nu)$sub($greek(mu))', # muon neutrino
    'nu_tau':     '$greek(nu)$sub($greek(tau))',# tau neutrino
    'e+':         'e$sup(+)',                   # positron
    'mu+':        '$greek(mu)$sup(+)',          # antimuon
    'tau+':       '$greek(tau)$sup(+)',         # antitau
    'nu_e-bar':   '$greek(nu)$math(bar)$sub(e)', # electron antineutrino
    'nu_mu-bar':  '$greek(nu)$math(bar)$sub($greek(mu))',  # muon antineutrino
    'nu_tau-bar': '$greek(nu)$math(bar)$sub($greek(tau))', # tau antineutrino
  
    # bosons
    'gamma':      '$greek(gamma)',              # photon
    'g':          'g',                          # gluon
    'W-':         'W$sup(-)',                   # W- boson
    'Z':          'Z',                          # Z boson
    'H0':         'H$sup(0)',                   # Higgs boson
    'W+':         'W$sup(+)',                   # W+ boson
  
    # baryons
    'p':          'p',                          # proton 
    'p+':         'p$sup(+)',                   # proton alternative
    'n':          'n',                          # neutron 
    'n0':         'n$sup(0)',                   # neutron alternative
    'p-bar':      'p$math(bar)',                # antiproton 
    'n-bar':      'n$math(bar)',                # antineutron 
  
    # mesons
    'pi+':      '$greek(pi)$sup(+)',            # positive pion
    'pi0':      '$greek(pi)$sup(0)',            # pion naught
    'eta_c':    "$greek(eta)$sub(c)",           # charmed eta meson
    'eta_b':    "$greek(eta)$sub(b)",           # bottom eta meson
    'K+':       'K$sup(+)',                     # positive kaon
    'K0':       'K$sup(0)',                     # kaon naught
    'D+':       'D$sup(+)',                     # positive D meson
    'D0':       'D$sup(0)',                     # D naught meson
    'D+_s':     'D$sub(s)$sup(+)',              # strange positive D meson
    'B+':       'B$sup(+)',                     # positive B meson
    'B0':       'B$sup(0)',                     # B naught meson
    'B0_s':     'B$sub(s)$sup(0)',              # strange D meson
    'B+_c':     'B$sub(c)$sup(+)',              # charmed D meson
    'pi-':      '$greek(pi)$sup(-)',            # negative pion
    'pi0-bar':  '$greek(pi)$math(bar)$sup(0)',  # pion naught bar
    'K-':       'K$sup(-)',                     # negative kaon 
    'K0-bar':   'K$math(bar)$sup(0)',           # kaon naught bar meson
    'D-':       'D$sup(-)',                     # negative D meson
    'D0-bar':   'D$math(bar)$sup(0)',           # D naught bar meson
    'D-_s':     'D$sub(s)$sup(-)',              # strange negative D meson
    'B-':       'B$sup(-)',                     # negative B meson
    'B0-bar':   'B$math(bar)$sup(0)',           # B naught bar meson
    'B0_s-bar': 'B$math(bar)$sub(s)$sup(0)',    # strange B naught bar meson
    'B-_c':     'B$sub(c)$sup(-)',              # charmed negative B meson
  }

  def make_mapping(pre):
    post  = {}
    for key,expr in pre.items():
      post[key] = default_encoder(expr)
    return post

  if not default_encoder.has_table('sm'):
    SMMapping = make_mapping(SMMappingPre)

    default_encoder.install_encoder('sm', 'Standard Model symbols',
                          mapping=SMMapping)

# -----------------------------------------------------------------------------
# NullParticle Class
# -----------------------------------------------------------------------------
class NullParticle:
  """
  Null particle class.

  A null particle exists but does not interact with anything in the big U.

  Does it exist?
  """
  Pid     = StandardModel.ParticleId.NULL
  Name    = 'null'
  Symbol  = default_encoder("$math(null)")

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def print_null_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed null particle properties to output stream using
    the default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    print2cols([
      ('Pid',     klass.Pid.name),
      ('Name',    klass.Name),
      ('Symbol',  klass.Symbol),],
        indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    """ Initializer. """
    pass

  def __repr__(self):
    return f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return self.Name

  @property
  def pid(self):
    """ Return the particle id. """
    return self.Pid

  @property
  def name(self):
    """ Return standard name string of the particle. """
    return self.Name

  @property
  def symbol(self):
    """ Return standard symbol string of the particle. """
    return self.Symbol

# -----------------------------------------------------------------------------
# SubatomicParticle Class
# -----------------------------------------------------------------------------
class SubatomicParticle:
  """ 
  Subatomic particle base class.

  All wave to the particle.
  """
  #
  # Class Fixed Properties
  #
  Pid             = StandardModel.ParticleId.UNKNOWN    # unique identification
  Classification  = StandardModel.Classification.UNKNOWN  # broad classificaion
  Family          = StandardModel.Family.UNKNOWN          # partical family
  Statistics      = StandardModel.Statistics.UNKNOWN      # stats applied

  Name            = "dilaton"       # particle name (dilettante string theory)
  Symbol          = default_encoder('0$sup(0)') # particle symbol
  AltName         = ''              # alternative name
  AltSymbol       = ''              # alternative symbol in plain text

  AntiParticle    = NullParticle          # antiparticle
  RestMass        = 0.0                   # MeV/c^2
  ElecCharge      = ElectricCharge(0)     # electric charge
  QSpin           = SpinQuantumNumber(0)  # intrinsic spin quantum number
  MeanLifetime    = math.inf              # seconds
  DecayProducts   = []                    # subatomicparticle classes

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  @classmethod
  def is_matter(klass):
    """ Is the subatomic particle 'normal matter'? """
    return klass.Pid.value > 0

  @classmethod
  def is_antimatter(klass):
    """ Is the particle 'antimatter' as opposed to universe 'normal'? """
    return klass.Pid.value < 0

  @classmethod
  def classification_notation(klass):
    """ Return the particle's classification(s) as a text string. """
    name = ''
    enum = klass.Classification
    if enum & StandardModel.Classification.HADRON:
      name = StandardModel.Classification.HADRON.name + ' | '
      enum &= ~StandardModel.Classification.HADRON
    name += enum.name
    return name

  @classmethod
  def decay_notation(klass, decay):
    """
    Generate a particle's decay products notation with default encoder.

    Output format:
      sym [+ sym...]

    Parameters:
      decay - Decay particle class or list of decay particle classes.

    Returns:
      Formatted string.
    """
    sep = ' ' + default_encoder('$math(+)') + ' '
    if not isiterable(decay):
      decay = (decay)
    slist = [prod.Symbol for prod in decay]
    return sep.join(slist)

  @classmethod
  def print_subatomic_properties(klass, indent=0, **print_kwargs):
    """
    Print fixed subatomic particle properties to output stream using
    the default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    decay = '; '.join([klass.decay_notation(byprods)
                        for byprods in klass.DecayProducts])

    print2cols([
      ('Pid',             klass.Pid.name),
      ('Classification',  klass.classification_notation()),
      ('Family',          klass.Family.name),
      ('Statistics',      klass.Statistics.name),
      ('Name(s)',         f"{klass.Name} {klass.AltName}"),
      ('Symbol(s)',       f"{klass.Symbol} {klass.AltSymbol}"),
      ('AntiParticle',    klass.AntiParticle.Symbol),
      ('IsAntiMatter',    klass.is_antimatter()),
      ('RestMass',        f"{klass.RestMass} MeV/c^2"),
      ('Electric Charge', klass.ElecCharge),
      ('Spin',            klass.QSpin),
      ('MeanLifetime',    f"{fInfNum(klass.MeanLifetime)} seconds"),
      ('DecayProducts',   decay),],
        indent=indent, **print_kwargs)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Class Instance Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def __init__(self):
    pass

  def __repr__(self):
    return f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return self.Name

  @property
  def pid(self):
    """ Return the particle id. """
    return self.Pid

  @property
  def classification(self):
    """ Return the particle's classification(s). """
    return self.Classification

  @property
  def family(self):
    """ Return the particle's family. """
    return self.Family

  @property
  def statistics(self):
    """ Return the particle's overarching statistics. """
    return self.Statistics

  @property
  def name(self):
    """ Return standard name string of the particle. """
    return self.Name

  @property
  def symbol(self):
    """ Return standard symbol string of the particle. """
    return self.Symbol

  @property
  def altname(self):
    """ Return alternative name string of the particle. """
    return self.AltName

  @property
  def altsymbol(self):
    """ Return alternative symbol string of the particle. """
    return self.AltSymbol

  @property
  def antiparticle(self):
    """ Return the particle's antiparticle class (could be self). """
    return self.AntiParticle

  @property
  def restmass(self):
    """ Return the particle's rest mass (MeV/c^2). """
    return self.RestMass

  @property
  def electric_charge(self):
    """ Return the particle's electric charge. """
    return self.ElecCharge

  @property
  def spin_quantum_number(self):
    """ Return the particle's intrinsic spin quantum number. """
    return self.QSpin

  @property
  def mean_lifetime(self):
    """ Return the particle's mean lifetime (could be inf) (seconds). """
    return self.MeanLifetime

  @property
  def decay_products(self):
    """
    Return list or list of lists of the particle's decay products.

    Decay products are listed by subatomic particle class object.
    """
    return self.DecayProducts

  def copy(self):
    """ SubatomicParticle.copy() -> shallow copy of SubatomicParticle. """
    return copy(self)

  def print_state(self, indent=0, **print_kwargs):
    """
    Print the current state of this instance (particle) using the
    default encoder.

    Parameters:
      indent        Line indentation.
      print_kwargs  Print control keyword arguments.
    """
    pass


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utstandardmodel as ut

  sys.exit(ut.utmain())

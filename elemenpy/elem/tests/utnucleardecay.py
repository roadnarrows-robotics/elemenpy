"""
Unit test the nucleardecay module.

Package:
  RoadNarrows elemenpy python package.

File:
  utnucleus.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""
import io
from copy import copy
import random
import math

from elemenpy.core.format import (default_encoder)
from elemenpy.testing.ut import *

from elemenpy.elem.atomicnucleus import AtomicNucleus
import elemenpy.elem.nucleardecay as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsNuclearDecay = UTDataset('ds_nucleardecay',
    data=[
      sut.NuclearDecay(),

      sut.NuclearDecay(mode=sut.DecayMode.ALPHA_DECAY, halflife=3.5),
      sut.NuclearDecay(mode=sut.DecayMode.PROTON_EMISSION, halflife=1.0),
      sut.NuclearDecay(mode=sut.DecayMode.DOUBLE_PROTON_EMISSION, halflife=1.0),
      #sut.NuclearDecay(mode=sut.DecayMode.SPONTANEOUS_FISSION, halflife=1.0),
      sut.NuclearDecay(mode=sut.DecayMode.CLUSTER_DECAY, halflife=1.0,
          emission=[AtomicNucleus(20, 24, name='neon-24', symbol='Ne')]),

      sut.NuclearDecay(mode='beta_decay', halflife=3.3),
      sut.NuclearDecay(mode='positron_decay', halflife=9.3e-3),
      sut.NuclearDecay(mode=sut.DecayMode.ELECTRON_CAPTURE, halflife=9.3e-3),
      #sut.NuclearDecay(mode=sut.DecayMode.BOUND_STATE_BETA_DECAY),
      sut.NuclearDecay(mode=sut.DecayMode.DOUBLE_BETA_DECAY),
      sut.NuclearDecay(mode=sut.DecayMode.DOUBLE_ELECTRON_CAPTURE),
      #sut.NuclearDecay(mode=sut.DecayMode.ELECTRON_CAPTURE_POSITRON_EMISSION),

      sut.NuclearDecay(mode=sut.DecayMode.ISOMERIC_TRANSITION),
      #sut.NuclearDecay(mode=sut.DecayMode.INTERNAL_TRANSITION),
    ]
)

dsNuclei = UTDataset('ds_nuclei',
    data=[
      AtomicNucleus(1, 0, name='hydrogen', symbol='H'),

      AtomicNucleus(92, 238, name='uranium', symbol='U'),
      AtomicNucleus(27, 49, name='cobalt', symbol='Co'),
      AtomicNucleus(26, 45, name='iron', symbol='Fe'),
      #AtomicNucleus(26, 45, name='iron', symbol='Fe'),
      AtomicNucleus(90, 230), #, name='thorium', symbol='Th'),

      AtomicNucleus(6, 14, name='carbon', symbol='C'),
      AtomicNucleus(6, 11, name='carbon', symbol='C'),
      AtomicNucleus(19, 40, name='potassium', symbol='K'),
      #AtomicNucleus(19, 40, name='potassium', symbol='K'),
      AtomicNucleus(20, 48, name='calcium', symbol='Ca'),
      AtomicNucleus(56, 130, name='barium', symbol='Ba'),
      #AtomicNucleus(56, 130, name='barium', symbol='Ba'),

      AtomicNucleus(43, 99, name='technetium', symbol='Tc'),
      #AtomicNucleus(43, 99, name='technetium', symbol='Tc'),
    ]
)

dsDecay = UTDataset('ds_decay',
    data=list(zip(dsNuclearDecay.data, dsNuclei.data))
)

# the database of datasets
db = UTDsDb('db', ds=[dsNuclearDecay, dsNuclei, dsDecay])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrintProperties(UT):
  """ Unit test NuclearDecay.print_properties(). """
  def __init__(self, dskey):
    UT.__init__(self, "print_properties()", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      datum.print_properties(file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow} output info"] + lines

class utDecay(UT):
  """ Unit test NuclearDecay.decay(). """
  def __init__(self, dskey):
    UT.__init__(self, "decay()", dskey)

  def begin(self, sequencer, datum):
    self.nucleardecay = datum[0]
    self.parent       = datum[1]
    if str(self.nucleardecay) != 'stable':
      return (f"{self.nucleardecay} of {self.parent}", UTState.PASS)
    else:
      return (f"{self.nucleardecay} {self.parent}", UTState.PASS)

  def test(self, sequencer, datum):
    emission, daughter = self.nucleardecay.decay(self.parent)
    emits     = self.nucleardecay.emission_notation(emission)
    captures  = self.nucleardecay.capture_notation(self.nucleardecay.capture)
    if len(emits) > 0:
      emits = ' + ' + emits
    if len(captures) > 0:
      captures = ' + ' + captures
    arrow  = '\u27f6'   # long right arrow
    sp = 40 - len(sequencer.utwhat)
    if sp <= 0:
      sp = 1
    line =  f":{'':<{sp}}{self.parent.fqsymbol}{captures}  {arrow}   "\
            f"{daughter.fqsymbol} {emits}"
    #else:
    #  line = f":{'':<{sp}}{self.parent.symbol} {post} {daughter.symbol}"
    return UTState.PASS, line

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('NuclearDecay',
      "Test NuclearDecay class.",
      unittests=[
        utPrintProperties('ds_nucleardecay'),
        utDecay('ds_decay'),
      ]
    ),
  ],
)

utseq = UTSequencer('nucleardecay', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test nucleardecay module.")

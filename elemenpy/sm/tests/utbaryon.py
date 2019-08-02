"""
Unit test the baryon module.

Package:
  RoadNarrows elemenpy python package.

File:
  utbaryon.py

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
import math
import io

from elemenpy.core.prettyprint import (print2cols)

from elemenpy.testing.ut import *

import elemenpy.sm.baryon as sut

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

##-
class utPrintProperties(UT):
  """ Unit test print properties methods. """
  def __init__(self, dskey, classobj):
    UT.__init__(self, "print_properties", dskey)
    self.classobj = classobj

  def begin(self, sequencer, datum):
    #classobj  = datum
    classname = self.classobj.__name__
    self.func = None
    for funcname in ['print_properties', 'print_baryon_properties']:
      try:
        self.func = getattr(self.classobj, funcname)
        break
      except AttributeError:
        self.func = None
    if self.func is not None:
      return (f"{classname}.{funcname}()", UTState.PASS)
    else:
      return (f"{classname}.NO_PRINT_METHOD()", UTState.FAIL)

  def test(self, sequencer, datum):
    if self.func is None:
      return UTState.FAIL, f"{uRArrow} cannot print"
    with io.StringIO() as output:
      self.func(indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow}"] + lines

##-
class utPrintRegistered(UT):
  """ Unit test print registered baryon family. """
  def __init__(self, dskey):
    UT.__init__(self, "family", dskey)

  def begin(self, sequencer, datum):
    return (f"registered.family", UTState.PASS)

  def test(self, sequencer, datum):
    family = [(name,cls) for name,cls in sut.Baryon.baryon_family().items()]
    with io.StringIO() as output:
      print2cols(family, indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow}"] + lines

##-
class utNew(UT):
  """ Unit test baryon instantiation. """
  def __init__(self, dskey, classobj, dskey_out):
    UT.__init__(self, "new", dskey)
    self.classobj = classobj
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.randcolor  = datum
    self.pf         = UTState.PASS
    return (f"{self.classobj.__name__}(randcolor={self.randcolor})", self.pf)

  def test(self, sequencer, datum):
    try:
      b = self.classobj(randcolor=self.randcolor)
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(b)
      return (UTState.PASS, f"{uRArrow} {b}(...)")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

##-
class utPrintState(UT):
  """ Unit test print state methods. """
  def __init__(self, dskey):
    UT.__init__(self, "print_state", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}.print_state()", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      datum.print_state(indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow}"] + lines

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsBase    = UTDataset('ds_base', data=[sut.Baryon])
dsFamily  = UTDataset('ds_family',
    data=[cls for name,cls in sut.Baryon.baryon_family().items()])
dsRandColor = UTDataset('ds_randcolor', data=[False, True, True, True])

# the database of datasets
db = UTDsDb('db', ds=[dsBoilOne, dsBase, dsFamily, dsRandColor])

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('base',
      "Test Baryon bass class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Baryon),
        utPrintRegistered('ds_boil_one'),
      ]
    ),
    UTSubsys('proton',
      "Test Baryon derived Proton class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Proton),
        utNew('ds_randcolor', classobj=sut.Proton, dskey_out='ds_proton'),
        utPrintState('ds_proton'),
      ]
    ),
    UTSubsys('antiproton',
      "Test Baryon derived AntiProton class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiProton),
        utNew('ds_randcolor', classobj=sut.AntiProton,
                              dskey_out='ds_antiproton'),
        utPrintState('ds_antiproton'),
      ]
    ),
    UTSubsys('neutron',
      "Test Baryon derived Neutron class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Neutron),
        utNew('ds_randcolor', classobj=sut.Neutron, dskey_out='ds_neutron'),
        utPrintState('ds_neutron'),
      ]
    ),
    UTSubsys('antineutron',
      "Test Baryon derived AntiNeutron class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiNeutron),
        utNew('ds_randcolor', classobj=sut.AntiNeutron,
                              dskey_out='ds_antineutron'),
        utPrintState('ds_antineutron'),
      ]
    ),
  ],
)

utseq = UTSequencer('baryon', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test baryon module.")

"""
Unit test the boson module.

Package:
  RoadNarrows elemenpy python package.

File:
  utboson.py

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

from elemenpy.testing.ut import *
from elemenpy.core.prettyprint import (print2cols)

import elemenpy.sm.boson as sut

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

##-
class utPrintProperties(UT):
  """ Unit test print properties methods. """
  def __init__(self, dskey):
    UT.__init__(self, "properties", dskey)

  def begin(self, sequencer, datum):
    classobj  = datum
    classname = classobj.__name__
    self.func = None
    for funcname in ['print_properties', 'print_boson_properties']:
      try:
        self.func = getattr(classobj, funcname)
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
  """ Unit test print registered boson family. """
  def __init__(self, dskey):
    UT.__init__(self, "family", dskey)

  def begin(self, sequencer, datum):
    return (f"registered.family", UTState.PASS)

  def test(self, sequencer, datum):
    family = [(name,cls) for name,cls in sut.Boson.boson_family().items()]
    with io.StringIO() as output:
      print2cols(family, indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow}"] + lines

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

##-
class utNewGluons(UT):
  """ Unit test instantiating gluons. """
  def __init__(self, dskey, dskey_out):
    UT.__init__(self, "new", dskey)
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.color      = datum[0]
    self.anticolor  = datum[1]
    self.pf         = datum[2]
    return (f"Gluon({self.color}, {self.anticolor})", self.pf)

  def test(self, sequencer, datum):
    try:
      g = sut.Gluon(self.color, self.anticolor)
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(g)
      return (UTState.PASS,
          f"{uRArrow} {g}({g.color_charge}, {g.anticolor_charge})")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

##-
class utNewPhotons(UT):
  """ Unit test instantiating photons. """
  def __init__(self, dskey, dskey_out):
    UT.__init__(self, "new", dskey)
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.pf         = datum[1]
    return (f"Photon()", self.pf)

  def test(self, sequencer, datum):
    try:
      p = sut.Photon()
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(p)
      return (UTState.PASS,
        f"{uRArrow} photon()")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

##-
class utNewWBosonN(UT):
  """ Unit test instantiating W- bosons. """
  def __init__(self, dskey, dskey_out):
    UT.__init__(self, "new", dskey)
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.pf         = datum[1]
    return (f"WBosonN()", self.pf)

  def test(self, sequencer, datum):
    try:
      wn = sut.WBosonN()
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(wn)
      return (UTState.PASS,
        f"{uRArrow} wn()")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

##-
class utNewWBosonP(UT):
  """ Unit test instantiating W+ bosons. """
  def __init__(self, dskey, dskey_out):
    UT.__init__(self, "new", dskey)
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.pf         = datum[1]
    return (f"WBosonP()", self.pf)

  def test(self, sequencer, datum):
    try:
      wp = sut.WBosonP()
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(wp)
      return (UTState.PASS,
        f"{uRArrow} wp()")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

##-
class utNewZBoson(UT):
  """ Unit test instantiating Z bosons. """
  def __init__(self, dskey, dskey_out):
    UT.__init__(self, "new", dskey)
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.pf         = datum[1]
    return (f"ZBoson()", self.pf)

  def test(self, sequencer, datum):
    try:
      z = sut.ZBoson()
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(z)
      return (UTState.PASS,
        f"{uRArrow} z()")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

##-
class utNewHiggsBoson(UT):
  """ Unit test instantiating Higgs bosons. """
  def __init__(self, dskey, dskey_out):
    UT.__init__(self, "new", dskey)
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.pf         = datum[1]
    return (f"HiggsBoson()", self.pf)

  def test(self, sequencer, datum):
    try:
      higgs = sut.HiggsBoson()
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(higgs)
      return (UTState.PASS,
        f"{uRArrow} higgs()")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsBase      = UTDataset('ds_base', data=[sut.Boson])
dsFamily    = UTDataset('ds_family',
    data=[cls for name,cls in sut.Boson.boson_family().items()])
dsGluonInit = UTDataset('ds_gluon_init',
    data=[('red', 'antigreen', UTState.PASS),
          ('blue', 'magenta', UTState.PASS),
          ('antigreen', 'blue', UTState.FAIL),
          ('blue', 'antiblue', UTState.FAIL),
          ('blue', 'red', UTState.FAIL),
          ('green', 'antired', UTState.PASS),])
dsPhotonInit = UTDataset('ds_photon_init',
    data=[('', UTState.PASS),
          ('', UTState.PASS),])
dsWBosonNInit = UTDataset('ds_wn_init',
    data=[('', UTState.PASS),
          ('', UTState.PASS),])
dsWBosonPInit = UTDataset('ds_wp_init',
    data=[('', UTState.PASS),
          ('', UTState.PASS),])
dsZBosonInit = UTDataset('ds_z_init',
    data=[('', UTState.PASS),
          ('', UTState.PASS),])
dsHiggsBosonInit = UTDataset('ds_higgs_init',
    data=[('', UTState.PASS),
          ('', UTState.PASS),])

# the database of datasets
db = UTDsDb('db',
  ds=[dsBoilOne,
      dsBase, dsFamily,
      UTDataset('ds_gluon_class', data=[sut.Gluon]), dsGluonInit,
      UTDataset('ds_photon_class', data=[sut.Photon]), dsPhotonInit,
      UTDataset('ds_wn_class', data=[sut.WBosonN]), dsWBosonNInit,
      UTDataset('ds_wp_class', data=[sut.WBosonP]), dsWBosonPInit,
      UTDataset('ds_z_class', data=[sut.ZBoson]), dsZBosonInit,
      UTDataset('ds_higgs_class', data=[sut.HiggsBoson]), dsHiggsBosonInit,
  ])

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
#RDK boson gluon photon higgs wboson- wboson+ zboson
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('base',
      "Test Boson base class.",
      unittests=[
        utPrintProperties('ds_base'),
        utPrintRegistered('ds_boil_one'),
      ]
    ),
    UTSubsys('gluon',
      "Test Gluon derived class.",
      unittests=[
        utPrintProperties('ds_gluon_class'),
        utNewGluons('ds_gluon_init', dskey_out='ds_gluons'),
        utPrintState('ds_gluons'),
      ]
    ),
    UTSubsys('photon',
      "Test Photon derived class.",
      unittests=[
        utPrintProperties('ds_photon_class'),
        utNewPhotons('ds_photon_init', dskey_out='ds_photons'),
        utPrintState('ds_photons'),
      ]
    ),
    UTSubsys('w-',
      "Test WBosonN (W-) derived class.",
      unittests=[
        utPrintProperties('ds_wn_class'),
        utNewWBosonN('ds_wn_init', dskey_out='ds_wn'),
        utPrintState('ds_wn'),
      ]
    ),
    UTSubsys('w+',
      "Test WBosonP (W+) derived class.",
      unittests=[
        utPrintProperties('ds_wp_class'),
        utNewWBosonP('ds_wp_init', dskey_out='ds_wp'),
        utPrintState('ds_wp'),
      ]
    ),
    UTSubsys('z',
      "Test ZBoson derived class.",
      unittests=[
        utPrintProperties('ds_z_class'),
        utNewZBoson('ds_z_init', dskey_out='ds_z'),
        utPrintState('ds_z'),
      ]
    ),
    UTSubsys('higgs',
      "Test HiggsBoson derived class.",
      unittests=[
        utPrintProperties('ds_higgs_class'),
        utNewHiggsBoson('ds_higgs_init', dskey_out='ds_higgs'),
        utPrintState('ds_higgs'),
      ]
    ),
  ],
)

utseq = UTSequencer('boson', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test boson module.")

"""
Unit test the color module.

Package:
  RoadNarrows elemenpy python package.

File:
  utcolor.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""
import random
from enum import Enum
import io

from elemenpy.testing.ut import *

import elemenpy.core.color as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
# null and singleton datasets
dsNotifiers = UTDataset('ds_notifiers',           # tcw notifiers plus unknown
                data=['debug', 'info', 'warn', 'error', 'critical', 'ooga'])

# the database of datasets
db = UTDsDb('db', ds=[dsBoilOne, dsNotifiers])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utCPrint(UT):
  """ Unit test color cprint(). """
  def __init__(self, dskey):
    UT.__init__(self, "cprint()", dskey)

  def begin(self, sequencer, datum):
    self.colors = sequencer['tcw'].colors()
    return (f"cprint(...)", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      i = 1
      for color in self.colors:
        sequencer['tcw'].cprint(
          'normal', f"{i:>2}. ",
          color, f"The quick {color} fox jumps over the lazy dog.",
          file=output)
        i += 1
      olines = output.getvalue().split('\n')
    if not olines[-1]:
      olines = olines[:-1]
    return UTState.PASS, [f"{uRArrow} output with color"] + olines

class utNCPrint(UT):
  """ Unit test color ncprint(). """
  def __init__(self, dskey):
    UT.__init__(self, "ncprint()", dskey)

  def begin(self, sequencer, datum):
    return (f"ncprint(...)", UTState.PASS)

  def test(self, sequencer, datum):
    ncprint = sequencer['tcw'].ncprint
    with io.StringIO() as output:
      ncprint("Boy: Look Ma! No hands.", file=output, end=' ')
      ncprint("(crash, bam, ouch)", file=output)
      ncprint(" Ma: Get a job boy!",file=output,  flush=True)
      olines = output.getvalue().split('\n')
    if not olines[-1]:
      olines = olines[:-1]
    return UTState.PASS, [f"{uRArrow} output with no color"] + olines

class utNotifier(UT):
  """ Unit test color notifier. """
  Notifiers = ['debug', 'info', 'warn', 'error', 'critical']

  def __init__(self, dskey):
    UT.__init__(self, "notifier", dskey)

  def begin(self, sequencer, datum):
    self.what = datum
    if self.what in utNotifier.Notifiers:
      return (f"{self.what}(...)", UTState.PASS)
    else:
      return (f"{self.what}(...)", UTState.FAIL)

  def test(self, sequencer, datum):
    if self.what == 'debug':
      self.notifier = sequencer['tcw'].debug
    elif self.what == 'info':
      self.notifier = sequencer['tcw'].info
    elif self.what == 'warn':
      self.notifier = sequencer['tcw'].warn
    elif self.what == 'error':
      self.notifier = sequencer['tcw'].error
    elif self.what == 'critical':
      self.notifier = sequencer['tcw'].critical
    else:
      return (UTState.FAIL, f"{self.what!r} is an unknown notifier")

    with io.StringIO() as output:
      self.notifier(f"This is a {self.what} notifier. That is all.",
                    file=output)
      notice = output.getvalue().split('\n')
    if not notice[-1]:
      notice = notice[:-1]
    res = UTState.PASS
    ans = [f"{uRArrow} output"] +  notice
    return res, ans

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('TermColorWriter', "Test terminal color writer class.",
      unittests=[
        utCPrint('ds_boil_one'),
        utNCPrint('ds_boil_one'),
        utNotifier('ds_notifiers'),
      ]
    ),
  ],
)

utseq = UTSequencer('color', suite, db, tcw=sut.TermColorWriter())

utmain = lambda: UTMainTemplate(utseq, "Unit test color module.")

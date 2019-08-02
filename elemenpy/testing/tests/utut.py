"""
Unit test the unit testing framework.

Package:
  RoadNarrows elemenpy python package.

File:
  utut.py

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

from elemenpy.testing.ut import *

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
# vector 1 dataset
dsvec1 = UTDataset('vec1',
 data = [ [1,2,3], [0.9, -3.2 , 3.14], [1, 0, 0],
          [0, 0, 0], [2.18, 1.618, 0], [-108, 7, -9.2], ]
)

# vector 2 dataset
dsvec2 = UTDataset('vec2',
  data = [ [1,1,1], [-5, 45.6], [2, 4, 8], ]
)

# random integers dataset
dsrandi = UTDataset('randint',
                data = [random.randint(1,100) for i in range(10)])

# random floats dataset
dsrandf = UTDataset('randfloat',
                data = [10.0 * random.random() for i in range(10)])

# dataset to unit test UTDataset. Format: [opcode, (opands)]
dsds = UTDataset('UTDataset',
  data = [['create',  ('random', 'numbers')],
          #['print', ('vec2', )],
          ['copy', ('vec1',)],
          ['add', ('randint', 'randfloat')],
          ['iadd', ('randfloat', 'vec2')],
          ['append', ('vec2', [3, 4, 5])],
          ['pair', ('randint', 'randfloat')],
  ]
)

# Dataset to unit test UTDsDB. Format: [opcode, (opands)]
dsdb = UTDataset('UTDsDb',
  data = [['setitem', ('nums', [random.randint(50, 59) for i in range(5)],)],
          ['dup', ('randint', 'randint2')],
          ['del', ('nums', )],
          ['del.error', ('numbnuts', )],
  ]
)

# Dataset to unit test UTSuite. Format: [opcode, (opands)]
dssuite = UTDataset('UTSuite',
  data = [
  ]
)

# the database of datasets
db = UTDsDb('utdb', ds=[dsvec1, dsvec2, dsrandi, dsrandf, dsds, dsdb, dssuite])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utDsClass(UT):
  """ Test UTDataset class. """
  def __init__(self, dskey):
    UT.__init__(self, 'UTDataset', dskey)

  def begin(self, sequencer, datum):
    self.opcode = datum[0]
    self.opands = datum[1]

    i = self.opcode.find('.error')
    if i < 0:
      expect = UTState.PASS
    else:
      self.opcode = self.opcode[:i]
      expect = UTState.FAIL
    return f"{self.opcode}{self.opands}", expect

  def test(self, sequencer, datum):
    if self.opcode == 'create':
      return self.test_create(sequencer)
    elif self.opcode == 'copy':
      return self.test_copy(sequencer)
    elif self.opcode == 'add':
      return self.test_add(sequencer)
    elif self.opcode == 'iadd':
      return self.test_iadd(sequencer)
    elif self.opcode == 'append':
      return self.test_append(sequencer)
    elif self.opcode == 'pair':
      return self.test_pair(sequencer)
    elif self.opcode == 'print':
      return self.test_print(sequencer)
    else:
      return (UTState.FAIL, f"{self.opcode!r} unknown operator")

  def test_create(self, sequencer):
    how  = self.opands[0] # 'random'
    name = self.opands[1]
    if how == 'random':
      dslen = 10
      ds = UTDataset(name, [random.randint(1,100) for i in range(dslen)])
      if len(ds) == dslen:
        res = UTState.PASS
        ans = [f"{uRArrow} created", f"{ds.name}: {ds.data}"]
      else:
        res = UTState.FAIL
        ans = f"{len(ds)} {uNeq} {dslen}"
    else:
      res = UTState.FAIL
      ans = f"{how!r} unknown operand"
    return (res, ans)

  def test_copy(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds  = ds1.copy()
    if ds.name == ds1.name and ds.data == ds1.data:
      res = UTState.PASS
      ans = [f"{uRArrow} copied", f"{ds.name}: {ds.data}"]
    else:
      res = UTState.FAIL
      ans = [ f"{ds.name} data {uNeq} {ds1.name} data",
              f"{ds.data}",
              f"{ds1.data}"]
    return (res, ans)

  def test_add(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds2 = sequencer.dsdb[self.opands[1]]
    ds = ds1 + ds2
    if len(ds) != len(ds1) + len(ds2):
      res = UTState.FAIL
      ans = f"{len(ds)} {uNeq} {len(ds1)}+{len(ds2)}"
    elif ds[0] != ds1[0] or ds[-1] != ds2[-1]:
      res = UTState.FAIL
      ans = f"bad add"
    else:
      res = UTState.PASS
      ans = [f"{uRArrow} added", f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_iadd(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds2 = sequencer.dsdb[self.opands[1]]
    ds = ds1.copy()
    ds += ds2
    if len(ds) != len(ds1) + len(ds2):
      res = UTState.FAIL
      ans = f"{len(ds)} {uNeq} {len(ds1)}+{len(ds2)}"
    elif ds[0] != ds1[0] or ds[-1] != ds2[-1]:
      res = UTState.FAIL
      ans = f"bad add"
    else:
      res = UTState.PASS
      ans = [ f"{uRArrow} in-place added",
              f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_append(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    datum = self.opands[1]
    ds = ds1.copy()
    ds.append(datum)
    if len(ds) != len(ds1) + 1:
      res = UTState.FAIL
      ans = f"{len(ds)} {uNeq} {len(ds1)}+1"
    elif ds[0] != ds1[0] or ds[-1] != datum:
      res = UTState.FAIL
      ans = f"bad add"
      ans = [ f"bad append",
              f"{ds.data}",
              f"{datum}",
              f"{ds1.data}"]
    else:
      res = UTState.PASS
      ans = [ f"{uRArrow} appended",
              f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_pair(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    ds2 = sequencer.dsdb[self.opands[1]]
    ds = ds1.pair(ds2)
    if len(ds) != len(ds1) * len(ds2):
      res = UTState.FAIL
      ans = f"{len(ds)} {uNeq} {len(ds1)}x{len(ds2)}"
    else:
      res = UTState.PASS
      ans = [ f"{uRArrow} paired",
              f"{ds.name}: {ds.data}" ]
    return (res, ans)

  def test_print(self, sequencer):
    ds = sequencer.dsdb[self.opands[0]]
    print(f"name={ds.name}, data={ds.data}")
    return UTState.PASS, f"{uRArrow} printed"

class utDsDbClass(UT):
  """ Test UTDsDB class. """
  def __init__(self, dskey):
    UT.__init__(self, 'UTDsDb', dskey)

  def begin(self, sequencer, datum):
    self.opcode = datum[0]
    self.opands = datum[1]

    i = self.opcode.find('.error')
    if i < 0:
      expect = UTState.PASS
    else:
      self.opcode = self.opcode[:i]
      expect = UTState.FAIL
    return f"{self.opcode}{self.opands}", expect

  def test(self, sequencer, datum):
    if self.opcode == 'setitem':
      return self.test_setitem(sequencer)
    elif self.opcode == 'dup':
      return self.test_dup(sequencer)
    elif self.opcode == 'del':
      return self.test_del(sequencer)
    else:
      return (UTState.FAIL, f"{self.opcode!r} unknown operator")

  def test_setitem(self, sequencer):
    name = self.opands[0]
    data = self.opands[1]
    try:
      sequencer.dsdb[name] = (name, data)
      ds = sequencer.dsdb[name]
      res = UTState.PASS
      ans = f"{uRArrow} added ds {ds.name!r}"
    except (KeyError):
      res = UTState.FAILEd
      ans = f"{uRArrow} failed to add new ds"
    return (res, ans)

  def test_dup(self, sequencer):
    ds1 = sequencer.dsdb[self.opands[0]]
    name = self.opands[1]
    sequencer.dsdb[name] = ds1.copy()
    ds = sequencer.dsdb[name]
    ds[0] = 1234567890
    if len(ds) != len(ds1):
      res = UTState.FAIL
      ans = f"{len(ds)} {uNeq} {len(ds1)}"
    elif ds[0] == ds1[0]:
      res = UTState.FAIL
      ans = [ f"bad dup - data to same reference"
              f"{ds.data}",
              f"{ds1.data}"]
    else:
      res = UTState.PASS
      ans = [ f"{uRArrow} duped",
              f"{ds.name}: [{ds[0]}, ..., {ds[-1]}]"]
    return (res, ans)

  def test_del(self, sequencer):
    name = self.opands[0]
    try:
      del sequencer.dsdb[name]
    except (KeyError):
      return (UTState.FAIL, f"{name!r} ds not in db")
    if name in sequencer.dsdb:
      return (UTState.FAIL, f"{name!r} ds did not delete from db")
    else:
      return (UTState.PASS, f"ds deleted")

class utDotProduct(UT):
  """ Test operations on two datasets class. """
  uDot = '\u22c5'   # dot product operator symbol

  def __init__(self, dskey, dskey2):
    UT.__init__(self, 'dotproduct', dskey, dskey2)
    self.rhs = UTDsAux(self.args[0])

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    return  (f"{datum} {utDotProduct.uDot} {self.rhs.datum()}",
            self.expect(datum))
  
  def test(self, sequencer, datum):
    try:
      f = self.dot(datum, self.rhs.datum())
      res = UTState.PASS
      ans = f"= {f}"
    except (IndexError) as e:
      res = UTState.FAIL
      ans = [ f"{uRArrow} error",
              f"vectors of unequal sizes "\
              f"{len(datum)} {uNeq} {len(self.rhs.datum())}" ]
    except (TypeError, ValueError) as e:
      res = UTState.FAIL
      ans = [f"{uRArrow} error", e]

    return (res, ans)

  def end(self, sequencer):
    self.rhs += 1

  def expect(self, datum):
    if len(datum) == len(self.rhs.datum()):
      return UTState.PASS
    else:
      return UTState.FAIL

  def dot(self, v1, v2):
    f = 0
    n = len(v1)
    for i in range(n):
      f += v1[i] * v2[i]
    return f

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
ssInteg = UTSubsys('integrity', 'Test UT classes.',
                unittests=[
                  utDsClass('UTDataset'),
                  utDsDbClass('UTDsDb'),
                  #utSuiteClass('UTSuite'),
                ])

ssDot = UTSubsys('vector', 'Test vector math to test UT further.',
                unittests=[utDotProduct('vec1', 'vec2')])

suite = UTSuite('testsuite', subsystems=[ssInteg, ssDot])

utseq = UTSequencer('ut', suite, db)

utmain = lambda: UTMainTemplate(utseq,
                                "Unit test the unit test framework module")

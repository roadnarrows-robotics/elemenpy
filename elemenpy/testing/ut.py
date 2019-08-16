"""
Unit testing framework.

It is intended that each (sub)package public MODULE should import and
execute the corresponding .tests.utMODULE specific unit tests under
the __main__ section of MODULE.

Acronyms:
  SUT     System Under Test
  SSUT    Subsystem Under Test
  UT      Unit Test
  DS      Dataset
  DB      Database

Infoasciic:
                                      UT...        Unit test operates over one
                                       |           or more datasets
                                       |
Dataset of test       UTDataset...  UTSubsys...    Collection of subsystem
data (list wrapper)       |            |           unit tests (list wrapper)
                          |            |
Database of datasets    UTDsDb       UTSuite       Set of all subsystem tests
   (dict wrapper)         |            |           (dict wrapper)
                          |            |
                          --------------
                                |
Runs all specified          UTSequencer <-- UTCli  Provides command-line
tests with options                                 interface to parse input test
                                                   options and arguments

Package:
  RoadNarrows elemenpy python package.

File:
  ut.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

import os
import sys
import io
from enum import Enum 
from copy import copy
import argparse

# minimize imports from elemenpy package since also candiate sut's
from elemenpy.core.common import (enumfactory, indexget, termsize)
from elemenpy.core.format import (unicode_encoder)
from elemenpy.core.color import (TermColors)
from elemenpy.core.args import (SmartFormatter)

# -----------------------------------------------------------------------------
# UTState Enumeration
# -----------------------------------------------------------------------------
class UTState(Enum):
  """ Unit test state enumeration."""
  PASS  = 0   # test passed
  WARN  = 1   # test passed, but with warnings
  FAIL  = 2   # test failed
  FATAL = 3   # crash n' burn - test not well framed
  WAIT  = 4   # test in progress

# -----------------------------------------------------------------------------
# Class UTStats
# -----------------------------------------------------------------------------
class UTStats:
  """
  Test result statistics class.

  Statistics are kept on unit tests, subsystem tests, and as a grand
  total.
  """

  def __init__(self, start=None):
    """
    Initializer.

    Parameters:
      start   Starting statistics. If None, then zeros.
    """
    self.reset()
    if start is not None:
      self += start

  def reset(self):
    """ Reset statistics. """
    self.total    = 0 # total tests ran
    self.passed   = 0 # total tests passed
    self.epass    = 0 # total test expected to pass 
    self.failed   = 0 # total tests failed
    self.efail    = 0 # total tests expected to fail
    self.warnings = 0 # total tests passed but with warnings

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
      f"({self.total!r}, {self.passed!r}, {self.failed!r}, {self.warnings!r})"

  def __str__(self):
    return  f"{self.total:>3} total, "\
        f"{self.passed:>3}/{self.epass:<3} passed, "\
        f"{self.failed:>3}/{self.efail:<3} failed, "\
        f"{self.warnings:>3} warnings"

  def __add__(self, rhs):
    """ Addition. Return self + rhs. """
    return UTStats(self.total+rhs.total,
        self.passed+rhs.passed, self.epass+rhs.epass,
        self.failed+rhs.failed, self.efail+rhs.efail,
        self.warnings+rhs.warnings)

  def __iadd__(self, rhs):
    """ In-place addition. self += rhs. """
    self.total    += rhs.total
    self.passed   += rhs.passed
    self.epass    += rhs.epass
    self.failed   += rhs.failed
    self.efail    += rhs.efail
    self.warnings += rhs.warnings
    return self

  def bump_expected(self, expect):
    """
    Increment relevant expected test result statistics by one.

    Parameters:
      expect   UTState convertible value.
    """
    e = enumfactory(UTState, expect)
    if e == UTState.PASS:
      self.epass += 1
    elif e == UTState.FAIL:
      self.efail += 1
    else:
      raise ValueError(f"{e.name} has no expected")

  def bump_result(self, state):
    """
    Increment relevant test results statistics by one.

    Parameters:
      state   UTState convertible value.
    """
    r = enumfactory(UTState, state)
    if r == UTState.PASS:
      self.total  += 1
      self.passed += 1
    elif r == UTState.WARN:
      self.total    += 1
      self.passed   += 1
      self.warnings += 1
    elif r == UTState.FAIL:
      self.total  += 1
      self.failed += 1
    else:
      raise ValueError(f"{r.name} has no statistics")

# -----------------------------------------------------------------------------
# Class Colorize
# -----------------------------------------------------------------------------
class Colorize:
  """
  Color class. Look ANSI!
  """
  # Unit test state - output color mapping
  StateColor = {
    UTState.PASS:   'green',
    UTState.WARN:   'yellow',
    UTState.FAIL:   'lightred',
    UTState.FATAL:  'lightpurple',
    UTState.WAIT:   'lightgray',
  }

  def __init__(self):
    """ Initializer. """
    self.tc = TermColors() # terminal supported colors (auto enabled)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return f"Colorize"

  def __call__(self, obj, color):
    """
    Color object.

    Parameters:
      obj   Python object to color. String of object str(obj) will be used.
      color Color to use.

    Returns:
      Color string.
    """
    return self.obj(obj, color)

  def enable(self):
    """ Enable color output, if possible. """
    self.tc.enable()

  def disable(self):
    """ Disable color output. """
    self.tc.disable()

  def colors(self):
    """ List available colors. """
    return list(self.tc.keys())

  def obj(self, obj, color):
    """
    Color object.

    Parameters:
      obj   Python object to color. String of object str(obj) will be used.
      color Color to use.

    Returns:
      Color string.
    """
    return f"{self.tc[color]}{str(obj)}{self.tc['normal']}"

  def utstate(self, state):
    """
    Color unit test state.

    Parameters:
      state   UTState enum.

    Returns:
      Color string.
    """
    v = enumfactory(UTState, state)
    c = Colorize.StateColor[v]
    return f"{self.tc[c]}{v.name}{self.tc['normal']}"

  def using_color(self):
    """ Returns True/False if color is enabled. """
    return self.tc.usingColor()

# -----------------------------------------------------------------------------
# Useful Shorthands
# -----------------------------------------------------------------------------
Ok        = UTState.PASS.value  # test (expected) result is ok
Nok       = UTState.FAIL.value  # test (expected) result is not ok
uRArrow   = '\u2192'            # right arrow
uIdTo     = '\u2261'            # identical to (3 horizontal bars)
uNidTo    = '\u2262'            # not identical to (3 horizontal bars and slash)
uEq       = '\u003d'            # equal to
uNeq      = '\u2260'            # not equal to
uApprox   = '\u2245'            # approximately equal to
uTrue     = '\u22a8'            # is true
uNtrue    = '\u22ad'            # is not true
uColonEq  = '\u2254'            # colon equals

# -----------------------------------------------------------------------------
# Class UTDataset
# -----------------------------------------------------------------------------
class UTDataset:
  """
  Unit test dataset class.

  A dataset is a collection of test data (list). Each unit test iterates
  over at least one dataset and generate test results.

  An iterable over data.
  """
  def __init__(self, name, data=[]):
    """
    Initializer.

    Parameters:
      name    Dataset name.
      data    Dataset data.
    """
    self.name = str(name)
    self.data = data

  @classmethod
  def from_value(klass, value):
    """
    UTDataset class instance factory method.

    Create UTDataset instance from value.

    Parameters:
      klass   (Derived) UTDataset class.
      value   Value object used to initialize.

    Returns:
      UTDataset instance.
    """
    try:    # is (derived) UTDataset instance
      return klass(value.name, value.data)
    except AttributeError:
      pass

    try:    # is dictionary like object
      return klass(value['name'], value.get('data', [])) 
    except (KeyError, AttributeError, TypeError):
      pass

    try:    # is iterable or indexed object
      return klass(value[0], indexget(value, 1, []))
    except (IndexError, TypeError, KeyError):
      pass

    raise TypeError(f"{value} is not a {klass.__name__} convertible object")

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.name!r}, {self.data!r})"

  def __str__(self):
    return f"ds.{self.name}"

  def __len__(self):
    """ Number of data points in dataset. """
    return len(self.data)

  def __iter__(self):
    """ Iterator over dataset. """
    return self.data.__iter__()

  def __getitem__(self, i):
    """ __getitem__(i)  <==> data[i]. """
    return self.data[i]

  def __setitem__(self, i, datum):
    """ __setitem__(i, datum)  <==> data[i] = datum. """
    self.data[i] = datum

  def __contains__(self, datum):
    """ Return the outcome of the test 'datum in dataset'. """
    try:
      self.index(datum)
      return True
    except (ValueError):
      return False

  def __add__(self, rhs):
    """
    Concatenate. Return self + rhs.

    Parameters:
      rhs   A UTDataset convertible value.
    """
    ds2 = self.from_value(rhs)
    return UTDataset(f"{self.name}+{ds2.name}", self.data+ds2.data)

  def __iadd__(self, rhs):
    """ In-place concatenation. self += rhs.

    Parameters:
      rhs   A UTDataset convertible value.
    """
    ds2 = self.from_value(rhs)
    self.data += ds2.data
    return self

  def copy(self):
    """ self.copy() --> dataset -- shallow copy of self. """
    return UTDataset(self.name, self.data.copy())

  def append(self, datum):
    """ Append datum object to end of dataset. """
    self.data.append(datum)

  def index(self, datum, *args):
    """
    index(datum, [start, [stop]])
    
    Find first instance of datum in dataset ds.

    Parameters:
      datum   Value to search on dataset.
      start   Starting search position. Default: 0 (start of data)
      stop    Stopping search position. Default len(data) (end of data + 1)

    Returns:
      Integer index of first tag found.
      Raises ValueError if the tag is not present.
    """
    return self.data.index(datum, *args)

  def pair(self, pair2):
    """
    Create a dataset of length MxN by pairing the data from self with ds,
    where the length M and N are for self and ds, respectively.

    Given two datasets D (self) and E (ds2), then the resulting dataset
    data are (self[i], ds[j]), i=0...M-1, j=0...N-1:
    
    Parameters:
      p2    The second dataset. For each datum in self, p2 data will form
            the columns. A UTDataset convertible value.

    Returns:
      Dataset with pairs of data.
    """
    ds2 = self.from_value(pair2)
    pairs = []
    for d in self:
      for e in ds2:
        pairs.append((d, e))
    return UTDataset(f"({self.name}, {ds2.name})", pairs)

# -----------------------------------------------------------------------------
# Class UTDsDb
# -----------------------------------------------------------------------------
class UTDsDb:
  """
  Datasets database class.

  An iterable over datasets.
  """
  def __init__(self, name, ds=[]):
    self.name = str(name)
    self.db   = {}
    for d in ds:
      v = UTDataset.from_value(d)
      if v.name not in self.db:
        self.db[v.name] = v
      else:
        raise KeyError(f"{df.name} duplicate key in database")

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.name!r}, {self.db!r})"

  def __str__(self):
    return f"dsdb.{self.name}"

  def __len__(self):
    """ Number of db datasets. """
    return len(self.db)

  def __iter__(self):
    """ Iterator over db. """
    return self.db.__iter__()

  def __getitem__(self, k):
    """ __getitem__(k)  <==> db[k]. """
    return self.db[k]

  def __setitem__(self, k, v):
    """ __setitem__(k, v)  <==> db[k] = v. """
    self.db[k] = UTDataset.from_value(v)

  def __contains__(self, k):
    """ True if db has key k, else False. """
    return k in self.db

  def __delitem__(self, k):
    """ Delete db[k]. """
    del self.db[k]

  def items(self):
    """ Return key,datasets iterator. """
    return self.db.items()

  def keys(self):
    """ Return key iterator. """
    return self.db.keys()

  def datasets(self):
    """ Return datasets iterator. """
    return self.db.values()

# -----------------------------------------------------------------------------
# Class UT
# -----------------------------------------------------------------------------
class UT:
  """
  Unit test (base) class.

  A unit test validates a specific component of a subsystem of the SUT.

  A unit test operates at the granularity of one or more datasets.

  Test Cycle (driven by sequencer):
    sequencer:  prep()
    sequencer:  for datum in ut
    sequencer:    begin()
                    what, expect()
    sequencer:    test()
                    do_the_test
                    result, details
    sequencer:    end()
    sequencer:  finalize()

  An iterable over tests.
  """

  def __init__(self, name, dskey, *args, **kwargs):
    """
    Initializer.

    Parameters:
      name    Name of unit test.
      dskey   Primary db dataset key.
      args    Test additional arguments beyond the standard arguments.
      kwargs  Test additional keyword arguments beyond the standard arguments.
    """
    self.name   = str(name)
    self.dskey  = dskey
    self.args   = args
    self.kwargs = kwargs

    self.ds     = None        # primary dataset
    self.stats  = UTStats()   # statistics

  def reset(self):
    """ Reset unit test state. """
    self.ds = None
    self.stats.reset()

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.name!r}, {self.dskey!r}, {self.args} {self.kwargs})"

  def __str__(self):
    return f"ut.{self.name}"

  def __iter__(self):
    return self.ds.__iter__()

  def prep(self, sequencer):
    """
    Prepare unit test to iterate over test data.

    Parameters:
      sequencer   Tests sequencer.
    """
    self.reset()
    try:
      self.ds = sequencer.dsdb[self.dskey] # always regrab since data can change
    except KeyError:
      raise KeyError(
        f"{self.dskey!r} not in sequencer database - spelling? forget to add?")


  def begin(self, sequencer, datum):
    """
    Begin test preparations on the specific test datum.

    Parameters:
      sequencer   Tests sequencer.
      datum       Unit of test data. Does not have to be a simple
                  data type.

    Returns:
      Returns a 2-tuple (what, expect) where:
        what      String of what is to be tested.
        exepct    Expected pass/fail result of the test.
    """
    return (str(datum), self.expect(self.datum))

  def test(self, sequencer, datum):
    """
    Execute test on the specific test datum.

    Parameters:
      sequencer   Tests sequencer.
      datum       Unit of test data. Does not have to be a simple
                  data type.

    Returns:
      Returns 3-tuple (result, answer, details) where:
        result    The pass/fail/warning result of test.
        answer    String providing answer to test
                  (e.g '= 5', 'is large', 'error: not a string').
        details   String providing any additional details of the
                  test outcome including warnings.
    """
    return (UTState.FAIL, "UT base class has no test to run", '')

  def end(self, sequencer):
    """
    End of the test on the specific test datum.

    Internal data state changes and cleanup performed here.

    Parameters:
      sequencer   Tests sequencer.
    """
    pass

  def finalize(self, sequencer):
    """
    Finalize unit test after complete iteration over test data.

    Parameters:
      sequencer   Tests sequencer.
    """
    pass

  def expect(self, datum):
    """
    Determine expected result when executing test on the test datum.

    Parameters:
      datum   Unit of test data. Does not have to be a simple data type.

    Returns:
      Returns pass/fail exepect result.
    """
    return UTState.PASS

# -----------------------------------------------------------------------------
# Class UTDsAux
# -----------------------------------------------------------------------------
class UTDsAux:
  """
  Unit test dataset auxiliary helper class.

  This class provides a round-robin access to seconary datasets during
  unit testing. It is usefull for binary+ testing (e.g. addition). 
  """
  def __init__(self, dskey):
    """
    Initliazer.

    Parameters:
      dskey   Secondary db dataset key.
    """
    self.dskey  = dskey

    self.ds     = None  # the dataset
    self.count  = 0     # number of items in dataset
    self.i      = 0     # current index into the data of the dataset

  def reset(self):
    """ Reset. """
    self.ds     = None
    self.count  = 0
    self.i      = 0

  def prep(self, sequencer):
    """
    Prepare the secondary dataset information. 

    Parameters:
      sequencer   Tests sequencer.
    """
    self.ds     = sequencer.dsdb[self.dskey]
    self.count  = len(self.ds) 
    self.i      = 0

  def datum(self):
    """ Return datum at current index. """
    return self.ds[self.i]

  def __iadd__(self, j):
    """ In-place addition. self.i += j modulo count. """
    self.bump(j)
    return self

  def bump(self, j):
    """
    Bump index by j modulo count.

    Parameters:
      j   Size of bump.

    Returns:
      New index.
    """
    self.i = (self.i + j) % self.count
    return self.i

# -----------------------------------------------------------------------------
# Class UTSubsys
# -----------------------------------------------------------------------------
class UTSubsys:
  """
  Unit test subsystem class.

  It is at the subystem unit test level that a published interface to
  the command-line is provided.

  A SSUT is user-defined. It can be a class, method, function,
  etc. A series of unit test are executed over this user-defined
  subsystem.

  An iterable over unit test.
  """
  def __init__(self, name, desc, unittests=[], prereqs=[]):
    """
    Initializer.

    Parameters:
      name        Subsystem name. Exposed to command-line interface.
      desc        Short one-line description. Exposed to command-line interface.
      unittests   List of unit tests.
      prereqs     List of subsystem test to run prior to this subsystem.
    """
    self.name     = name
    self.desc     = desc
    self.ut       = unittests
    self.prereqs  = prereqs

    self.stats  = UTStats()

  @classmethod
  def from_value(klass, value):
    """
    UTSubsys class instance factory method.

    Create UTSubsys instance from value.

    Parameters:
      value   Value object used to initialize.

    Returns:
      UTSubsys instance.
    """
    try:    # is (derived) UTSubsys instance
      return klass(value.name, value.desc, unittests=value.ut,
          prereqs=value.prereqs)
    except AttributeError:
      pass

    try:    # is dictionary like object
      return klass(value['name'], value['desc'],
                  value.get('unittests', []), 
                  value.get('prereqs', [])) 
    except (KeyError, TypeError):
      pass

    try:    # is iterable or indexed object
      return klass(value[0], value[1],
                    indexget(value, 2, []),
                    indexget(value, 3, []))
    except (IndexError, TypeError, KeyError):
      pass

    raise TypeError(f"{value} is not a {klass.__name__} convertible object")

  def reset(self):
    """ Reset subssytem unit tests status. """
    self.stats.reset()

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.name!r}, {self.desc!r}, {self.ut!r})"

  def __str__(self):
    return f"ssut.{self.name}"

  def __len__(self):
    """ Number of unit tests ut. """
    return len(self.ut)

  def __iter__(self):
    """ Iterator over unit tests ut. """
    return self.ut.__iter__()

  def __getitem__(self, i):
    """ __getitem__(i)  <==> ut[i]. """
    return self.ut[i]

  def __setitem__(self, i, v):
    """ __getitem__(i)  <==> ut[i]. """
    ut = UTSubsys.from_value(v)
    self.ut[i] = ut

# -----------------------------------------------------------------------------
# Class UTSuite
# -----------------------------------------------------------------------------
class UTSuite:
  """
  Unit test suite class.

  The suite contains all tests for all subsystems for a given SUT.

  An iterable over subsytems.
  """
  def __init__(self, name, subsystems=[]):
    """
    Initializer.

    Parameters:
      name        Name of test suite.
      subsystems  List of subsystem tests convertible values.
    """
    self.name  = str(name)
    self.ssut = {}    # dictionary of subsystem tests.
    for v in subsystems:
      ss = UTSubsys.from_value(v)
      self.ssut[ss.name] = ss

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.name!r}, {self.ssut!r})"

  def __str__(self):
    return f"suite.{self.name}"

  def __len__(self):
    """ Number of subsystems. """
    return len(self.ssut)

  def __iter__(self):
    """ Iterator over subsystems. """
    return self.ssut.__iter__()

  def __getitem__(self, k):
    """ __getitem__(k)  <==> ssut[k]. """
    return self.ssut[k]

  def __setitem__(self, k, v):
    """ __setitem__(k, v)  <==> ssut[k] = v. """
    self.db[k] = UTSubsys.from_value(v)

  def __contains__(self, k):
    """ True if ssut has key k, else False. """
    return k in self.ssut

  def __delitem(self, k):
    """ Delete ssut[k]. """
    del self.ssut[k]

  def items(self):
    """ Return a key,subsystem iterator. """
    return self.ssut.items()

  def keys(self):
    """ Return a key iterator. """
    return self.ssut.keys()

  def ssut(self):
    """ Return a subsytems iterator. """
    return self.ssut.values()

# -----------------------------------------------------------------------------
# Class UTSequencer
# -----------------------------------------------------------------------------
class UTSequencer:
  """
  Unit test sequencer.

  Top-level execution control over the suite of tests.

  This class provides the execution environment for test sequencing, data
  error catching, out output formatting.
  """
  def __init__(self, name, suite, dsdb, **kwargs):
    """
    Initializer.

    Parameters:
      name    System under test (sut) name.
      suite   Unit test suite.
      dsdb    Database of test datasets.
      kwargs  Optional keyword sequencer and user configuration.
    """
    self.name   = str(name)
    self.suite  = suite
    self.dsdb   = dsdb

    self.color    = Colorize()      # bind to a terminal colorizer
    self.stats    = UTStats()       # total SUT statistics
    self.columns  = termsize()[1]   # default output columns
    self.nocolor  = False           # use color
    self.user     = {}              # user configuration

    self.config(**kwargs)
    self.reset()

  def config(self, **kwargs):
    """
    Configure sequencer and user-specific data from keyword values.

    Parameters:
      kwargs  Optional keyword configuration.
    """
    for k, v in kwargs.items():
      if k == 'columns':
        if v is None or v == 0:
          self.columns  = termsize()[1]   # default output columns
        else:
          self.columns = v
      elif k == 'nocolor':
        self.coloring = not v
      else:
        self.user[k] = v

  def reset(self):
    """ Reset sequencer state. """
    self.ssran    = []    # empty list of subsystem tests successfully ran
    self.ssut     = None  # no subsystem under test
    self.ut       = None  # no unit test in progress
    self.utwhat   = ''    # no unit test what information
    self.utexpect = UTState.PASS  # unit test expectation is whatever
    self.stats.reset()    # zero total stats

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.name!r}, {self.suite!r}, {self.dsdb!r})"

  def __str__(self):
    return f"seq.{self.name}"

  def __getitem__(self, k):
    """ __getitem__(k)  <==> config[k]. """
    return self.user[k]

  def __setitem__(self, k, v):
    """ __setitem__(k, v)  <==> nfig[k] = v. """
    self.user[k] = v

  def run(self, testnames=[]):
    """
    Run all specified subsystem tests.

    Parameters:
      testnames   Names of subsystems to test.
    """
    self.reset()
    self.print_top_hdr(testnames)

    # test all specified subsytems
    for ssname in testnames:
      self.ssut = self.suite[ssname]
      self.ut   = None
      self.ssut.reset()
      self.print_ssut_hdr()

      # check subsys tests prereqs
      try:
        self.check_prereqs(self.ssut)
      except Exception as e:
        self.fatalexit(-1, 'in check_prereqs()', e)

      # test all unit tests in a subsystem
      for self.ut in self.ssut:
        utname = self.ut.__class__.__name__

        # reset unit test to initial state
        try:
          self.ut.reset()
        except Exception as e:
          self.fatalexit(-1, 'in {utname}.reset()', e)

        self.print_ut_hdr()

        # prepare unit test for testing
        try:
          self.ut.prep(self)
        except Exception as e:
          self.fatalexit(-1, 'in {utname}.prep()', e)

        # unit test number
        tnum = 0

        # test all data in unit test 
        for datum in self.ut:
          # begin this unit test on this datum
          try:
            what, expect = self.ut.begin(self, datum)
          except Exception as e:
            self.fatalexit(tnum, 'in {utname}.begin()', e)

          self.mark_test_begin(what, expect)
          self.ut.stats.bump_expected(expect)

          # test
          try:
            result, answer = self.ut.test(self, datum)
          except Exception as e:
            self.fatalexit(tnum, 'in {utname}.test()', e)

          self.mark_tested(result, answer)
          self.ut.stats.bump_result(result)

          # end this unit test on datum
          try:
            self.ut.end(self)
          except Exception as e:
            self.fatalexit(tnum, 'in {utname}.end()', e)

          tnum += 1

        # finalize unit test
        try:
          self.ut.finalize(self)
        except Exception as e:
          self.fatalexit(-1, 'in {utname}.finalize()', e)
        
        self.ssut.stats += self.ut.stats
        self.ssran.append(self.ssut.name)

        self.print_stats(self.ut.name, self.ut.stats)
        print('')

      self.ut = None

      self.stats += self.ssut.stats
      self.print_stats(self.ssut.name, self.ssut.stats)

    self.ssut = None

    print('')
    self.print_stats(self.name, self.stats)

  def get_avail_tests(self):
    """
    Get available subsystem unit tests.

    Returns:
      Dictionary {testname:description, ...}
    """
    d = {}
    for k,ss in self.suite.items():
      d[k] = ss.desc
    return d

  def get_subsys_under_test(self):
    """ Return current subsystem under test. None if no subsystem. """
    return self.ssut

  def get_unit_under_test(self):
    """ Return current unit test. None if no test. """
    return self.ut

  def check_prereqs(self, ssut):
    """
    Check prerequisits for the subsystem testing.

    Parameters:
      ssut    Subsystem unit test.
    """
    for prereq in ssut.prereqs:
      if prereq not in self.ssran:
        raise RuntimeError(f"prerequisite {prereq!r} for {ssut.name!r} not met")

  def mark_test_begin(self, what, expect):
    """
    Mark the beginning of a single unit test.

    Parameters:
      what    What is being tested.
      expect  The expected pass/fail results of the test.
    """
    self.utwhat   = f"{what}"
    self.utexpect = expect

    state = UTState.WAIT
    pre   = f"[{state.name}] "              # notice the trailing space
    post  = f" Expect [{expect.name}]"      # notice the leading space

    w = self.columns - len(pre) - len(post)
    if w < 0:
      w = 0

    #RDK s = self.utwhat[:w]
    s,n = unicode_encoder.pslice(self.utwhat, stop=w)

    #RDK sp = self.columns - len(pre) - len(s) - len(post)
    sp = self.columns - len(pre) - n - len(post)
    if sp < 0:
      sp = 0

    print(f"[{self.color.utstate(state)}] {s}{'':<{sp}}{post}", end='')

  def mark_tested(self, result, lines):
    """
    Mark the end of a single unit test.

    Parameters:
      result    Result of the test.
      lines     List of lines providing answers and details of the test
                results.
    """
    pre   = f"[{result.name}] "                 # notice the trailing space
    post  = f" Expect [{self.utexpect.name}]"   # notice the leading space

    # first line is sandwiched between the prefix and postfix strings
    if type(lines) == str:
      line = lines
    elif len(lines) > 0:
      line = lines[0]
    else:
      line = ''
    w = self.columns - len(pre) - len(post)
    if w < 0:
      w = 0
    s = self.utwhat + ' ' + line
    #RDK s = s[:w]
    s,n = unicode_encoder.pslice(s, stop=w)
    #RDK sp = self.columns - len(pre) - len(s) - len(post)
    sp = self.columns - len(pre) - n - len(post)
    if sp < 0:
      sp = 0
    print(f"\r[{self.color.utstate(result)}] {s}{'':<{sp}}{post}")

    if type(lines) == str:
      return

    # subsequent lines printed indented
    sp = len(pre)
    w = self.columns - sp
    if w < 0:
      w = 0
    for line in lines[1:]:
      #RDK s = line[:w]
      s,n = unicode_encoder.pslice(line, stop=w)
      print(f"{'':<{sp}}{s}")

  def print_top_hdr(self, testnames):
    """
    Print top SUT header.

    Paramters:
      testnames   Subsystems to test.
    """
    testpath = self.breadcrumbs()
    tlist = ' '.join(testnames)
    suttests = f"UT.{self.name} test to run"
    print()
    print(f"{self.color(suttests, 'green')}: {tlist}")
    print()
    print(f"  {self.color(testpath, 'lightblue')}")

  def print_ssut_hdr(self):
    """ Print SSUT subheader. """
    testpath = self.breadcrumbs()
    print('')
    print(f"  {self.color(testpath, 'lightblue')}")

  def print_ut_hdr(self):
    """ Print UT subheader. """
    testpath = self.breadcrumbs()
    print(f"  {self.color(testpath, 'lightblue')}")

  def print_stats(self, name, stats):
    if len(name) <= 16:
      n = f"{name[:16]:<16}"
    else:
      n = name[:13] + '...'
      n = f"{n:<16}"
    print(f"  {self.color(n, 'darkgray')}"
          f"{self.color(str(stats), 'darkgray')}")

  def fatalexit(self, tnum, doing, e):
    """
    Print fatal message and exit.

    Paramters:
      tnum    Test number that caused fatal exception. -1 if no test.
      doing   While doing something in the unit test cycle.
      e       Unhandled exception. 
    """
    testpath = self.breadcrumbs()
    state = UTState.FATAL
    pre   = f"[{state.name}] "
    sp    = len(pre)
    print(f"\n[{self.color.utstate(state)}] Unhandled exception: "\
          f"{e.__class__.__name__}")
    print(f"{'':<{sp}}{e}")
    if tnum >= 0:
      print(f"{'':<{sp}}{testpath} {doing} test {tnum}")
    else:
      print(f"{'':<{sp}}{testpath} {doing}")
    sys.exit(8)

  def breadcrumbs(self):
    """ Return unit testing path. """
    crumbs = f"UT.{self.name}"
    if self.ssut:
      crumbs += f".{self.ssut.name}"
      if self.ut:
        crumbs += f".{self.ut.name}"
    return crumbs

  @property
  def columns(self):
    """ Return the current output column width. """
    return self._columns

  @columns.setter
  def columns(self, cols):
    """
    Set the number of output columns.

    Parameters:
      cols    Integer >= 24.
    """
    if cols >= 24:
      self._columns = cols
    else:
      self._columns = 24

  @property
  def coloring(self):
    """ Return True/False if coloring is enabled. """
    return self._coloring

  @coloring.setter
  def coloring(self, enable):
    """
    Enable/disable color output.

    Parameters:
      enable  True/False.
    """
    if not self.color.using_color() and enable:
      self.color.enable()
    elif self.color.using_color() and not enable:
      self.color.disable()
    self._coloring = self.color.using_color()

# -----------------------------------------------------------------------------
# Class UTCli
# -----------------------------------------------------------------------------
class UTCli:
  """
  Unit test command-line interface class.

  This class provides a simple parse of command-line arguments and
  options. The output may be fed into a unit test sequencer.
  """
  OptsHelp    = ['-h', '--help']
  OptsNoColor = ['--nocolor']
  OptsColumns = ['--columns']
  OptionDesc  = [
    (OptsHelp,    "",     "Print help and exit."),
    (OptsNoColor, "",     "Disable color output."),
    (OptsColumns, "COLS", "Set output column width. Default: terminal size."),
  ]

  def __init__(self, synopsis):
    """
    Initializer.

    Parameters:
      synopsis    Short synopsis of testing.
    """
    self.argv0        = os.path.basename(sys.argv[0])
    self.argv         = sys.argv[1:]
    self.synopsis     = str(synopsis)
    self.avail_tests  = { }

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(self.synopsis)"

  def __str__(self):
    return "UT Command-Line Interface"

  def set_avail_tests(self, testnames):
    """
    Set available tests.

    Parameters:
      testnames   - List of available test names.
    """
    self.avail_tests = testnames.copy()

  def parse(self, default_test=None):
    """
    Parse command-line options and arguments.

    Parameters:
      default_test  Default test if none specified. If no default test
                    and no tests are specified, then all tests are ran.
                    The special 'all' test overrides the default.

    Returns:
      A 2-tuple of (options, testnames) where:
        options is a dictionary of keywords, values.
        testnames is a list of subsystem test names.
    """
    alltests  = list(self.avail_tests.keys())
    options   = {}
    testnames = []

    i = 0
    while i < len(self.argv):
      arg = self.argv[i]
      i += 1
      if arg in UTCli.OptsHelp:
        self.help(default_test)
        sys.exit(0)
      elif arg in UTCli.OptsNoColor:
        options[arg[2:]] = True
      elif arg in UTCli.OptsColumns:
        try:
          optarg = self.argv[i]
          i += 1
        except IndexError:
          self.usage(f"{arg!r}: missing option argument")
          sys.exit(2)
        try:
          options[arg[2:]] = int(optarg)
        except ValueError:
          self.usage(f"{optarg!r}: not an integer")
          sys.exit(2)
      elif arg in ['--']:
        pass
      elif arg in alltests:
        testnames += [arg]
      elif arg == 'all':
        testnames = alltests
        break
      else:
        self.usage(f"{arg!r}: unknown test.")
        sys.exit(2)

    # default is either default or all tests
    if len(testnames) == 0:
      if default_test:
        if default_test in alltests:
          testnames = [default_test]
        else:
          self.usage(f"{default_test!r}: unknown default test.")
          sys.exit(2)
      else:
        testnames = alltests

    return options, testnames

  def usage(self, emsg=None):
    """
    Print usage statements.

    Parameters:
      emsg    Error message.
    """
    if emsg:
      print(f"{self.argv0}: error: {emsg}")
      print(f"Try 'python3 {self.argv0} --help' for more information.")
    else:
      print(f"""\
Usage: python3 {self.argv0} [OPTIONS] [TEST [TEST...]]
       python3 --help""")

  def help(self, default_test):
    """ Print help statements. """
    self.usage()
    print('')
    print(f"{self.synopsis}")

    print("\nOPTIONS:")
    for opt, optarg, desc in UTCli.OptionDesc: #UTCli.OptionDesc.items():
      fopt = ', '.join([o for o in opt])
      if optarg:
        fopt += f" {optarg}"
      sp = 20 - len(fopt)
      if sp <= 0:
        sp = 1
      print(f"  {fopt}{'':<{sp}}{desc}")

    print("\nTESTS:")
    maxlen = 4
    for tst in self.avail_tests.keys():
      n = len(tst)
      if n > maxlen:
        maxlen = n
    maxlen += 2

    for tst,desc in self.avail_tests.items():
      sp = maxlen - len(tst)
      if sp <= 0:
        sp = 1
      print(f"  {tst}{'':<{sp}}{desc}")

    sp = maxlen - len('all')
    print()
    print(f"  all{'':<{sp}}Run all tests.")

    print()
    if default_test:
      print(f"  DEFAULT: {default_test}")
    else:
      print(f"  DEFAULT: all")


# -----------------------------------------------------------------------------
# Class UTCliArgParse
# -----------------------------------------------------------------------------
class UTCliArgParse:
  """
  Unit test command-line interface class.

  This class provides a python argparse version of command-line arguments
  and options parsing. The output may be fed into a unit test sequencer.
  """

  def __init__(self, synopsis):
    """
    Initializer.

    Parameters:
      synopsis    Short synopsis of testing.
    """
    self.argv0        = os.path.basename(sys.argv[0])
    self.argv         = sys.argv[1:]
    self.synopsis     = str(synopsis)
    self.avail_tests  = { }

    self.parser = argparse.ArgumentParser(
        formatter_class=SmartFormatter,
        description=self.synopsis)
    self.parser.add_argument('--nocolor',
        action='store_true',
        help="Disable color output."),
    self.parser.add_argument('--columns',
        type=int,
        required=False,
        help="Set output column width. Default: terminal size.")
    self.parser.add_argument('testnames',
        metavar='TEST',
        type=str,
        nargs='*',
        help="Name of unit test to run (See tests section below).")

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"(self.synopsis)"

  def __str__(self):
    return "UT Command-Line Interface"

  def set_avail_tests(self, testnames):
    """
    Set available tests.

    Parameters:
      testnames   - List of available test names.
    """
    self.avail_tests = testnames.copy()

  def parse(self, default_test=None):
    """
    Parse command-line options and arguments.

    Parameters:
      default_test  Default test if none specified. If no default test
                    and no tests are specified, then all tests are ran.
                    The special 'all' test overrides the default.

    Returns:
      A 2-tuple of (options, testnames) where:
        options is a dictionary of keywords, values.
        testnames is a list of subsystem test names.
    """
    alltests  = list(self.avail_tests.keys())

    self.parser.epilog = self.help_epilog(default_test)

    args = self.parser.parse_args(self.argv)

    kwdict = vars(args)

    #print(f"args={kwdict}")

    # pop test names, leaving options
    testnames = kwdict.pop('testnames')

    if 'all' in testnames:
      testnames = alltests
    elif not set(testnames).issubset(alltests):
      badtests = set(testnames).difference(alltests)
      self.parser.error(f"{list(badtests)!r}: unknown test(s).")
      sys.exit(2)

    # default is either default or all tests
    if len(testnames) == 0:
      if default_test:
        if default_test in alltests:
          testnames = [default_test]
        else:
          self.usage(f"{default_test!r}: unknown default test.")
          sys.exit(2)
      else:
        testnames = alltests

    #print(kwdict)
    #print(testnames)

    return kwdict, testnames

  def help_epilog(self, default_test):
    """
    Build help epilog string of tests and defaults.

    Parameters:
      default_test  Default test.

    Return:
      Epilog string
    """
    # find maximum test name length
    maxlen = 4
    for tst in self.avail_tests.keys():
      n = len(tst)
      if n > maxlen:
        maxlen = n
    maxlen += 2

    with io.StringIO() as output:
      print("\ntests:", file=output)
      for tst,desc in self.avail_tests.items():
        sp = maxlen - len(tst)
        if sp <= 0:
          sp = 1
        print(f"  {tst}{'':<{sp}}{desc}", file=output)

      sp = maxlen - len('all')
      print('', file=output)
      print(f"  all{'':<{sp}}Run all tests.", file=output)

      print('', file=output)
      if default_test:
        print(f"  DEFAULT: {default_test}", file=output)
      else:
        print(f"  DEFAULT: all", file=output)

      epilog = output.getvalue()

    return epilog


# -----------------------------------------------------------------------------
# Unit test main template.
# -----------------------------------------------------------------------------
def UTMainTemplate(sequencer, synopsis, default_test=None):
  """
  A unit test main that can be used in a unit test script. Not required.

  Parameters:
    sequencer     Unit test sequencer.
    synopsis      SUT synopsis string.
    default_test  Default test.

  Returns:
    Zero on success, failure otherwise.
  """
  #cli = UTCli(synopsis)
  cli = UTCliArgParse(synopsis)

  cli.set_avail_tests(sequencer.get_avail_tests())

  options, testnames = cli.parse(default_test=default_test)

  sequencer.config(**options)

  sequencer.run(testnames)

  return 0

# -----------------------------------------------------------------------------
# Boilerplate unit test datasets and functions.
# -----------------------------------------------------------------------------
dsBoilNull  = UTDataset('ds_boil_null')               # null dataset (no test)
dsBoilOne   = UTDataset('ds_boil_one', data=['push']) # push one test cycle

# call(tobj) : built-ins on sut numeric test object
dsBoilBuiltinsNum = UTDataset('ds_boil_builtins_num',
    data = [abs, bin, complex, float, hex, int, oct, round,])

# call(tobj, value) : built-ins on sut numeric test object with value
dsBoilBuiltinsNum2 = UTDataset('ds_boil_builtins_num2',
    data = [divmod, pow, round,])

# call(tobj) : built-ins on sut character test object
dsBoilBuiltinsChar  = UTDataset('ds_boil_builtins_char', data = [chr, ord])

# call(tobj) : built-ins on sut iterable test object
dsBoilBuiltinsIter  = UTDataset('ds_boil_builtins_iter',
    data = [all, enumerate, max, min, sum, tuple, zip,])

# call(tobj) : built-ins on sut test object
dsBoilBuiltins  = UTDataset('ds_boil_builtins',
    data = [ascii, bool, callable, id, len, repr, str, type,])

# call(tobj, value) : built-ins on sut test object with value
dsBoilBuiltins2  = UTDataset('ds_boil_builtins2',
    data = [delattr, format, getattr, hasattr, max, min,])

# call(tobj, value1, value2) : built-ins on sut test object with two values
dsBoilBuiltins3  = UTDataset('ds_boil_builtins3', data = [setattr,])

class utBoilBuiltins(UT):
  """
  Boilerplate unit test python built-ins on sut test objects.

  For each test object apply the built functions.
  """
  def __init__(self, name, dskey_builtins, dskey_tobjs):
    """
    Initializer.

    Parameters:
      name            Name of unit test.
      dskey_builtins  Key to dataset of a list of built-in calls
                      that require only the test object as an argument.
      dskey_tobjs     Key to dataset containing a list of test objects.
    """
    UT.__init__(self, f"call({name})", dskey_builtins, dskey_tobjs)
    self.dskey_tobjs = self.args[0] # base class saves this key in args list

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.dstobjs = sequencer.dsdb[self.dskey_tobjs]
    self.dssave = copy(self.ds)
    self.ds = copy(self.ds.pair(self.dstobjs)) # iterate on MxN dataset pair

  def begin(self, sequencer, datum):
    self.func     = datum[0]
    self.funcname = self.func.__name__
    self.tobj     = datum[1]
    return (f"{self.funcname}({self.tobj})", UTState.PASS)

  def test(self, sequencer, datum):
    output = self.func(self.tobj)
    return UTState.PASS, f"= {output}"

  def finalize(self, sequencer):
    self.ds = copy(self.dssave)

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utut as ut

  sys.exit(ut.utmain())

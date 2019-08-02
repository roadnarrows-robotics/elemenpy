"""
Test whatever - not met to be part of package per se.

Package:
  RoadNarrows elemenpy python package.

File:
  testwhat.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

from __future__ import print_function

import sys
import os
import math
import inspect
import copy
import argparse
import textwrap

# -----------------------------------------------------------------------------
# Class NewOverridden
# -----------------------------------------------------------------------------
class NewOverridden:
  """ Test overriding __new__, but behave identical to python3 construction. """
  def __new__(klass, *args, **kwargs):
    """
    Constructor.

    Parameters:
      args    Arguments passed to __init__()
      kwargs  Keyword arguments passed to __init__()

    Returns:
      NewOverridden instance.
    """
    print("Creating NewOverridden Instance")
    instance = super(NewOverridden, klass).__new__(klass)
    return instance

  def __init__(self, a, b):
    """
    Initializer.

    Parameters:
      a   Anything number.
      b   Anything number.
    """
    print("Initializing NewOverridden Instance")
    self.a = a
    self.b = b
    self.c = self.a * self.a + self.b * self.b

def testNewOverridden():
  print("  Test NewOverrriden")
  no1 = NewOverridden(3, 4)
  no2 = NewOverridden(math.sqrt(2), math.sqrt(2))

  print(f"NewOverridden       = {NewOverridden}")
  print(f"type(NewOverridden) = {type(NewOverridden)}")
  print(f"no1                 = {no1}")
  print(f"type(no1)           = {type(no1)}")
  print(f"no2                 = {no2}")
  print('')
  print(f"no1: {no1.a}^2 + {no1.b}^2 = {no1.c}")
  print(f"no2: {no2.a:.4}^2 + {no2.b:.4}^2 = {no2.c:.4}")
  print('')

# -----------------------------------------------------------------------------
# Class Singleton
# -----------------------------------------------------------------------------
class Singleton:
  """ Test limiting to single class instance. """
  _instance   = None
  _initiated  = False

  def __new__(klass, *args, **kwargs):
    """
    Constructor.

    Parameters:
      args    Arguments passed to __init__()
      kwargs  Keyword arguments passed to __init__()

    Returns:
      Singleton instance.
    """
    print(f"Creating Singleton Instance")
    if not Singleton._instance:
      Singleton._instance = super(Singleton, klass).__new__(klass)
    return Singleton._instance

  def __init__(self, apples='red', bananas='yellow'):
    """
    Initializer.

    Parameters:
      apples    Anything string.
      bananas   Anything string.
    """
    print(f"Initializing Singleton Instance {apples}, {bananas}")
    if not Singleton._initiated:
      self.apples   = apples
      self.bananas  = bananas
      Singleton._initiated = True

def testSingleton():
  print("  Test Singleton")
  sn1 = Singleton()
  sn2 = Singleton(apples='green')
  sn3 = Singleton(bananas='red', apples='green')

  print(f"Singleton       = {Singleton}")
  print(f"type(Singleton) = {type(Singleton)}")
  print(f"sn1             = {sn1}")
  print(f"type(sn2)       = {type(sn2)}")
  print(f"sn2             = {sn2}")
  print(f"type(sn3)       = {type(sn3)}")
  print(f"sn3             = {sn3}")
  print('')
  print(f"sn1: apples={sn1.apples!r}, bananas={sn1.bananas!r}")
  print(f"sn2: apples={sn2.apples!r}, bananas={sn2.bananas!r}")
  print(f"sn3: apples={sn3.apples!r}, bananas={sn3.bananas!r}")
  print('')

# -----------------------------------------------------------------------------
# Class EvenPrime
# -----------------------------------------------------------------------------
class EvenPrime():
  """ Test __new__ returning different type than EvenPrime. """
  def __new__(klass):
    """
    Constructor.

    Returns:
      EvenPrime instance.
    """
    print(f"Creating EvenPrime Instance")
    instance = super(EvenPrime, klass).__new__(klass)
    return 2

  def __init__(self):
    """
    Initializer.

    Will not be called during construction and not usefule valid if called
    explicitly.
    """
    print(f"Initializing EvenPrime Instance")

def testEvenPrime():
  print("  Test EvenPrime")
  ep1 = EvenPrime()
  ep2 = EvenPrime()

  print(f"EvenPrime       = {EvenPrime}")
  print(f"type(EvenPrime) = {type(EvenPrime)}")
  print(f"ep1             = {ep1}")
  print(f"type(ep1)       = {type(ep1)}")
  print(f"ep2             = {ep2}")
  print('')

  a = ep1 * 3 + ep2 * 4
  print(f"{ep1} * 3 + {ep2} * 4 = {a}")

  # not useful
  #ep2.__init__()
  #print(f"ep2             = {ep2}")
  #print(f"type(ep2)       = {type(ep2)}")

  print('')

# -----------------------------------------------------------------------------
# Class Constant
# -----------------------------------------------------------------------------
class Constant(float):
  """ Constant class. """
  def __new__(klass, *args, **kwargs):
    instance = super(Constant, klass).__new__(klass, args[0])
    return instance

  def __init__(self, value, name, **kwargs):
    """
    Initializer.

    Parameters:
      v   Constant value.
    """
    print(f"init({value}, {name})")
    float.__init__(value)
    self._v   = value
    self.name = name
    self.desc = kwargs.get('desc', 'no description')

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}({self.v})"

  #def __str__(self):
  #  return f"{self.v}"

  def __call__(self):
    return self

  def __del__(self):
    print(f"Deleting {self.name}")

  #def __add__(self, rhs):
  #  return self.v + rhs

  @property
  def v(self):
    return self._v

#cperm = Constant(12345, "stop", desc='mommy is mad')

def testConstant():
  print("  Test Constant")
  c1 = Constant(math.pi,  'pi', desc='a la mode')
  c2 = Constant(math.tau, 'tau')
  c3 = Constant(math.e,   'e')

  inher = [c.__name__ for c in inspect.getmro(Constant)]

  print(f"Constant       = {Constant}")
  print(f"type(Constant) = {type(Constant)}")
  print(f"inheritance    = {inher}")
  print(f"type(c1)       = {type(c1)}")
  print(f"type(c2)       = {type(c2)}")
  print(f"type(c3)       = {type(c3)}")
  print(f"c1             = {c1}")
  print(f"c2             = {c2}")
  print(f"c3             = {c3}")
  print(f"c1.desc        = {c1.desc!r}")
  print(f"c2.desc        = {c2.desc!r}")
  print(f"c3.desc        = {c3.desc!r}")

  print('')

  f = c1 + c2 + c3
  print(f"c1 + c2 + c3 = {f}")
  print(f"type(f)      = {type(f)}")

  # checks of op
  if not isinstance(c1, Constant):
    print(f"c1 mutated to {type(c1)}")
  if not isinstance(c2, Constant):
    print(f"c2 mutated to {type(c2)}")
  if not isinstance(c1, Constant):
    print(f"c3 mutated to {type(c3)}")

  f = c2 / c1
  print(f"c2 / c1 = {f}")
  print(f"type(f) = {type(f)}")

  if not isinstance(c2, Constant):
    print(f"c2 mutated to {type(c2)}")
  if not isinstance(c1, Constant):
    print(f"c1 mutated to {type(c1)}")

  f = c3 + 9.0
  print(f"c3 + 9.0 = {f}")
  print(f"type(f)  = {type(f)}")

  if not isinstance(c3, Constant):
    print(f"c3 mutated to {type(c3)}")

  try:
    c2.v = 4
  except AttributeError:
    print(f"{c2.name}: c2.v = 4  -> read-only")

  c2 += 50.0
  print(f"c2 += 50 = {c2}")

  if not isinstance(c2, Constant):
    print(f"c2 mutated to {type(c2)}")

  c3 = 5
  print(f"c3 = {c3}")

  if not isinstance(c3, Constant):
    print(f"c3 mutated to {type(c3)}")

  c4 = c1
  print(f"c4 = c1 -> {c4} {c4.name}")
  if not isinstance(c4, Constant):
    print(f"c4 mutated to {type(c4)}")

  c5 = cperm
  print(f"c5 = cperm -> {c5} {c5.name}")
  c5 = 8
  print(f"c5 = 8")
  print(f"type(c5) = {type(c5)}")

  #cperm = 'a'
  #print(f"type(cperm) = {type(cperm)}")

  print('')

# -----------------------------------------------------------------------------
# Foo 
# -----------------------------------------------------------------------------
class Foo:
  Vey = "robinhood"
  Ooh = 'oak'
  Lah = 'mighty'

  def __init__(self):
    self.i = 5
    self.d = {}

  def addpair(self, k, v):
    self.d[k] = v

class Bar(Foo):
  Vey = 109
  Nonsense = {'b': 'balderdash', 'r': 'rot'}

  foo = Foo()

  def __init__(self):
    Foo.__init__(self)
    self.j = -5

  @classmethod
  def newpair(klass, k, v):
    klass.foo.addpair(k, v)

  @classmethod
  def __contains__(klass, key):
    return key in klass.Nonsense

def testClassmethod():
  print("  Test Classmethod")
  print(f"i = {Bar.foo.i}")
  print(f"d = {Bar.foo.d}")

  Bar.newpair('cedar', 7)
  Bar.newpair('pine', 11)
  print(f"d = {Bar.foo.d}")

  print(f"Foo.Vey = {Foo.Vey}")
  print(f"Foo.Ooh = {Foo.Ooh}")
  print(f"Bar.Vey = {Bar.Vey}")

  print(f"Foo.__dict__ = {Foo.__dict__}")
  print(f"Bar.__dict__ = {Bar.__dict__}")

  setattr(Bar, 'Ooh', getattr(Foo, 'Ooh'))
  print(f"Bar.Ooh = {Bar.Ooh}")
  Bar.Ooh = 'aspen'
  print(f"Foo.Ooh = {Foo.Ooh}")
  print(f"Bar.Ooh = {Bar.Ooh}")
  print(f"Bar.Lah = {Bar.Lah}")

  if Bar.__contains__('r'):
    ninny = Bar.Nonsense['r']
    print(f"r = {ninny}")

  print('')

def testModuleLoad():
  print("Test loading module standardmodel")
  from elemenpy.sm.standardmodel import OnlyThis
  print(f"OnlyThis = {OnlyThis}")
  from elemenpy.core.format import (Unicoder)
  print(f"electron neutrino = {Unicoder.lookup('sm', 'nu_e')}")

  print("Test loading module quark")
  from elemenpy.sm.quark import Quark
  print(f"antiup quark = {Quark.quark_class('AntiUp').symbol()}")

class Tree:
  TreeTypes = {'d': 'deciduous', 'e':'evergreen'}

  def __init__(self, name, ttype, age=0):
    self.name = name
    self.ttype = ttype
    self.age = age

  def happybirthday(self):
    self.age += 1

  def printtree(self):
    print(f"  Name:      {self.name}")
    print(f"  Tree Type: {self.ttype}")
    print(f"  Age:       {self.age}")

  @property
  def classname(self):
    return self.__class__.__name__

  def copy(self):
    return copy.copy(self)

class Aspen(Tree):
  SummerColor = 'green'
  FallColor   = 'yellow'

  def __init__(self, age=0):
    Tree.__init__(self, 'aspen', Tree.TreeTypes['d'], age=age)
    self.currentcolor = Aspen.SummerColor

  def falltime(self):
    self.currentcolor = Aspen.FallColor

  def printtree(self):
    Tree.printtree(self)
    print(f"  Color:     {self.currentcolor}")

def testCopy():
  print("Test shallow copy")

  print("** Plant some trees **")
  t = Tree('unnamed', Tree.TreeTypes['e'])
  a = Aspen(4)
  print(t.classname, 't')
  t.printtree()
  print(a.classname, 'a')
  a.printtree()

  print("** Clone (copy) trees **")
  #u = copy.copy(t)
  #b = copy.copy(a)
  print('t.copy() -> u')
  u = t.copy()
  print('a.copy() -> b')
  b = a.copy()
  print(u.classname, 'u')
  u.printtree()
  print(b.classname, 'b')
  b.printtree()

  print("** GMO (modify) trees **")
  print('u.name = yew')
  u.name = 'yew'
  print('b.falltime()')
  b.falltime()
  print('a.happybirthday()')
  a.happybirthday()

  print(t.classname, 't')
  t.printtree()
  print(u.classname, 'u')
  u.printtree()
  print(a.classname, 'a')
  a.printtree()
  print(b.classname, 'b')
  b.printtree()

def testArgs():
  #print("Test parse args")

  argv0 = os.path.basename(sys.argv[0])
  
  parser = argparse.ArgumentParser(
#      usage=f"""\
#python3 {argv0} [OPTIONS] [TEST [TEST...]]
#       python3 {argv0} --help""",
      epilog="This is EPILOG",
      description="""\
This is my story.

This is my song.""")

  parser.add_argument('--debug',
      action='store_true',
      help="""Enable debugging.""")

  parser.add_argument('ssut', metavar='TEST',
      type=str,
      nargs='*',        # list of tests
      #choices=['this', 'that', 'all'],
      #default=['all'])
      help="Unit tests to run.\nheh hemek")

  parser.epilog = "now this is the new epilog"

  args = parser.parse_args(sys.argv[1:])

  kwdict = vars(args)

  print(f"args={kwdict}")


if __name__ == '__main__':
  #testNewOverridden()
  #testSingleton()
  #testEvenPrime()
  #testConstant()
  #testClassmethod()
  #testModuleLoad()
  #testCopy()
  testArgs()

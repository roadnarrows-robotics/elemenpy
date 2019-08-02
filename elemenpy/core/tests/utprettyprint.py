"""
Unit test the prettyprint module.

Package:
  RoadNarrows elemenpy python package.

File:
  utprettyprint.py

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

from elemenpy.testing.ut import *
import elemenpy.core.prettyprint as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

ds2Col = UTDataset('ds_2col',
  data = [[
    ("Ball lichen",             "Sphaerophorus"),
    ("Barnacle lichen",         "Thelotrema"),
    ("Beard lichen",            "Usnea"),
    ("Birchbark dot lichen",    "Leptorhaphis"),
    ("Blackcurly lichen",       "Pseudephebe"),
    ("Blackthread lichen",      "Placynthium"),
    ("Blemished lichen",        "Phlyctis"),
    ("Blistered navel lichen",  "Lasallia"),
    ("Blood lichen",            "Mycoblastus"),
    ("Bloodstain lichen",       "Haematomma"),
    ("Bowl lichen",             "Psoroma"),
    ("Bran lichen",             "Parmeliopsis"),
    ("Brittle lichen",          "Cornicularia"),
    ("Bullseye lichen",         "Placopsis"),
    ("Bruised lichen",          "Toninia"),
    ("Button lichen",           "Buellia"),
    ("Cap lichen",              "Baeomyces"),
    ("Cartilage lichen",        "Ramalina"),
    ("Chocolate chip lichen",   "Solorina"),
    ("Clam lichen",             "Normandina"),
    ("Club lichen",             "Multiclavula"),
    ("Cobblestone lichen",      "Acarospora"),
    ("Cockleshell lichen",      "Hypocenomyce"),
    ("Comma lichen",            "Arthonia"),
    ("Chalice lichen",          "Endocarpon"),
    ("Coral lichen",            "Sphaerophorus"),
    ("Crabseye lichen",         "Ochrolechia"),
    ("Cracked lichen",          "Acarospora"),
    ("Crater lichen",           "Diploschistes"),
    ("Cup lichen",              "Cladonia"),
  ]]
)

# the database of datasets
db = UTDsDb('db', ds=[ds2Col])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

class utPrint(UT):
  """ Unit test print2col and print_to_str. """
  def __init__(self, dskey):
    UT.__init__(self, "print2col()", dskey)

  def begin(self, sequencer, datum):
    return (f"Lichen Genus", UTState.PASS)

  def test(self, sequencer, datum):
    lines = sut.print_to_str(sut.print2cols, datum, indent=6)
    return (UTState.PASS, [f"two columns {uRArrow}"] + lines.split('\n'))

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('print', "Test print2cols and print_to_str functions.",
      unittests=[
        utPrint('ds_2col'),
      ]
    ),
  ],
)

utseq = UTSequencer('prettyprint', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test prettyprint module.")

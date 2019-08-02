"""
Unit test the format module.

Package:
  RoadNarrows elemenpy python package.

File:
  utformat.py

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
import random
from enum import Enum

from elemenpy.core.common import (enumfactory)
from elemenpy.testing.ut import *
import elemenpy.core.format as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

Maybe = UTState.WARN.value

dsHtmlTbls = UTDataset('ds_html_tbls', data=sut.html_encoder.tid_list())
dsLatexTbls = UTDataset('ds_latex_tbls', data=sut.latex_encoder.tid_list())
dsPlainTbls = UTDataset('ds_plain_tbls', data=sut.plain_encoder.tid_list())
dsUnicodeTbls = UTDataset('ds_unicode_tbls',data=sut.unicode_encoder.tid_list())

dsParser = UTDataset('ds_parser',
  data = [
    # good test cases
    ("My plain world.", Ok),
    ("I have \$2 to my name.", Ok),
    ("A$sup(123)", Ok),
    ("I$sub(\(123\))", Ok),
    ("$greek(Omega) man and his dog $greek(phi)do.", Ok),
    ("\$50$math(*)10$sup(9) dollars, ooh baby.", Ok),
    ("To $math(inf) and beyond.", Ok),
    ("Spodumene: LiAlSi$sub(2)O$sub(6)$sup(+)", Ok),
    ("$frac(3,5) is 60%", Ok),
    ("j$math(hat)$math(+-)5", Ok),
    ("$script(ABZN)", Ok),
    ("M$sub($frac(1,2))", Ok),

    # maybe's - depends on parser strict value
    ("reduced Planck constant: $phy(h-bar)", Maybe),
    ("$roman(A)", Maybe),
    ("$greek(tome)", Maybe),

    # bad test cases
    ("$greek Beta)", Nok),
    ("$math(>=", Nok),
    ("$", Nok),
    ("$frac(1,2,3)", Nok),

    # good in a weird way
    ("escape \\", Ok),
    ("$frac(1,apple)", Ok),
  ]
)

dsParser2 = UTDataset('ds_parser2',
  data = [
    ("$math(sum)$sub(x=0)$sup(10)x = $arabic(55)", Ok), 
    ("The $greek(Phi)$greek(Kappa)$greek(Sigma) Frat Boys", Ok),
    ("99 $math(<) 100", Ok),
  ]
)

# the database of datasets
db = UTDsDb('db',
  ds=[dsParser, dsParser2, dsUnicodeTbls, dsHtmlTbls, dsLatexTbls, dsPlainTbls])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utParser(UT):
  """ Unit test EncoderParser class. """
  def __init__(self, dskey, encoder=sut.default_encoder):
    self.encoder = encoder
    UT.__init__(self, f"EncoderParser({self.encoder})", dskey)

  def begin(self, sequencer, datum):
    self.expr = datum[0]
    self.pf   = datum[1]
    if self.pf == Maybe:
      if self.encoder.parser.strict:
        self.pf = Nok
      else:
        self.pf = Ok
    return (f"{self.expr!r}", enumfactory(UTState, self.pf))

  def test(self, sequencer, datum):
    try:
      encode = self.encoder.parse(self.expr)
    except sut.EncoderParseError as e:
      res = UTState.FAIL
      elines = str(e).split('\n')
      ans = [f"{uRArrow} error"] + elines
    else:
      res = UTState.PASS
      ans = f"{uRArrow} {encode}"
    return (res, ans)

class utPrintEncodingTables(UT):
  """ Unit test EncodingTables class. """
  def __init__(self, dskey, encoder=sut.default_encoder, in_ascii=False):
    self.encoder  = encoder
    self.in_ascii = in_ascii
    if self.in_ascii:
      UT.__init__(self, f"{encoder}.print_table(in_ascii)", dskey)
    else:
      UT.__init__(self, f"{encoder}.print_table()", dskey)

  def begin(self, sequencer, datum):
    self.tid = datum
    return f"{self.tid!r}", UTState.PASS

  def test(self, sequencer, datum):
    return UTState.PASS, f"{uRArrow} print"

  def end(self, sequencer):
    self.encoder.print_table(self.tid, in_ascii=self.in_ascii)

class ut4Some(UT):
  """ Unit test Format4Some class. """
  def __init__(self, dskey):
    UT.__init__(self, f"Format4Some()", dskey)

  def begin(self, sequencer, datum):
    self.expr = datum[0]
    self.pf   = datum[1]
    return (f"{self.expr!r}", enumfactory(UTState, self.pf))

  def test(self, sequencer, datum):
    try:
      fset = sut.Format4Some(self.expr)
    except sut.EncoderParseError as e:
      res = UTState.FAIL
      elines = str(e).split('\n')
      ans = [f"{uRArrow} error"] + elines
    else:
      with io.StringIO() as output:
        fset.print4(file=output)
        lines = output.getvalue().split('\n')
      if not lines[-1]:
        lines = lines[:-1]
      res = UTState.PASS
      ans = [f"{uRArrow}"] + lines
    return (res, ans)

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------

suite = UTSuite('testsuite',
  subsystems=[
    # Format4Some
    UTSubsys('4some', 'Test Format4Some class.',
      unittests=[
        ut4Some('ds_parser2'),
      ]
    ),

    # html
    UTSubsys('hparser', 'Test html parser.',
      unittests=[
        utParser('ds_parser', encoder=sut.html_encoder),
      ]
    ),
    UTSubsys('htables', 'Print html tables in markup.',
      unittests=[
        utPrintEncodingTables('ds_html_tbls', encoder=sut.html_encoder),
      ]
    ),

    # latex
    UTSubsys('lparser', 'Test latex parser.',
      unittests=[
        utParser('ds_parser', encoder=sut.latex_encoder),
      ]
    ),
    UTSubsys('ltables', 'Print latex tables in markup.',
      unittests=[
        utPrintEncodingTables('ds_latex_tbls', encoder=sut.latex_encoder),
      ]
    ),

    # plain text
    UTSubsys('pparser', 'Test plain text parser.',
      unittests=[
        utParser('ds_parser', encoder=sut.plain_encoder),
      ]
    ),
    UTSubsys('ptables', 'Print plain text tables in ascii.',
      unittests=[
        utPrintEncodingTables('ds_plain_tbls', encoder=sut.plain_encoder),
      ]
    ),

    # unicode
    UTSubsys('uparser', 'Test unicoder parser.',
      unittests=[
        utParser('ds_parser', encoder=sut.unicode_encoder),
      ]
    ),
    UTSubsys('utables', 'Print unicode tables in unicode.',
      unittests=[
        utPrintEncodingTables('ds_unicode_tbls', encoder=sut.unicode_encoder),
      ]
    ),
    UTSubsys('utables_ascii', 'Print unicode tables in ascii representation.',
      unittests=[
        utPrintEncodingTables('ds_unicode_tbls', encoder=sut.unicode_encoder,
          in_ascii=True),
      ]
    ),
  ],
)

utseq = UTSequencer('format', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test format module.")

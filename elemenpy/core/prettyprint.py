"""
Pretty print routines.

Package:
  RoadNarrows elemenpy package.

File:
  prettyprint.py

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
from io import (StringIO)

##-
def print2cols(lines, indent=0, c1width='auto', spacing=1, **print_kwargs):
  """
  Print lines in two columns.

  Parameters:
    lines         A list of integer indexable name,value pairs (tuple or list)
                  where name is a string, value is anything printable.
    indent        Line indentation.
    c1width       Column one width. If 'auto', then it is determined by the 
                  widest name in lines.
    spacing       Spacing between columns one and two.
    print_kwargs  Python3 print() keyword arguments.
  """
  if c1width == 'auto':
    c1width = 1
    for n,v in lines:
      if len(n) > c1width:
        c1width = len(n)
    c1width += 1    # colon
  for n,v in lines:
    n += ':'
    print(f"{'':<{indent}}{n:<{c1width}}{'':<{spacing}}{v}", **print_kwargs)

##-
def print_to_str(fn, *fn_args, **fn_kwargs):
  """
  Capture print output from a print function to a string.

  Parameters:
    fn          Print function.
    fn_args     Positional arguments to print function.
    fn_kwargs   Keyword arguments to print function.

  Returns:
    Captured output as a string. Newlines may be included in string.
  """
  lines = ''
  with StringIO() as output:
    filearg = fn_kwargs.get('file', sys.stdout)
    fn_kwargs['file'] = output
    fn(*fn_args, **fn_kwargs)
    lines = output.getvalue()
    fn_kwargs['file'] = filearg
  if lines[-1] == '\n':
    lines = lines[:-1]
  return lines

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utprettyprint as ut

  sys.exit(ut.utmain())

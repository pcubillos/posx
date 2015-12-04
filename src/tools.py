import sys
import traceback
import textwrap

# Warning separator:
sep = 70*":"


def msg(verbose, message, file=None, indent=0, noprint=False):
  """
  Conditional message printing to screen.

  Parameters:
  -----------
    verbose:  Integer
        Print only if verbose is greater than 0.
    message:  String
        The text message to print.
    file:  File object
        If not None, print message into file.
    indent:  Integer
        Number of blank spaces to indent the printed message.
    noprint:  Bool
        If True, do not print to screen/file.  Instead, return the string.
  """
  if verbose <= 0:
    return

  sentences = message.splitlines()
  indspace = " "*indent
  text = ""
  # Break the text down into the different sentences (line-breaks):
  for s in sentences:
    msg = textwrap.fill(s, break_long_words=False, initial_indent=indspace,
                                                subsequent_indent=indspace)
    text += msg + "\n"

  # Do not print, just return the string:
  if noprint:
    return text

  else:
    # Print to screen:
    print(text[:-1])  # Remove the trailing "\n"
    sys.stdout.flush()
    # Print to file, if requested:
    if file is not None:
      file.write(text)


def error(message, file=None, lev=-2):
  """
  Pretty print error message.

  Parameters:
  -----------
    message:  String
    file:  File object
    lev:  Integer
  """
  # Trace back the file, function, and line where the error source:
  t = traceback.extract_stack()
  # Extract fields:
  modpath    = t[lev][0]
  modname    = modpath[modpath.rfind('/')+1:]
  funcname   = t[lev][2]
  linenumber = t[lev][1]

  # Text to print:
  text = ("{:s}\n  Error in module: '{:s}', function: '{:s}', line: {:d}\n"
          "{:s}\n{:s}".format(sep, modname, funcname, linenumber,
                              msg(1,message,indent=4,noprint=True)[:-1], sep))

  # Print to screen:
  print(text)
  sys.stdout.flush()
  # Print to file if requested:
  if file is not None:
    file.write(text)
    file.close()
  sys.exit(0)



# -*- python -*-
#
# These SCons tests are based on the ones of boost numpy 
# (https://github.com/ndarray/Boost.NumPy/blob/master/SConscript),
# but have been altered and substantially extended.
#
# Copyright Christoph Lassner 2014.
# For the python, numpy and boost python checks, _setupPaths and _checkLibs:
# Copyright Jim Bosch 2010-2012.
#
# Distributed under the Boost Software License, Version 1.0.
#    (See http://www.boost.org/LICENSE_1_0.txt)

from boost import CheckBoostNumpy, \
                  CheckBoostPP, \
                  CheckBoostPython, \
                  CheckBoostSerialization, \
                  CheckBoostTest, \
                  CheckBoostThread, \
                  _check_dict

from python import CheckPython, \
                   CheckNumPy, \
                   _check_dict as _python_check_dict
_check_dict = dict(_check_dict, **_python_check_dict)

from opencv import CheckOpenCV,\
                   _check_dict as _opencv_check_dict
_check_dict = dict(_check_dict, **_opencv_check_dict)

def AddLibOptions(add_method, lib_names):
  options = {}
  for lib_name in lib_names:
    if not lib_name in _check_dict.keys():
      raise Exception("Unknown library: %s." % (lib_name))
    for option, keywords in _check_dict[lib_name]['options'].items():
      if not option in options.keys():
        options[option] = keywords
  for option in options.keys():
    add_method(option, **options[option])

def GetLibChecks(lib_names):
  checks = {}
  for lib_name in lib_names:
    if not lib_name in _check_dict.keys():
      raise Exception("Unknown library: %s." % (lib_name))
    for check in _check_dict[lib_name]['checks']:
      if not check.__name__ in checks.keys():
        checks[check.__name__] = check
  return checks

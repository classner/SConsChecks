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

from _tools import _checkLibs, _setupPaths
from python import CheckPython
from SCons.SConf import CheckContext
CheckContext.checkLibs = _checkLibs
import os

_check_dict = {}
_boost_option_dict = {'--boost-dir':
                      {'dest':"boost_prefix",
                      'type':"string",
                      'nargs':1,
                      'action':"store",
                      'metavar':"DIR",
                      'default':os.environ.get("BOOST_ROOT"),
                      'help':"prefix for Boost libraries; should have 'include' and 'lib' subdirectories"},
                      '--boost-inc-dir':
                      {'dest':"boost_include",
                      'type':"string",
                      'nargs':1,
                      'action':"store",
                      'metavar':"DIR",
                      'help':"location of Boost header files",
                      'default':os.environ.get("BOOST_INCLUDE_DIR")},
                      '--boost-lib-dir':
                      {'dest':"boost_lib",
                      'type':"string",
                      'nargs':1,
                      'action':"store",
                      'metavar':"DIR",
                      'help':"location of Boost libraries",
                      'default':os.environ.get("BOOST_LIB_DIR")}}
_boost_np_option_dict = { '--boost-np-dir':
                          {'dest':"boost_np_prefix",
                          'type':"string",
                          'nargs':1,
                          'action':"store",
                          'metavar':"DIR",
                          'default':os.environ.get("BOOST_ROOT"),
                          'help':"prefix for Boost numpy libraries; should have 'include' and 'lib' subdirectories"},
                          '--boost-np-inc-dir':
                          {'dest':"boost_np_include",
                          'type':"string",
                          'nargs':1,
                          'action':"store",
                          'metavar':"DIR",
                          'help':"location of Boost numpy header files",
                          'default':os.environ.get("BOOST_INCLUDE_DIR")},
                          '--boost-np-lib-dir':
                          {'dest':"boost_np_lib",
                          'type':"string",
                          'nargs':1,
                          'action':"store",
                          'metavar':"DIR",
                          'help':"location of Boost numpy libraries",
                          'default':os.environ.get("BOOST_LIB_DIR")}}

def CheckBoostPython(context):
    bp_source_file = r"""
// Get diagnostics in the log.
#define BOOST_LIB_DIAGNOSTIC
#include "boost/python.hpp"
class Foo { public: Foo() {} };
int main()
{
  Py_Initialize();
  boost::python::object obj;
  boost::python::class_< Foo >("Foo", boost::python::init<>());
  Py_Finalize();
  return 0;
}
"""
    context.Message('Check building against Boost.Python... ')
    _setupPaths(context.env,
        prefix = context.env.GetOption("boost_prefix"),
        include = context.env.GetOption("boost_include"),
        lib = context.env.GetOption("boost_lib")
        )
    if context.env['CC'] == 'cl':
        # Use msvc's autolinking support.
        result = (context.checkLibs([''], bp_source_file))
    else:
        result = (
            context.checkLibs([''], bp_source_file) or
            context.checkLibs(['boost_python'], bp_source_file) or
            context.checkLibs(['boost_python-mt'], bp_source_file)
            )
    if not result:
        context.Result(0)
        print "Cannot build against Boost.Python."
        return False
    result, output = context.TryRun(bp_source_file, '.cpp')
    if not result:
        context.Result(0)
        print "Cannot run program built against Boost.Python."
        return False
    context.Result(1)
    return True
_check_dict['boost.python'] = {'options': _boost_option_dict,
                                'checks': [CheckPython, CheckBoostPython]}

def CheckBoostNumpy(context):
    bp_source_file = r"""
// Get diagnostics in the log.
#define BOOST_LIB_DIAGNOSTIC
#include "boost/python.hpp"
#include <boost/numpy.hpp>
namespace py = boost::python;
namespace np = boost::numpy;
class Foo { public: Foo(np::ndarray &t) {} };
int main()
{
  Py_Initialize();
  np::initialize();
  boost::python::object obj;
  boost::python::class_< Foo >("Foo", boost::python::init<np::ndarray&>());
  Py_Finalize();
  return 0;
}
"""
    context.Message('Check building against Boost.Numpy... ')
    _setupPaths(context.env,
        prefix = context.env.GetOption("boost_np_prefix"),
        include = context.env.GetOption("boost_np_include"),
        lib = context.env.GetOption("boost_np_lib")
        )
    if context.env.GetOption("debug_checks"):
      result = (context.checkLibs(['boost_numpy_d'], bp_source_file))
    else:
      result = (context.checkLibs(['boost_numpy'], bp_source_file))
    if not result:
        context.Result(0)
        print "Cannot build against Boost.Numpy."
        return False
    result, output = context.TryRun(bp_source_file, '.cpp')
    if not result:
        context.Result(0)
        print "Cannot run program built against Boost.Numpy."
        return False
    context.Result(1)
    return True
_check_dict['boost.numpy'] = {'options': dict(_boost_option_dict, **_boost_np_option_dict),
                              'checks': [CheckBoostPython, CheckBoostNumpy]}

def CheckBoostSerialization(context):
    boost_source_file = r"""
// Get diagnostics in the log.
#define BOOST_LIB_DIAGNOSTIC
#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/serialization/serialization.hpp>
#include <sstream>

int main()
{
  std::stringstream ss;
  boost::archive::text_oarchive oa(ss);
  int t = 5;
  oa << t;
  int t2 = 0;
  boost::archive::text_iarchive ia(ss);
  ia >> t2;
  return (t != t2);
}
"""
    context.Message('Check building against Boost.Serialization... ')
    _setupPaths(context.env,
        prefix = context.env.GetOption("boost_prefix"),
        include = context.env.GetOption("boost_include"),
        lib = context.env.GetOption("boost_lib")
        )
    if context.env['CC'] == 'cl':
        # Use msvc's autolinking support.
        result = (context.checkLibs([''], boost_source_file))
    else:
        result = (
            context.checkLibs([''], boost_source_file) or
            context.checkLibs(['boost_serialization'], boost_source_file) or
            context.checkLibs(['boost_serialization-mt'], boost_source_file)
            )
    if not result:
        context.Result(0)
        print "Cannot build against Boost.Serialization."
        return False
    result, output = context.TryRun(boost_source_file, '.cpp')
    if not result:
        context.Result(0)
        print "Cannot run program built against Boost.Serialization."
        return False
    context.Result(1)
    return True
_check_dict['boost.serialization'] = {'options': _boost_option_dict,
                                      'checks': [CheckBoostSerialization]}

def CheckBoostTest(context):
    boost_source_file = r"""
#define BOOST_TEST_MODULE "dummy module"
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_CASE( my_test )
{
    BOOST_REQUIRE( 1+1==2 );
}
"""
    context.Message('Check building against Boost.Test... ')
    _setupPaths(context.env,
        prefix = context.env.GetOption("boost_prefix"),
        include = context.env.GetOption("boost_include"),
        lib = context.env.GetOption("boost_lib")
        )
    if context.env['CC'] == 'cl':
        # Use msvc's autolinking support.
        result = (context.checkLibs([''], boost_source_file))
    else:
        result = (
            context.checkLibs([''], boost_source_file) or
            context.checkLibs(['boost_test'], boost_source_file)
            )
    if not result:
        context.Result(0)
        print "Cannot build against Boost.Test."
        return False
    result, output = context.TryRun(boost_source_file, '.cpp')
    if not result:
        context.Result(0)
        print "Cannot run program built against Boost.Test."
        return False
    context.Result(1)
    return True
_check_dict['boost.test'] = {'options': _boost_option_dict,
                             'checks': [CheckBoostTest]}
  
def CheckBoostThread(context):
    boost_source_file = r"""
// Get diagnostics in the log.
#define BOOST_LIB_DIAGNOSTIC
#include <boost/thread.hpp>

void workerFunc() {
  int i = 0;
  for (int j = 0; j < 5; ++j)
    ++i;
}

int main()
{
  boost::thread workerThread(workerFunc);
  workerThread.join();
  return 0;
}
"""
    context.Message('Check building against Boost.Thread... ')
    _setupPaths(context.env,
        prefix = context.env.GetOption("boost_prefix"),
        include = context.env.GetOption("boost_include"),
        lib = context.env.GetOption("boost_lib")
        )
    if context.env['CC'] == 'cl':
        # Use msvc's autolinking support.
        result = (context.checkLibs([''], boost_source_file))
    else:
        result = (
            context.checkLibs([''], boost_source_file) or
            context.checkLibs(['boost_thread'], boost_source_file) or
            context.checkLibs(['boost_thread-mt'], boost_source_file)
            )
    if not result:
        context.Result(0)
        print "Cannot build against Boost.Thread."
        return False
    result, output = context.TryRun(boost_source_file, '.cpp')
    if not result:
        context.Result(0)
        print "Cannot run program built against Boost.Thread."
        return False
    context.Result(1)
    return True
_check_dict['boost.thread'] = {'options': _boost_option_dict,
                                'checks': [CheckBoostThread]}

def CheckBoostPP(context):
    boost_source_file = r"""
#include <boost/preprocessor/cat.hpp> 

#define STATIC_ASSERT(EXPR)\
  enum\
  { BOOST_PP_CAT(static_check_,__LINE__) = (EXPR) ? 1 : -1\
  };\
  typedef char\
    BOOST_PP_CAT(static_assert_,__LINE__)\
    [ BOOST_PP_CAT(static_check_,__LINE__)\
    ]

int main()
{
  STATIC_ASSERT(sizeof(int) <= sizeof(long));
  return 0;
}
"""
    context.Message('Check building against Boost.Preprocessor... ')
    _setupPaths(context.env,
        prefix = context.env.GetOption("boost_prefix"),
        include = context.env.GetOption("boost_include"),
        lib = context.env.GetOption("boost_lib")
        )
    result = (context.checkLibs([''], boost_source_file))
    if not result:
        context.Result(0)
        print "Cannot build against Boost.Preprocessor."
        return False
    result, output = context.TryRun(boost_source_file, '.cpp')
    if not result:
        context.Result(0)
        print "Cannot run program built against Boost.Preprocessor."
        return False
    context.Result(1)
    return True
_check_dict['boost.preprocessor'] = {'options': _boost_option_dict,
                                     'checks': [CheckBoostPP]}

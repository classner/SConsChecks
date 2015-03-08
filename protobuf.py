# -*- python -*-
#
# Copyright Christoph Lassner 2015.
#
# Distributed under the Boost Software License, Version 1.0.
#    (See http://www.boost.org/LICENSE_1_0.txt)
from __future__ import print_function
from ._tools import _checkLibs, _setupPaths
from SCons.SConf import CheckContext
CheckContext.checkLibs = _checkLibs
import os
import subprocess

_check_dict = {}
_protobuf_option_dict = {'--protobuf-dir':
                           {'dest':"protobuf_prefix",
                           'type':"string",
                           'nargs':1,
                           'action':"store",
                           'metavar':"DIR",
                           'default':os.environ.get("PROTOBUF_ROOT"),
                           'help':"prefix for protobuf; should contain the 'src' folder."},
                           '--protoc':
                           {'dest':"protoc",
                           'type':"string",
                           'nargs':1,
                           'action':"store",
                           'metavar':"EXEC",
                           'help':"this is the protoc executable.",
                           'default':os.environ.get("PROTOC")}}

def CheckProtobuf(context):
    context.Message('Check that protoc is available... ')
    if not context.env.GetOption("protoc") is None:
        result = os.path.isfile(context.env.GetOption("protoc"))
    else:
        if os.name != 'nt':
            result = not subprocess.call(['which', 'protoc'])
        else:
            result = not subprocess.call(['where', 'protoc'])
    if not result:
        context.Result(0)
        print("Cannot find protoc!")
        return False
    context.Message('Check that protobuf header files are available...')
    source_file = r"""
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>

int main() {
  return 0;
}
"""
    if not context.env.GetOption("protobuf_prefix") is None:
        context.env.PrependUnique(CPPPATH=[os.path.join(context.env.GetOption("protobuf_prefix"), 'src')])
        if os.name == 'nt':
            context.env.PrependUnique(LIBPATH=[os.path.join(context.env.GetOption("protobuf_prefix"), 'vsprojects', 'x64', 'Release')])
    result = context.checkLibs(['libprotobuf'], source_file)
    if not result:
        context.Result(0)
        print("Cannot build with PROTOBUF headers.")
        return False
    context.Result(1)
    return True
_check_dict['protobuf'] = {'options': _protobuf_option_dict,
                           'checks': [CheckProtobuf]}

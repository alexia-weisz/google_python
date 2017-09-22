#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def get_special_paths(thisdir):
    if os.path.exists(thisdir):
        special_fnames = []
        filenames = os.listdir(thisdir)
        for fname in filenames:
            match = re.search(r'__\w+__', fname)
            if match:
                special_fnames.append(os.path.abspath(fname))
        return special_fnames
    else:
        return None

def copy_to(paths, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

    for path in paths:
        shutil.copy(path, dir)

def zip_to(paths, zippath):
    inputs = ' '.join(paths)
    cmd = 'zip -j '+ ' '.join((zippath, inputs))
    print("Command I'm going to do: " + cmd)
    (status, output) = commands.getstatusoutput(cmd)
    if status:
        sys.stderr.write(output + '\n')
        sys.exit(status)
    print(output)



def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
      print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
      sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
      todir = args[1]
      del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
      tozip = args[1]
      del args[0:2]

    if len(args) == 0:
      print "error: must specify one or more dirs"
      sys.exit(1)

    # +++your code here+++
    # Call your functions
    thisdir = args[0]
    special_fnames = get_special_paths(thisdir)
    if special_fnames is None:
        print('Error: No special files exist in ', thisdir)
        sys.exit(1)
        
    if todir:
        copy_to(special_fnames, todir)

    elif tozip:
        zip_to(special_fnames, tozip)

    else:
        for fname in special_fnames:
            print(fname)
  
if __name__ == "__main__":
    main()

#!/usr/bin/env python

import os
import sys
import subprocess

def main():
   travis = is_travis()

   if travis == True:
      set_git_config()

   for module in os.listdir('.'):
      if os.path.isdir(module) and os.path.isfile(module + '/package.py'):
         commit_change(module)

def set_git_config():
   if 'NAME' in os.environ and 'EMAIL' in os.environ:
      os.system(
         'git config user.email ' + os.environ['EMAIL'] + ' && ' \
         'git config user.name ' + os.environ['NAME'])

def commit_change(module):
   if output('git status %s --porcelain | sed s/^...//' % module):
      version = get_package_version(module)
      print(
         'git add ./' + module + ' && ' + \
         'git commit -m "Travis: Add ' + module + ' last update on ' + version + ' version"')

def output(command):
   return subprocess.check_output(command, shell=True).decode(sys.stdout.encoding)

def get_package_version(module):
   with open(module + '/PKGBUILD') as f:
      for line in f.readlines():
         if line.startswith('pkgver='):
            return line.split('=', 1)[1].rstrip("\n\r")

def is_travis():
   if "IS_TRAVIS_BUILD" in os.environ:
      return True
   else:
      return False

if __name__ == '__main__':
   main()
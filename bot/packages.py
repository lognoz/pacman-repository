#!/usr/bin/env python

import os
import sys
import shutil

from utils.editor import edit_file, replace_ending, extract
from utils.terminal import output
from utils.constructor import constructor

class new(constructor):
   def build(self):
      sys.path.append(self.path_pkg)

      for name in self.packages:
         module = package(
            name = name,
            path_pkg = self.path_pkg,
            path_mirror = self.path_mirror
         )

         module.prepare()
         module.pull()
         module.make()

         if module.compiled == True:
            return

class package(constructor):
   compiled = False

   def construct(self):
      __import__(self.name + ".package")
      os.chdir(self.path_pkg + "/" + self.name)

      self.path = self.path_pkg + "/" + self.name
      self.package = sys.modules[self.name + ".package"]

   def prepare(self):
      self.set_utils()
      self.clean_directory()

   def make(self):
      self.version = extract(self.path, "pkgver")

      if "pre_build" in dir(self.package):
         self.package.pre_build()

      if not self.is_builded():
         self.compiled = True
         self.commit()
         self.install_dependencies()
         self.build()

   def commit(self):
      os.system(
         'git add . && ' + \
         'git commit -m "Bot: Add last update into ' + self.package.name + ' package ~ version ' + self.version + '"')

   def is_builded(self):
      if not output("git status . --porcelain | sed s/^...//"):
         return False

      for f in os.listdir(self.path_mirror):
         if f.startswith(self.name + '-' + self.version + '-'):
            return False

      return True

   def install_dependencies(self):
      packages = output("source ./PKGBUILD && echo ${makedepends[@]}")

      if packages.strip() != "":
         os.system("sudo pacman -S %s --noconfirm" % packages)

   def build(self):
      os.system(
         "makepkg -Asc --skipinteg && " \
         "mv *.pkg.tar.xz " + self.path_mirror);

   def pull(self):
      os.system(
         "git init --quiet && " \
         "git remote add origin " + self.package.source + " && " \
         "git pull origin master --quiet && " \
         "rm -rf .git")

      if os.path.isfile(".SRCINFO"):
         os.remove(".SRCINFO")

   def clean_directory(self):
      files = os.listdir(".")
      for f in files:
         if os.path.isdir(f):
            shutil.rmtree(f)
         elif os.path.isfile(f) and f != "package.py":
            os.remove(f)

   def set_utils(self):
      self.package.edit_file = edit_file
      self.package.replace_ending = replace_ending


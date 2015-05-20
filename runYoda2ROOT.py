#!/usr/bin/env python
import os, sys, ROOT

os.chdir(sys.argv[1])
file_l = [x for x in os.listdir(".") if x.endswith(".yoda")]
for i, x in enumerate(file_l):
  print i+1, x
  in_file = x
  os.system("../yoda2root.py %s"%x)


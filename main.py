# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 18:50:00 2020

@author: ydeng
"""
import sys

from simulation import Simulation
from configuration import Config
from database import Database

time_unit = 1 # 1 second by default
if len(sys.argv) > 2:
  print("Usage: python main.py <time_unit_by_seconds>")
elif len(sys.argv) == 1:
  print("Default time unit is 1 second. You can use python main.py <time_unit_by_seconds> to specify.")
else:
  time_unit = int(sys.argv[1])
  print("Use %d seconds as time unit" % time_unit)

cfg = Config("config.xlsx")
db = Database(cfg)

s = Simulation(cfg, db, time_unit)
s.run()

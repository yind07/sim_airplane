# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 11:22:20 2020

@author: ydeng
"""
import math
import random
import pandas # get info from excel file

from constant import IName, FName, WType

class Config:
    def __init__(self, filename):
        print("Get static configuration info from %s" % filename)
        xls = pandas.ExcelFile(filename)
        
        self.__cfg_db(xls)
        self.__cfg_sim(xls)

    def init_db(self):
        print("Init DB tables - <depends>")

    def __cfg_db(self, h_xls):
      dh = pandas.read_excel(h_xls, "database")
      self.ip = str(dh.loc[0, "ip"])
      self.username = str(dh.loc[0, "username"])
      self.password = str(dh.loc[0, "password"])
      #print("ip=%s, %s/%s" % (self.ip, self.username, self.password))

    def __cfg_sim(self, h_xls):
      dh = pandas.read_excel(h_xls, "simulation")
      cfg_col_val = "Value"
      row_id_speed = 0      # 飞行速度(km/hr)
      row_id_deviation = 1  # 速度偏差
      row_id_posx_lb = 2    # 导航X坐标下限(km)
      row_id_posx_ub = 3    # 导航X坐标上限(km)
      row_id_posy_lb = 4    # 导航Y坐标下限(km)
      row_id_posy_ub = 5    # 导航Y坐标上限(km)
      row_id_posz_lb = 6    # 导航Z坐标下限(km)
      row_id_posz_ub = 7    # 导航Z坐标上限(km)
      row_id_safe_angle = 8    # 安全距离夹角[0,360)
      row_id_collision_duration = 9 # 预设撞击时间间隔(sec)

      self.speed = dh.loc[row_id_speed, cfg_col_val]
      self.deviation = dh.loc[row_id_deviation, cfg_col_val]
      self.posx_lb = dh.loc[row_id_posx_lb, cfg_col_val]
      self.posx_ub = dh.loc[row_id_posx_ub, cfg_col_val]
      self.posy_lb = dh.loc[row_id_posy_lb, cfg_col_val]
      self.posy_ub = dh.loc[row_id_posy_ub, cfg_col_val]
      self.posz_lb = dh.loc[row_id_posz_lb, cfg_col_val]
      self.posz_ub = dh.loc[row_id_posz_ub, cfg_col_val]
      self.safe_angle = dh.loc[row_id_safe_angle, cfg_col_val]
      self.collision_duration = dh.loc[row_id_collision_duration, cfg_col_val]
      #print("speed: %d, deviation: %.2f, x[%d, %d], y[%d, %d], z[%d, %d]" % (self.speed, self.deviation, self.posx_lb, self.posx_ub, self.posy_lb, self.posy_ub, self.posz_lb, self.posz_ub))

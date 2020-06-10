# -*- coding: utf-8 -*-
"""
Created on Fri May 29 10:14:26 2020

@author: ydeng
"""
import math

# point coordinate in 3D space
class Position:
    def __init__(self, x=0, y=0, z=0):
      self.x = x
      self.y = y
      self.z = z
      self.ratio = 1000 # 1km = 1000m
    
    # display unit: meter
    def __str__(self):
      return "(%d, %d, %d)" % (self.x*self.ratio,self.y*self.ratio,self.z*self.ratio)

    def distance(self, pos):
      return math.sqrt(math.pow(pos.x-self.x, 2)
                       + math.pow(pos.y-self.y, 2)
                       + math.pow(pos.z-self.z, 2))

    # check if (x, y) is within the area of circle with radius == r
    def is_in_range(self, r):
      return math.pow(self.x, 2) + math.pow(self.y, 2) <= math.pow(r, 2)
    
    # 返回(self.x, self.y)对应的极坐标(r, theta)
    def get_polar_xy(self):
      r = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
      rad = math.acos(self.x/r) # y>=0, x:[1,-1] <=> rad:[0,pi]
      if self.y < 0: # adjust the angle!
        rad = math.pi*2 - rad # y<0, x:[-1,1] <=> rad:[pi,2pi)
      return r,rad
    
    # circle around the origin, counter-clockwise
    # unit: r(km), speed(m)
    # update self position
    def circle(self, speed):
      # rad_old: 当前夹角
      r, rad_old = self.get_polar_xy()
      rad_delta = speed/(r*self.ratio)
      
      # 单位时间后新夹角
      rad_new = rad_old + rad_delta
      #print("old=%.3f, delta=%.3f, new=%.3f" % (rad_old, rad_delta, rad_new))
      # 新坐标
      # x>=0,y>=0
      self.x = r * math.cos(rad_new)
      self.y = r * math.sin(rad_new)
        
        
    # 飞机从当前点以速度speed飞向target position
    # 单位时间(s)后当前位置变化
    def fly(self, target, speed):
      speed_square = math.pow(speed, 2)
      delta_x = target.x - self.x
      delta_y = target.y - self.y
      delta_z = target.z - self.z
      print("delta-2-target: %s" % Position(delta_x,delta_y,delta_z))

      if delta_x == 0 or delta_y == 0 or delta_z == 0:
        print("Found 0: delta_x=%d, delta_y=%d, delta_z=%d" % (delta_x,delta_y,delta_z))
        print("self: %s, target: %s, speed: %d" % (self, target, speed))
        return

      mx = 1 + math.pow(delta_y/delta_x, 2) + math.pow(delta_z/delta_x, 2)
      if delta_x >= 0:
        self.x += (math.sqrt(speed_square/mx)/self.ratio)
      else:
        self.x -= (math.sqrt(speed_square/mx)/self.ratio)
      
      my = 1 + math.pow(delta_x/delta_y, 2) + math.pow(delta_z/delta_y, 2)
      if delta_y >= 0:
        self.y += (math.sqrt(speed_square/my)/self.ratio)
      else:
        self.y -= (math.sqrt(speed_square/my)/self.ratio)
      
      mz = 1 + math.pow(delta_x/delta_z, 2) + math.pow(delta_y/delta_z, 2)
      self.z += (math.sqrt(speed_square/mz)/self.ratio)
      
    def is_height_ok(self, target):
      return self.z >= target.z
    
    # preconditions:
    #   (self.x,self.y) and (pos.x,pos.y) have same polar r
    # return the arc length from pos to self (so it has direction!)
    def distance_in_circle(self, pos):
      r1,rad1 = self.get_polar_xy()
      r2,rad2 = pos.get_polar_xy()
      delta_degree = int(math.fabs(rad1-rad2)*180/math.pi)
      #print("polar1=(%.2f, %.2f), polar2=(%.2f, %.2f),delta_degree = %d " % (r1,rad1,r2,rad2,delta_degree))
      # assert: r1 == r2
      if rad2 < rad1:
        return r1 * (rad1-rad2)
      elif rad2 > rad1:
        return r1 * (rad1+math.pi*2-rad2)
      return 0
      
      
      

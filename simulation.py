# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 18:50:00 2020

@author: ydeng
"""

import math
import csv
import random
import datetime
import time
import keyboard

from position import Position

class Simulation:
    def __init__(self, cfg, db, time_unit):
      self.config = cfg
      self.db = db
      self.tunit = time_unit
      self.target_pos = self.get_pilot_pos()
      print("Target position: %s" % self.target_pos)
        
    def run(self):
      print("\nStart simulation for aircrafts >>")
      t0 = datetime.datetime.now()
      pos = Position()
      
      # 记录
      # format example: 200507102338
      self.save_log(pos, None, None, 0)
      self.adjust_time(t0)

      while not pos.is_height_ok(self.target_pos):
        ts = datetime.datetime.now()
        #print("\ncurrent position: %s" % pos)
        print('.', end='', flush=True) # more responsive!
        speed = get_speed(self.config.speed, self.config.deviation)
        pos.fly(self.target_pos, speed)
        
        self.save_log(pos, None, None, 0)
        self.adjust_time(ts)
      
      ts = datetime.datetime.now()
      print("\ncurrent position: %s" % pos)
      # force current position to target position!
      pos = self.target_pos
      print("After adjustment: current position: %s" % pos)
      # position of the second aircraft
      pos2 = get_second_pos(pos, self.config.safe_angle)
      print("The second position: %s" % pos2)

      gap = pos.distance_in_circle(pos2)
      c_speed = self.get_collision_speed(gap*pos.ratio)
      last_gap = gap # for collision check!
      
      print("\nStart circling >>>")
      distance = 0 # total circling distance by meters
      cnt = 0 # how long does it take to fly one circle
      cnt_circle = 0 # cnt for the # of circles
      # assume 导航X坐标上限(km) == 导航Y坐标上限(km)
      if pos.is_in_range(self.config.posx_ub):
        r = math.sqrt(math.pow(pos.x, 2) + math.pow(pos.y, 2))
        circum = 2*math.pi*r # circumference by km
        print("Circling around the origin O: R(m) = %d, C(m) = %.2f" % (r*pos.ratio, circum*pos.ratio))
        #start = datetime.datetime.now()
        while cnt_circle < self.config.maxnum_circling:
          # detect key pressing
          if keyboard.is_pressed('q'):
            #print('You Pressed a Key!')
            break # quit decently

          print('.', end='', flush=True) # more responsive!
          speed = get_speed(self.config.speed, self.config.deviation)
          pos.circle(speed)
          speed2 = speed
          
          # attack check - TODO
          attack = get_attack(cnt_circle)
          if attack == 1:
            speed2 = c_speed
            last_gap = gap
          pos2.circle(speed2)  # simple handling - same speed+deviation
          cnt += 1
          distance += speed
          # new gap
          gap = pos.distance_in_circle(pos2)
          #print("Distance(m): %.3f" % (gap*pos.ratio))
          
          # check collision before log!
          if self.is_in_collision(gap*pos.ratio, last_gap*pos.ratio):
            print("\n\n### Air Collision!!! cnt = %d" % cnt)
            # adjust pos2 to match pos1, then do last log
            pos2 = pos
            gap = 0
            self.save_log(pos, pos2, gap, attack)

            tdlt = datetime.datetime.now() - t0
            print(">>> 本次演示实际花费 %d小时%d分钟%d秒" % (tdlt.seconds/3600,tdlt.seconds%3600/60,tdlt.seconds%60))
            return
          
          self.save_log(pos, pos2, gap, attack)
          self.adjust_time(ts)
          ts = datetime.datetime.now()
          
          if math.floor(distance/pos.ratio/circum) > cnt_circle:
            cnt_circle = math.floor(distance/pos.ratio/circum)
            print("\n\nHas flown %d circle(s)!" % cnt_circle)
            print("[%d] current position: %s" % (cnt,pos))
            cnt = 0
        tdlt = datetime.datetime.now() - t0
        print("\n\n>>> 本次演示实际花费 %d小时%d分钟%d秒" % (tdlt.seconds/3600,tdlt.seconds%3600/60,tdlt.seconds%60))
      else:
        print("Fly to the track, then circling - obsolete")
      
      
 
    # 产生地面导航坐标:
    # assume: cfg.posx_ub == cfg.posy_ub
    # make sure:
    #   1.  x^2 + y^2 <= cfg.posx_ub^2
    #   2.  x != 0, y != 0
    def get_pilot_pos(self):
      cfg = self.config

      x = random.randint(cfg.posx_lb, cfg.posx_ub)
      while x == 0:
        time.sleep(1) # 1s
        x = random.randint(cfg.posx_lb, cfg.posx_ub)
      #make sure x^2 + y^2 <= cfg.posx_ub^2
      y_ub = math.floor(math.sqrt(math.pow(cfg.posx_ub,2) - math.pow(x,2)))
      y = random.randint(0-y_ub, y_ub)
      while y == 0:
        time.sleep(1) # 1s
        y = random.randint(0-y_ub, y_ub)

      z = random.randint(cfg.posz_lb, cfg.posz_ub)

      #return Position(6,-10,10)   # for test      
      return Position(x,y,z)
    
    def get_collision_speed(self, distance_in_circle):
      return distance_in_circle/self.config.collision_duration + self.config.speed
    
    # return True if within collision area
    # return False otherwise
    # assumption:
    #   Once attack begins, gap reduces(the 2nd airplane tries
    #   to catch up the 1st one), so gap < last_gap
    #   If gap > last_gap, this means the 2nd airplane has
    #   exceeded the 1st one, when the collision happened!
    #   math.isclose() is added to cancel the float number calculation deviation
    def is_in_collision(self, gap, last_gap):
      if math.isclose(gap, last_gap, rel_tol=1e-03):
        return False
      return gap > last_gap
    
    # write periodic log to DB and csv
    def save_log(self, pos1, pos2, gap, attack):
      if self.config.enable_log_csv:
        with open(self.config.logfname, 'a', newline='') as h:
          w = csv.writer(h)
          if gap == None:
            w.writerow([int(pos1.x*pos1.ratio),int(pos1.y*pos1.ratio),int(pos1.z*pos1.ratio),"?","?","?","?",attack])
          else:
            w.writerow([int(pos1.x*pos1.ratio),int(pos1.y*pos1.ratio),int(pos1.z*pos1.ratio),int(pos2.x*pos2.ratio),int(pos2.y*pos2.ratio),int(pos2.z*pos2.ratio),int(gap*pos1.ratio),attack])
        h.close()
        self.db.clear_table("sim_airplane")
        self.db.add_coordinates(pos1, pos2, gap, attack)

    def adjust_time(self, ts):
      tdelta = datetime.datetime.now() - ts
      while tdelta.seconds < self.tunit:
        time.sleep(0.1) # 100ms
        tdelta = datetime.datetime.now() - ts
        # detect key pressing
        if keyboard.is_pressed('q'):
          break
    
# return real speed after deviation is counted     
def get_speed(base, deviation):
  lb = math.ceil(base*(1-deviation))
  ub = math.floor(base*(1+deviation))
  speed = random.randint(lb, ub)
  #print("speed(m/sec): %d" % speed)
  return speed

# return the 2nd aircraft's position, which satisfies:
# 1. out of the safety distance
# 2. randomly
def get_second_pos(pos, safe_angle):
  r, rad = pos.get_polar_xy()
  degree = rad*180/math.pi
  # danger area: (left, right)
  # safe area: [right, left+2pi]
  d_left = math.floor(degree - safe_angle)
  d_right = math.ceil(degree + safe_angle)
  #print("degree: %d, safe_angle: %d, left: %d, right: %d" % (degree, safe_angle, d_left, d_right))
  #print("safe area: [%d, %d]" % (d_right, d_left+360))
  #print("ERROR: Something MUST be wrong: safe_angle degree = %d" % (safe_angle_rad*180/math.pi))
  angle_degree = random.randint(d_right, d_left+360)
  angle_rad = angle_degree*math.pi/180
  #print("random angle: [%d, %.2f]" % (angle_degree, angle_rad))
  
  px = r * math.cos(angle_rad)
  py = r * math.sin(angle_rad)
  return Position(px,py,pos.z)

def get_attack(cnt):
  return 0
  #if cnt <= 6:
  #  return 0
  #return 1
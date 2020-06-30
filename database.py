# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:35:05 2020

@author: ydeng
"""
#import sys
import MySQLdb
#from constant import FName, WType

class Database:
  def __init__(self, cfg):
    dbname = 'sim'
    self.db = MySQLdb.connect(cfg.ip, cfg.username, cfg.password, dbname, charset='utf8')
    print("Connected to DB successfully.")
    self.db.autocommit(True)
  
  # return dict: key=fname, val=dict_1 (key=fid(0-9), val=0/1)
  # 0为正常，1为攻击状态
  # specific id for airplane sim
  #   id | type    | count | status | plcattack 
  #    0 | 飞行模拟 | 1     | 0x00   | 0x00
  def get_attack(self):
    #print("%s" % __name__)
    tbl_name = "attacksignal"
    c = self.db.cursor()
    query = "SELECT * FROM %s" % tbl_name
    c.execute(query)
    
    # meaning for column index
    i_id = 0
    #i_type = 1
    #i_count = 2
    i_status = 3
    result = c.fetchall()
    for row in result:
      if row[i_id] == 0:
        status = int.from_bytes(row[i_status], "little")
        return status
    return 0 # just in case the specific row is removed! 
  
  # return true if mname is ready, return false otherwise
  def is_module_ready(self, mname):
    print("%s: Check if %s is ready, return boolean - <depends>" % (self.is_module_ready.__name__, mname))
    return True
  
  def clear_table(self, tbl_name):
    c = self.db.cursor()
    c.execute("TRUNCATE %s" % tbl_name)
    c.close()

  def add_coordinates(self, pos1, pos2, gap, attack):
    tbl_name = "sim_airplane"
    c = self.db.cursor()
    if gap == None:
      query = "INSERT INTO %s values (%d,%d,%d,NULL,NULL,NULL,NULL,%d)" % (tbl_name,pos1.x*pos1.ratio,pos1.y*pos1.ratio,pos1.z*pos1.ratio,attack)
    else:
      query = "INSERT INTO %s values (%d,%d,%d,%d,%d,%d,%d,%d)" % (tbl_name,pos1.x*pos1.ratio,pos1.y*pos1.ratio,pos1.z*pos1.ratio,pos2.x*pos2.ratio,pos2.y*pos2.ratio,pos2.z*pos2.ratio,gap*pos1.ratio,attack)
    #query = "INSERT INTO %s values ('%s',%d,'%s','N/A','N/A',NULL,0,NULL,0,NULL,NULL,NULL,0)" % (tbl_name, fname,fid,fstatus)      
    #print(query)
    c.execute(query) #c.execute(query.encode("cp936"))
    c.close()
    #quit()
    #sys.exit(0)

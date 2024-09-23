# -*- coding: utf-8 -*-
import datetime
import time
import random
import logging


class Mongodbcrud:

    def __init__(self):
        pass

    # Keyword 

    def mongodb_update_timestamp_object_id(self):
        timestamp = hex(int(time.time()))[2:]
        object_id = timestamp + ''.join([hex(random.randint(0, 15))[2:] for _ in range(16)])
        thai_time = self._objectid_to_utc_thai_time(object_id)
        utc_time = self._objectid_to_utc_time(object_id)
        #log result
        logging.info("Mongodb Ts OdjectId : %s" % (object_id))
        logging.info("UTC Time : %s" % (utc_time))
        logging.info("UTC Thai Time : %s" % (thai_time))
        return object_id
    
    #Private Function

    def _objectid_to_utc_thai_time(self,objectid):
        # ดึง 4 ไบต์แรกของ ObjectId (8 ตัวอักษรแรก) และแปลงเป็นฐาน 10
        timestamp = int(objectid[:8], 16)
        
        # แปลง timestamp เป็นวันที่และเวลา UTC
        utc_time = datetime.datetime.utcfromtimestamp(timestamp)

        # เพิ่ม 7 ชั่วโมงเพื่อแปลงเป็นเวลาไทย (THA)
        tha_time = utc_time + datetime.timedelta(hours=7)
        
        return tha_time
    
    def _objectid_to_utc_time(self,objectid):
        # ดึง 4 ไบต์แรกของ ObjectId (8 ตัวอักษรแรก) และแปลงเป็นฐาน 10
        timestamp = int(objectid[:8], 16)
        
        # แปลง timestamp เป็นวันที่และเวลา UTC
        utc_time = datetime.datetime.utcfromtimestamp(timestamp)
        
        return utc_time
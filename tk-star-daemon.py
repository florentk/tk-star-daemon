#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import socket
import time
import threading

TK_STAR_BINARY_DATA_MAGIC_NUMBER = b'\x24'
#NORTH = b'\x30'
#EAST = b'\x60'
PORT_NUMBER = 7000

def to_hexa_array(data):
  return ["%02x" % ord(d) for d in data]

def to_hexa_string(data):
  return ''.join(to_hexa_array(data))
  
def to_hexa_human_string(data):
  return ':'.join(to_hexa_array(data))  
  
def to_hexa_int(d):
  return int("%02x" % ord(d))
  
def decode_time_stamp(data):
  h = to_hexa_int(data[0])
  m = to_hexa_int(data[1])
  s =  to_hexa_int(data[2])
  y =  to_hexa_int(data[3])
  mt =  to_hexa_int(data[4])
  d =  to_hexa_int(data[5])
  return (y,mt,d,h,m,s,-1,-1,-1)
  
def decode_latitude(data):
  s = to_hexa_string(data)
  d = int(s[:2]) #degree
  sm = "%s.%s" % (s[2:4],s[4:8])
  m = float(sm) #minute
  #h = 1 if data[4] == NORTH else -1
  return d + m/60.0
  
def decode_longitude(data):
  s = to_hexa_string(data)
  d = int(s[:3]) #degree
  sm="%s.%s" % (s[3:5],s[5:9])
  m = float(sm) #minute
  #h = 1 if data[4] == EAST else -1
  return d + m/60.0 
 
def decode_tk_star_gps_data(data):
  if(data[0] == TK_STAR_BINARY_DATA_MAGIC_NUMBER):
    dev = to_hexa_string(data[1:6])
    timestamp = time.mktime(decode_time_stamp(data[6:12]))
    lat = decode_latitude(data[12:17])
    lon = decode_longitude(data[17:22])
    return dev,timestamp,lat,lon
  return data  
  
def gps_data_to_string(g):
  if len(g) == 4 :
    return "Device : %s\nTime : %s\nLatitude : %f\nLongitude : %f" % (g[0],time.ctime(g[1]),g[2],g[3])
  else:
    return str(g)
    
def service(client):
  try:
    while True:
      data = client.recv(1024)
      if len(data) > 0:
        print to_hexa_human_string(data)
        print gps_data_to_string(decode_tk_star_gps_data(data))
        print ""   
  except :  
    print address,"is deconnected"   
    client.close() 
  print address,"is deconnected"  
  client.close() 
  
  
  
  
class ClientThread(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        
    def run(self):
        service(self.client)
  
def listen(port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', port))

  print "Listen on port" , port , "..."

  try:
    while True:
      s.listen(5)
      client, address = s.accept()
      print "Connected by ", address
      client_thread = ClientThread(client,address) 
      client_thread.start()  
  except :
    s.close()  

def main():
  listen(PORT_NUMBER)


def test():
  d1 = b'\x24\x41\x09\x17\x90\x26\x11\x09\x27\x16\x01\x17\x50\x37\x69\x30\x05\x00\x30\x46\x75\x0e\x00\x00\x00\xff\xff\xfb\xff\xff\x00\x1e\x04\x00\x00\x00\x00\x00\xd0\x01\x00\x00\x00\x00\x2e'
  d2 = b'\x2a\x48\x51\x2c\x34\x31\x30\x39\x31\x37\x39\x30\x32\x36\x2c\x56\x31\x2c\x32\x30\x31\x37\x32\x37\x2c\x41\x2c\x35\x30\x33\x37\x2e\x37\x30\x33\x39\x2c\x4e\x2c\x30\x30\x33\x30\x34\x2e\x36\x36\x30\x32\x2c\x45\x2c\x30\x30\x30\x2e\x30\x30\x2c\x30\x30\x30\x2c\x31\x35\x30\x31\x31\x37\x2c\x46\x46\x46\x46\x46\x42\x46\x46\x2c\x32\x30\x38\x2c\x30\x31\x2c\x30\x2c\x30\x2c\x36\x23'
  print '-----------------------------------------------'  
  print to_hexa_human_string(d1)
  print gps_data_to_string(decode_tk_star_gps_data(d1))
  print '-----------------------------------------------'
  print to_hexa_human_string(d2)
  print gps_data_to_string(decode_tk_star_gps_data(d2))
  print '-----------------------------------------------'
  
if __name__ == "__main__":
   main()
   #test()

#!/usr/bin/env python

"""
Server to send bash commands to standard input. Sends output back to client
"""
import select
import socket
import subprocess
import sys
import threading

class Server:
  def __init__(self):
    self.host = '172.23.61.54' 
    self.port = 12345
    self.server = None
    self.threads = []

  def open_socket(self):
    try:
      self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.server.bind((self.host, self.port))
      self.server.listen(5)
    except socket.error, (value, message):
      if self.server:
        self.server.close()
      print "Could not open socket: " + message
      sys.exit(1)

  def run(self):
    self.open_socket()
    running = True
    while running:
      c = Client(self.server.accept())
      c.start()
      self.threads.append(c)
      
    self.server.close()
    for c in self.threads:
      c.join()
          

class Client(threading.Thread):
  def __init__(self, (client, address)):
    threading.Thread.__init__(self)
    self.client = client
    self.address = address
    self.size = 1024

  def run(self):
    running = True
    while running:
      data = self.client.recv(self.size)
      if data:
        #for now, echo
        print(data)
        process = subprocess.Popen(
            data.decode('utf-8'), 
            shell=True,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        stdoutdata, stderrdata = process.communicate()
        try:
          if(stdoutdata == ""):
            self.client.send(bytes("Request completed!"))
          else: 
            self.client.send(bytes(stdoutdata))
        except socket.error, (value, message):
          print "Failed to send output: " + stdoutdata
          print "Error: " + message

      else:
        self.client.close()
        running = False

if __name__ == "__main__":
  s = Server()
  s.run()

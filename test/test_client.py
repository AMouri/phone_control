#!/usr/bin/env python

"""
Client to manually hit server for local testing
"""
import socket
import sys

class Client:
  def __init__(self):
    self.host = '172.23.61.54'
    print self.host
    self.port = 12345
    self.client = None

  def open_socket(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      self.client.connect((self.host, self.port))
      print("Connection established!")
    except Exception, e:
      print(e)
      sys.exit(1)

  def run(self):
    self.open_socket()
    data = ''

    while data != 'quit':
      data = raw_input("CMD :")
      self.client.send(data)
      print(self.client.recv(1024))

    self.client.close()

if __name__ == "__main__":
  c = Client()
  c.run()

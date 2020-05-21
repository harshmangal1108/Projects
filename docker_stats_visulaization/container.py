#!/usr/bin/python3
import os 
for i in range(1,26):
  os.system("docker run -itd --name iiec{} alpine ping fb.com".format(i))
for i in range(26,51):
  os.system("docker run -itd --name iiec{} centos ping fb.com".format(i))
for i in range(51,76):
  os.system("docker run -itd --name iiec{} fedora ping fb.com".format(i))
for i in range(76,101):
  os.system("docker run -itd --name iiec{}  python".format(i))
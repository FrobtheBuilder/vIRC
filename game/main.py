import os
import sys


renpy = None
config = None

def auto_image():
   for fname in os.listdir(config.gamedir + '/img'):
      if fname.endswith(('.jpg', '.png')):
         tag = fname[:-4]
         fname =  'img/' + fname
      renpy.image(tag, fname)



def initialize(r, c):
   global renpy
   global config

   

   renpy = r
   config = c
   sys.path.append(os.path.join(config.gamedir, "lib"))
   print sys.path
   auto_image()
   

def start():
   pass
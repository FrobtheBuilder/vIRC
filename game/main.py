import os
def initialize(renpy, config):
   for fname in os.listdir(config.gamedir + '/img'):
      if fname.endswith(('.jpg', '.png')):
         tag = fname[:-4]
         fname =  'img/' + fname
   renpy.image(tag, fname)
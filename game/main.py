import os
import sys
#sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
#sys.path.append(os.path.join(config.gamedir, "lib"))
import irc.client
import irc.connection
from ircconfig import ircconf
#import socks

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
   
   print sys.path

   auto_image()
   

def start():
   

   pass

def get_reactor():
   
   #socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, 'localhost', 666)
   #socks.wrapmodule(irc.client)

   reactor = irc.client.Reactor()
   c = reactor.server().connect(
         ircconf['server'],
         ircconf['port'],
         ircconf['nick'],
         password=ircconf['passwd'],
         connect_factory=irc.connection.Factory()
      )
   return reactor
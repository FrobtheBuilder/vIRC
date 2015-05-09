import os
import sys
import irc.client
import irc.connection
from ircconfig import ircconf
if ircconf['socks']['enabled']:
   import socks

#initialized by initialize()
renpy = None
config = None

#initialized by start()
reactor = None
loop = None

def event_loop(st, at, re):
   re.process_once(0.2)
   #return Null(), 0.5
   return renpy.display.layout.Null(), 0.5

def on_pubmsg(connection, event):
   renpy.call("msg", str(event.source), event.arguments[0])

def auto_image():
   for fname in os.listdir(config.gamedir + '/img'):
      if fname.endswith(('.jpg', '.png')):
         tag = fname[:-4]
         fname =  'img/' + fname
      renpy.image(tag, fname)

def initialize(r):
   global renpy
   global config

   renpy = r
   config = renpy.config

   auto_image()

def start():
   global reactor
   global loop

   if ircconf['socks']['enabled']:
      socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ircconf['socks']['host'], ircconf['socks']['port'])
      socks.wrapmodule(irc.client)
   
   reactor = irc.client.Reactor()
   c = reactor.server().connect(
         ircconf['server'],
         ircconf['port'],
         ircconf['nick'],
         password=ircconf['passwd'],
         connect_factory=irc.connection.Factory()
      )
   reactor.add_global_handler("pubmsg", on_pubmsg)
   loop = renpy.display.layout.DynamicDisplayable(event_loop, reactor)
   renpy.show("loop", what=loop)
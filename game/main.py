from __future__ import division
import os
import sys
import irc.client
import irc.connection
from ircconfig import ircconf
if ircconf['socks']['enabled']:
   import socks
from util import get_image_size

imageinfo = {}

#initialized by initialize()
renpy = None
config = None

#initialized by start()
reactor = None
loop = None

def event_loop(st, at, re):
   re.process_once(0.2)
   return renpy.display.layout.Null(), 0.5

def on_pubmsg(connection, event):
   renpy.call("msg", str(event.source), event.arguments[0])

def load_images():
   for fname in os.listdir(config.gamedir + '/img'):
      if fname.endswith(('.jpg', '.png')):
         tag = fname[:-4]
         fname =  'img/' + fname
      imageinfo[tag] = {'path': fname,
                        'size': get_image_size(os.path.join(config.gamedir, fname))}
      imageinfo[tag]['ratio'] = imageinfo[tag]['size'][0]/imageinfo[tag]['size'][1]

      renpy.image(tag, renpy.display.im.Scale(fname, imageinfo[tag]['ratio']*550, 550))
      imageinfo[tag]['scaled'] = renpy.display.im.Scale(fname, imageinfo[tag]['ratio']*550, 550)

def initialize(r):
   global renpy
   global config

   renpy = r
   config = renpy.config

   load_images()


def start():
   global reactor
   global loop

   if ircconf['socks']['enabled']:
      socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ircconf['socks']['host'], ircconf['socks']['port'])
      socks.wrapmodule(irc.client)

   reactor = irc.client.Reactor()
   c = reactor.server().connect( ircconf['server'],
                                 ircconf['port'],
                                 ircconf['nick'],
                                 password=ircconf['passwd'],
                                 connect_factory=irc.connection.Factory())

   reactor.add_global_handler("pubmsg", on_pubmsg)
   loop = renpy.display.layout.DynamicDisplayable(event_loop, reactor)
   renpy.show("loop", what=loop)